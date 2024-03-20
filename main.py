from fastapi import Depends, FastAPI, HTTPException, Header, Form
from typing import Optional, Annotated

from core.models import database
from core.crud import user as user_crud
from core.crud import subscription as subscription_crud

from sqlmodel import Session

from datetime import datetime

database.create_db_and_tables()
app = FastAPI()

def get_db():
    db = Session(database.engine)
    try:
        yield db
    finally:
        db.close()

@app.get('/users')
async def users(db_session: Session = Depends(get_db)):
    with db_session:
        users = user_crud.get_users(session=db_session)
    return users

@app.get('/subscriptions')
async def subscriptions(db_session: Session = Depends(get_db)):
    with db_session:
        subscriptions = subscription_crud.get_subscriptions(session=db_session)
    return subscriptions

@app.post('/chat')
async def respond_to_chat(query: Annotated[str, Form()],
                            session_token: Optional[str] = Header(None),
                            db_session: Session = Depends(get_db)):
            request_time = datetime.now()
            formatted_time = request_time.strftime("%Y-%m-%d %H:%M:%S")
            return { 'query': query, 'response': f"Echoing {query}", 'request_time': formatted_time}
