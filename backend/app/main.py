"""
Application entrypoint.

Wires together:
- CORS
- DB initialization (create_all on startup)
- All API routers
- Static file serving for the frontend (so the whole project can be run
  from a single command during development)
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.infrastructure.database.session import init_db

from app.presentation.api.routes_auth import router as auth_router
from app.presentation.api.routes_clients import router as clients_router
from app.presentation.api.routes_websites import router as websites_router
from app.presentation.api.routes_orders import router as orders_router
from app.presentation.api.routes_link_check import router as link_check_router
from app.presentation.api.routes_analytics import router as analytics_router

app = FastAPI(
    title="Guest Post & Backlink Management Engine",
    description="Client & order management, automated link health checks, "
                "website quality metrics, and revenue analytics.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(websites_router)
app.include_router(orders_router)
app.include_router(link_check_router)
app.include_router(analytics_router)


@app.on_event("startup")
def on_startup():
    init_db()


# --- Serve the frontend (login page + dashboard) ---------------------------
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
    app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")

    @app.get("/", include_in_schema=False)
    def serve_login():
        return FileResponse(str(FRONTEND_DIR / "index.html"))

    @app.get("/dashboard.html", include_in_schema=False)
    def serve_dashboard():
        return FileResponse(str(FRONTEND_DIR / "dashboard.html"))
