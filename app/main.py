from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import api_router

app = FastAPI(
    title="Rapid Incident Response API",
    summary="REST API for real-time emergency reporting, incident management, dispatch coordination, and response tracking.",
    description="This Rapid Incident Response API provides secure endpoints for reporting emergencies, managing incidents, dispatching response agencies, nd tracking response progress in real time. It supports public user, emergency dispatchers, hospitals, police, and fire service personnel through role-based access control, enabling faster coordination and efficient emergency response.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=settings.CORS_CREDS,
    allow_origins=settings.ORIGINS,
    allow_headers=settings.HEADERS,
    allow_methods=settings.METHODS,
)

app.include_router(api_router)
