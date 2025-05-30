# 🔐 EZ Intern - Secure File Sharing System

This project is a **secure file-sharing backend system** built as part of the EZ Intern Backend Test. It supports two user types (Ops and Client) with encrypted file download links, email verification, and secure access control using Python (Flask) and SQL.

---

## 🚀 Features

- 🔑 **User Authentication**
  - JWT-based login for both Ops and Client users
  - Email verification for Client users
- 📤 **File Upload**
  - Only Ops users can upload `.pptx`, `.docx`, and `.xlsx` files
- 📥 **Secure Download**
  - Encrypted download links (accessible only to verified clients)
- 📃 **File Listing**
  - Clients can list all available files
- 📧 **Email Verification**
  - Secure link sent to registered email

---

## 🛠️ Tech Stack

- **Backend Framework**: Flask
- **Database**: SQLite (can be switched to PostgreSQL or MySQL)
- **Authentication**: JWT (via `Flask-JWT-Extended`)
- **Email**: Flask-Mail with Gmail SMTP
- **Security**: Encrypted download tokens using `cryptography`

---


---

## 🧪 API Collection

A complete **Postman Collection** is included with:
- Client Signup
- Email Verification
- Login (Client & Ops)
- File Upload (Ops)
- File List & Download (Client)

---

## 🧑‍💻 Getting Started

### 1. Clone the repository

git clone https://github.com/shitakshii/ez_file_sharing_submission

cd ez_file_sharing_submission

### 2.  Create a virtual environment and install dependencies

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

---

## Deploy  (Render / Railway)
Platforms like Render.com, Railway.app, or Fly.io support direct Docker deployment:

### 1. Push your code to GitHub

### 2. Connect the repo in the PaaS dashboard

### 3. Set environment variables from .env

### 4. Select Docker as the deploy method

### 5. Click Deploy




