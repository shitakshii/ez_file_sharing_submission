# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import auth, file_routes
from app.database import Base, engine

# Create DB tables (only for local development)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure File Sharing System",
    version="1.0.0"
)

# CORS config - allow localhost frontend or Postman
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router)
app.include_router(file_routes.router)

@app.get("/")
def root():
    return {"message": "🚀 Secure File Sharing Backend is running!"}
