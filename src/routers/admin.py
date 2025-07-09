from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import admin_required
from src.db.database import get_db
from src.db.models.user import User
from src.models.note import NoteResponse
from src.services.admin_service import AdminNoteService

router = APIRouter()


@router.get("/notes/", response_model=list[NoteResponse])
async def read_all_notes(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(admin_required)
):
    service = AdminNoteService(db, user_id=current_user.id, role=current_user.role)
    return await service.get_all_notes()


@router.get("/notes/{note_id}", response_model=NoteResponse)
async def read_note_admin(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    service = AdminNoteService(db, user_id=current_user.id, role=current_user.role)
    return await service.get_note_by_id(note_id)


@router.get("/users/{user_id}/notes/", response_model=list[NoteResponse])
async def read_user_notes_admin(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    service = AdminNoteService(db, user_id=current_user.id, role=current_user.role)
    return await service.get_notes_by_user(user_id)


@router.post("/notes/{note_id}/restore")
async def restore_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    service = AdminNoteService(db, user_id=current_user.id, role=current_user.role)
    await service.restore_note(note_id)
    return {"detail": "Note restored"}
