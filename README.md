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

## AWS Architecture (Production Deployment Design)

User (Browser)
     ↓ HTTP Request
Flask App (AWS EC2 - t2.micro, Ubuntu 22.04)
     ↓ Boto3 SDK
AWS S3 Bucket (my-filemanager-bucket, us-east-1)
     ↑
IAM Role (ec2-s3-filemanager-role)
     - Attached to EC2 instance
     - Grants S3 access without hardcoded credentials
     - Admin: upload, download, delete
     - Viewer: download only

## EC2 Deployment Steps (Production)
1. Launch EC2 t2.micro instance (Ubuntu 22.04)
2. Attach IAM role with S3 permissions
3. SSH into instance
4. Install Python, Flask, Boto3
5. Run Flask app with Gunicorn
6. Configure Nginx as reverse proxy
7. Open port 80 for public access

## How to Run Locally
1. Install dependencies: pip install flask boto3 moto
2. Run: python app.py
3. Open browser: http://127.0.0.1:5000
