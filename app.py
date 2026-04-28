from flask import Flask, request, render_template, redirect, url_for
import boto3
from moto import mock_aws

app = Flask(__name__)

BUCKET_NAME = "my-filemanager-bucket"

CURRENT_ROLE = "viewer" 
IAM_POLICIES = {
    "admin": ["upload", "download", "delete"],
    "viewer": ["download"]
}

def is_allowed(action):
    return action in IAM_POLICIES[CURRENT_ROLE]

mock = mock_aws()
mock.start()

s3 = boto3.client(
    "s3",
    region_name="us-east-1",
    aws_access_key_id="fake",
    aws_secret_access_key="fake"
)

s3.create_bucket(Bucket=BUCKET_NAME)

@app.route("/")
def index():
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    files = response.get("Contents", [])
    return render_template("index.html", files=files)

MAX_SIZE = 5 * 1024 * 1024 

@app.route("/upload", methods=["POST"])
def upload():
    if not is_allowed("upload"):
        return "Access Denied: Your role does not have upload permission.", 403
    file = request.files["file"]
    extension = file.filename.rsplit(".", 1)[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return "File type not allowed. Only PDF, JPG, PNG accepted.", 400
    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0)
    if file_size > MAX_SIZE:
        return "File too large. Maximum size is 5MB.", 400
    s3.upload_fileobj(file, BUCKET_NAME, file.filename)
    return redirect(url_for("index"))

ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}

def upload():
    file = request.files["file"]
    extension = file.filename.rsplit(".", 1)[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return "File type not allowed. Only PDF, JPG, PNG accepted.", 400
    s3.upload_fileobj(file, BUCKET_NAME, file.filename)
    return redirect(url_for("index"))

@app.route("/download/<filename>")
def download(filename):
    file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=filename)
    return file_obj["Body"].read(), 200, {
        "Content-Disposition": f"attachment; filename={filename}"
    }

@app.route("/delete/<filename>")
def delete(filename):
    if not is_allowed("delete"):
        return "Access Denied: Your role does not have delete permission.", 403
    s3.delete_object(Bucket=BUCKET_NAME, Key=filename)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)