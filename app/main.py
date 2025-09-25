

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import auth_routes, dashboard_routes

from app.database import Base, engine
from app.models import user  # import models so Base knows them


app = FastAPI()

# ✅ serve static files (for PDFs, CSS, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


Base.metadata.create_all(bind=engine)

# ✅ include routes
app.include_router(auth_routes.router)
app.include_router(dashboard_routes.router)


