from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.auth_manager import auth_handler, get_current_user, get_current_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create new user and return user info"""
    user = await auth_handler.create_user(user_data.dict(), db)
    return user

@router.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    return await auth_handler.login(user_data.email, user_data.password, db)

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/admin-only")
async def admin_only(current_user: User = Depends(get_current_admin)):
    return {"message": "Hello admin!"}




# from fastapi import FastAPI, Request, APIRouter
# # from starlette.responses import RedirectResponse
# # from starlette.middleware.sessions import SessionMiddleware
# # from authlib.integrations.starlette_client import OAuth
# import os
# from dotenv import load_dotenv

# load_dotenv()

# auth_router = APIRouter()

# oauth = OAuth()
# oauth.register(
#     name='google',
#     client_id=os.getenv("GOOGLE_CLIENT_ID"),
#     client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
#     server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#     client_kwargs={
#         'scope': 'openid email profile'
#     }
# )

# @app.get('/')
# def index():
#     return {'message': 'Welcome. Click /login to begin OAuth.'}

# @app.get('/login')
# async def login(request: Request):
#     redirect_uri = request.url_for('auth')
#     return await oauth.google.authorize_redirect(request, redirect_uri)

# @app.get('/auth')
# async def auth(request: Request):
#     token = await oauth.google.authorize_access_token(request)
#     user = await oauth.google.parse_id_token(request, token)
#     return {"user_info": user}


