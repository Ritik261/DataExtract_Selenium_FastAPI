from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.extract.extract import login_and_extract
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class LoginRequest(BaseModel):
    login_url: str
    username: str
    password: str    

origins = [
    "*"
    # "http://localhost:5173",
    # "http://localhost:5173/"   # React Vite frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello():
    return {"status": "working"}

@app.post("/login-and-extract")
def login_extract_api(data: LoginRequest):
    try:
        result = login_and_extract(data)
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))