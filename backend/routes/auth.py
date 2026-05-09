from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database.connection import get_db
from models.all_models import User
from middleware.auth import get_password_hash, verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter(prefix='/auth', tags=['Authentication'])

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'User registered successfully'}

@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    
    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer', 'username': user.username}