from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.services import users_service
from app.db.db import get_db_session
from app.schemas.schemas import (
    UserCreate, UserLogin
)
from app.schemas.response_schema import return_response


router = APIRouter()

@router.post("/register")
async def create_user(user_data: UserCreate, session: Session = Depends(get_db_session)):
    """
    Create new user.
    """
    user = users_service.get_user_by_email(session=session, email=user_data.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = users_service.create_user(session=session, user_data=user_data)
    if user and user.is_active:
        return return_response(data=user.email)
    return return_response(
        success=False,
        data="User Creation Failed",
        status_code=500
    )

@router.post("/login")
def login_access_token(user: UserLogin, session: Session = Depends(get_db_session)):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = users_service.authenticate(
        session=session, email=user.email, password=user.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token = security.create_access_token(
            user.id,
            user.name,
            user.role,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    return return_response(
        data={
            "access_token": access_token
        }
    )
