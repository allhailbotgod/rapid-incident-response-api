from fastapi import FastAPI

app = FastAPI(
    title="Rapid Incident Response API",
    summary="REST API for real-time emergency reporting, incident management, dispatch coordination, and response tracking.",
    description="This Rapid Incident Response API provides secure endpoints for reporting emergencies, managing incidents, dispatching response agencies, nd tracking response progress in real time. It supports public user, emergency dispatchers, hospitals, police, and fire service personnel through role-based access control, enabling faster coordination and efficient emergency response.",
    version="1.0.0",
)
