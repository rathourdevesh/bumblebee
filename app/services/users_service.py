from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.models import User
from app.schemas.schemas import UserCreate

def create_user(*, session: Session, user_data: UserCreate) -> User:
    user_object = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        password= get_password_hash(user_data.password),
        role=user_data.role
    )
    session.add(user_object)
    session.commit()
    session.refresh(user_object)
    return user_object

# def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
#     user_data = user_in.model_dump(exclude_unset=True)
#     extra_data = {}
#     if "password" in user_data:
#         password = user_data["password"]
#         hashed_password = get_password_hash(password)
#         extra_data["hashed_password"] = hashed_password
#     db_user.sqlmodel_update(user_data, update=extra_data)
#     session.add(db_user)
#     session.commit()
#     session.refresh(db_user)
#     return db_user


def get_user_by_email(*, session: Session, email: str) -> User:
    session_user = session.query(User).filter(User.email == email).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user
