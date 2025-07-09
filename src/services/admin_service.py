from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.log_utils import log_action
from src.db.models.note import Note


class AdminNoteService:
    def __init__(self, db: AsyncSession, user_id: int, role: str):
        self.db = db
        self.user_id = user_id
        self.role = role

    async def get_all_notes(self) -> List[Note]:
        async with self.db.begin():
            result = await self.db.execute(select(Note))
            notes = result.scalars().all()
            log_action(
                f"Получены все заметки (кол-во: {len(notes)})", self.user_id, self.role
            )
            return notes

    async def get_note_by_id(self, note_id: int) -> Note:
        async with self.db.begin():
            result = await self.db.execute(select(Note).filter(Note.id == note_id))
            note = result.scalars().first()
            if not note:
                log_action(f"Не найдена заметка id={note_id}", self.user_id, self.role)
                raise HTTPException(status_code=404, detail="Note not found")
            log_action(f"Получена заметка id={note_id}", self.user_id, self.role)
            return note

    async def get_notes_by_user(self, user_id: int) -> List[Note]:
        async with self.db.begin():
            result = await self.db.execute(select(Note).filter(Note.user_id == user_id))
            notes = result.scalars().all()
            log_action(
                f"Получены заметки пользователя id={user_id} (кол-во: {len(notes)})",
                self.user_id,
                self.role,
            )
            return notes

    async def restore_note(self, note_id: int) -> None:
        note = await self.get_note_by_id(note_id)
        async with self.db.begin():
            if not note.is_deleted:
                log_action(
                    f"Попытка восстановления активной заметки id={note_id}",
                    self.user_id,
                    self.role,
                )
                raise HTTPException(status_code=400, detail="Note is not deleted")
            note.is_deleted = False
            self.db.add(note)
            log_action(f"Восстановлена заметка id={note_id}", self.user_id, self.role)
