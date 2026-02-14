from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
import logging

app = FastAPI()
logger = logging.getLogger("user-api")
logging.basicConfig(level=logging.INFO)

# --- DTOs / schemas (Pydantic) ---
class UserResp(BaseModel):
    id: int
    name: str

class LoginReq(BaseModel):
    username: str
    password: str

# --- Helpers (placeholder for real auth) ---
def verify_credentials(username: str, password: str) -> bool:
    # TODO: Replace with call to external auth service or verify hashed password
    secret = os.environ.get("AUTH_SECRET")
    if not secret:
        # no secret configured — fail closed
        return False
    return username == "admin" and password == secret

@app.get("/user", response_model=UserResp)
def get_user(id: int):
    logger.info("get_user called id=%s", id)
    return UserResp(id=id, name="Alice")

@app.post("/login")
def login(payload: LoginReq):
    if not verify_credentials(payload.username, payload.password):
        logger.warning("Failed login attempt for user=%s", payload.username)
        raise HTTPException(status_code=401, detail="authentication failed")
    return {"status": "ok"}
