from fastapi import FastAPI
from app.routes import auth
from app.database.connection import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Data Analyzer API")

app.include_router(auth.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}
