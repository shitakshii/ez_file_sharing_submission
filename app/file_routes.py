# app/file_routes.py

import os
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas, utils, auth
from app.database import get_db
from typing import List
from datetime import datetime
from fastapi.responses import FileResponse

router = APIRouter(prefix="/files", tags=["Files"])

# Folder where files will be saved
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pptx", ".docx", ".xlsx"}

def is_allowed_file(filename: str) -> bool:
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)

@router.post("/upload")
def upload_file(
    uploaded_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.require_ops_user)
):
    if not is_allowed_file(uploaded_file.filename):
        raise HTTPException(status_code=400, detail="Only .pptx, .docx, .xlsx allowed")

    file_path = os.path.join(UPLOAD_DIR, f"{datetime.utcnow().timestamp()}_{uploaded_file.filename}")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.file.read())

    new_file = models.File(
        filename=uploaded_file.filename,
        filepath=file_path,
        user_id=user.id
    )
    db.add(new_file)
    db.commit()
    return {"message": "File uploaded successfully ✅"}

@router.get("/list", response_model=List[schemas.FileOut])
def list_files(
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.require_verified_user)
):
    return db.query(models.File).all()

@router.get("/generate-download-link")
def generate_download_link(
    file_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.require_verified_user)
):
    file = db.query(models.File).filter(models.File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Encrypt file_id + user_id into secure token
    data = f"{file_id}:{user.id}"
    encrypted = utils.encrypt_data(data)
    download_url = f"http://localhost:8000/files/download?token={encrypted}"
    return {"download_url": download_url}

@router.get("/download")
def download_file(
    token: str,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # Decrypt the token to extract file_id and user_id
        decrypted = utils.decrypt_data(token)
        file_id_str, token_user_id_str = decrypted.split(":")
        file_id = int(file_id_str)
        token_user_id = int(token_user_id_str)

        # Extract and decode JWT from Authorization header
        jwt_token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not jwt_token:
            raise HTTPException(status_code=401, detail="Missing Authorization token")

        payload = utils.decode_jwt(jwt_token)
        current_user_id = payload.get("user_id")

        if current_user_id != token_user_id:
            raise HTTPException(status_code=403, detail="Unauthorized access to file")

        file = db.query(models.File).filter(models.File.id == file_id).first()
        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        if not os.path.exists(file.filepath):
            raise HTTPException(status_code=404, detail="File not found on disk")

        return FileResponse(path=file.filepath, filename=file.filename)

    except Exception as e:
        print("Download error:", e)
        raise HTTPException(status_code=400, detail="Invalid or expired download token")
