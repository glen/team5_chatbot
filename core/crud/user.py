from sqlmodel import Session, select
from core.models.user import User

def get_users(session: Session):
    statement = select(User)
    users = session.exec(statement).all()
    return users
