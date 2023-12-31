# THIS FILE CONTAINS THE AUTHORIZATION
from fastapi import  FastAPI,Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext  # INSTALLED passlib[bycrypt] { pip install "passlib[bcrypt]" }
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm ,OAuth2PasswordBearer # for authento=ication
from datetime import datetime ,timedelta
from jose import jwt, JWTError

SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"
ALGORITHM = "HS256"


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


bcrypt_context = CryptContext(schemes=["bcrypt"] , deprecated ="auto")

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    # CHECKING WHETHER ENTERED PASSWORD AND THE HASHED PASSWORD ARE SAME OR NOT
    return bcrypt_context.verify(plain_password, hashed_password)


# FIRST CHECKING IF THE USERNAME MATCHES ANY OF THEN NAME FROM THE TABLE THEN VERIFYING THE PASSWORD
def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User)\
        .filter(models.User.username == username)\
        .first()
    if not user:
        raise HTTPException(status_code=404, detail="Incorrect username")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Incorrect Password")
    return user

def create_access_token(username: str , user_id : int ,expires_delta: Optional[timedelta] = None):
    encode = { "sub" : username , "id": user_id }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp" : expire})
    return jwt.encode(encode , SECRET_KEY , algorithm=ALGORITHM)


async def get_current_user(token : str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username : str = payload.get("sub")
        user_id = inr = payload.get("id")
        if username is None or user_id is None :
            raise HTTPException(status_code=404 , detail="User not found")
        return { "username" : username , "id" :user_id }
    except JWTError:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/create/user")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = models.User()
    create_user_model.username = create_user.username
    create_user_model.email = create_user.email
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name

    hash_password = get_password_hash(create_user.password)

    create_user_model.hashed_password = hash_password
    create_user_model.is_active = True


    db.add(create_user_model)
    db.commit()


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username,user.id,expires_delta=token_expires)
    return {"token" : token}
