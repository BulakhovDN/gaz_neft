from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import require_user_role
from src.db.database import get_db
from src.db.models.user import User
from src.models.note import NoteCreate
from src.models.note import NoteResponse
from src.services.note_service import NoteService

router = APIRouter()


@router.post("/", response_model=NoteResponse)
async def create_note(
    note_in: NoteCreate,
    current_user: User = Depends(require_user_role),
    db: AsyncSession = Depends(get_db),
):
    service = NoteService(db, user_id=current_user.id, role=current_user.role)
    return await service.create_note(note_in)


@router.get("/", response_model=list[NoteResponse])
async def read_own_notes(
    current_user: User = Depends(require_user_role), db: AsyncSession = Depends(get_db)
):
    service = NoteService(db, user_id=current_user.id, role=current_user.role)
    return await service.get_notes_by_user()


@router.get("/{note_id}", response_model=NoteResponse)
async def read_own_note(
    note_id: int,
    current_user: User = Depends(require_user_role),
    db: AsyncSession = Depends(get_db),
):
    service = NoteService(db, user_id=current_user.id, role=current_user.role)
    return await service.get_note_by_id(note_id)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_own_note(
    note_id: int,
    note_in: NoteCreate,
    current_user: User = Depends(require_user_role),
    db: AsyncSession = Depends(get_db),
):
    service = NoteService(db, user_id=current_user.id, role=current_user.role)
    return await service.update_note(note_id, note_in)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_own_note(
    note_id: int,
    current_user: User = Depends(require_user_role),
    db: AsyncSession = Depends(get_db),
):
    service = NoteService(db, user_id=current_user.id, role=current_user.role)
    await service.soft_delete_note(note_id)
