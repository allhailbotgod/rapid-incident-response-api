from fastapi import APIRouter
from fastapi.routing import APIRoute
from app.agencies.routes import router as agencies_router
from app.auth.routes import router as auth_router
from app.medic.routes import router as medic_router
from app.reports.routes import router as reports_router
from app.roles.routes import router as roles_router
from app.sos.routes import router as sos_router
from app.status.routes import router as status_router
from app.users.routes import router as users_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(agencies_router, tags=["Agencies"])
api_router.include_router(auth_router, tags=["Authentication"])
api_router.include_router(medic_router, tags=["Medicals"])
api_router.include_router(reports_router, tags=["Reports / Incidents"])
api_router.include_router(roles_router, tags=["Roles"])
api_router.include_router(sos_router, tags=["Emergency Contacts"])
api_router.include_router(status_router, tags=["Incidents Status"])
api_router.include_router(users_router, tags=["Users"])
