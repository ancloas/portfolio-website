from datetime import datetime, timedelta
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from fastapi import Request, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.user import User
from app.db.session import get_db
import os

# Configurations
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Auth:
    def __init__(self):
        pass

    def generate_jwt(self, user_id: int, is_admin: bool) -> str:
        """Generate a JWT token."""
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "user_id": user_id,
            "is_admin": is_admin,
            "exp": expire
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def decode_jwt(self, token: str):
        """Decode a JWT token."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password hash."""
        return check_password_hash(hashed_password, plain_password)

    def get_password_hash(self, password: str) -> str:
        """Generate password hash."""
        return generate_password_hash(password)

    async def authenticate_user(self, email: str, password: str, db: Session):
        """Authenticate user and return user object."""
        user = db.query(User).filter(User.email == email).first()
        if not user or not self.verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return user

    async def login(self, email: str, password: str, db: Session = Depends(get_db)):
        """Login user and return token."""
        user = await self.authenticate_user(email, password, db)
        token = self.generate_jwt(user.id, user.is_admin)
        return {
            "token": token,
            "user_details": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "is_admin": user.is_admin
            }
        }

    def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """Get current user from token."""
        payload = self.decode_jwt(token)
        user = db.query(User).filter(User.id == payload["user_id"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_current_admin(self, current_user: User = Depends(get_current_user)):
        """Check if current user is admin."""
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Admin access required")
        return current_user

    async def create_user(self, user_data: dict, db: Session):
        """Create a new user."""
        # Check if user already exists
        if db.query(User).filter(User.email == user_data['email']).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        db_user = User(
            email=user_data['email'],
            name=user_data['name'],
            password_hash=self.get_password_hash(user_data['password']),
            is_admin=False  # Default to non-admin
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


auth_handler = Auth()

# Dependency to use in routes
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return auth_handler.get_current_user(token, db)

async def get_current_admin(current_user: User = Depends(get_current_user)):
    return auth_handler.get_current_admin(current_user)