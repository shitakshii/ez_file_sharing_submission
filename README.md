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

## 📂 Project Structure

