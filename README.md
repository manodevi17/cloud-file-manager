# Cloud File Manager

A cloud-based file management system built with Flask and AWS S3.

## Technologies Used
- Python 3.13
- Flask
- Boto3 (AWS SDK)
- Moto (AWS S3 simulation)
- HTML/CSS

## Features
- Upload files (PDF, JPG, PNG only)
- Maximum file size: 5MB
- Download files
- Delete files
- Upload timestamp display
- IAM role-based access control (Admin and Viewer roles)

## IAM Roles
- Admin: upload, download, delete
- Viewer: download only

## Architecture
User (Browser) → Flask App → Boto3 → AWS S3 Bucket
                                ↑
                         IAM Role controls access

## How to Run
1. Install dependencies: pip install flask boto3 moto
2. Run: python app.py
3. Open browser: http://127.0.0.1:5000

git add .
git commit -m "Added AWS architecture and deployment documentation"
git push