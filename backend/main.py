from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import List
from supabase import Client, create_client
from supabase_auth.errors import AuthApiError
import os
from database import Base, engine, get_db
from schemas import AuthRequest, NoteResponse, NoteCreate, NoteUpdate
from models import Note

load_dotenv()

security = HTTPBearer()
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI(title="Notes")

Base.metadata.create_all(bind=engine)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)
    except AuthApiError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if not response.user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return response.user


@app.get("/")
def root():
    return {"message": "Welcome To Notes App"}


@app.post("/signup")
def signup(data: AuthRequest):
    response = supabase.auth.sign_up(
        {
            "email": data.email,
            "password": data.password,
        }
    )
    return response


@app.post("/login")
def login(data: AuthRequest):
    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": data.email,
                "password": data.password,
            }
        )
        return response
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@app.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note: NoteCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if db.query(Note).filter(Note.title == note.title, Note.user_id == current_user.id).first():
        raise HTTPException(
            status_code=400, detail="note with this name already exists"
        )
    new_note = Note(title=note.title, content=note.content, user_id=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@app.get("/notes", response_model=List[NoteResponse])
def get_all_notes(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    all_notes = db.query(Note).filter(Note.user_id == current_user.id).all()
    return all_notes


@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note: NoteUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == current_user.id)
        .first()
    )
    if not db_note:
        raise HTTPException(status_code=404, detail="note not found!")
    db_note.title = note.title
    db_note.content = note.content

    db.commit()
    db.refresh(db_note)

    return db_note


@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    db_note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == current_user.id)
        .first()
    )
    if not db_note:
        raise HTTPException(status_code=404, detail="note not found!")
    db.delete(db_note)
    db.commit()
    return {"message": "note deleted"}
