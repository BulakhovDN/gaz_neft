from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.log_utils import log_action
from src.db.models.note import Note
from src.models.note import NoteCreate


class NoteService:
    def __init__(self, db: AsyncSession, user_id: int, role: str):
        self.db = db
        self.user_id = user_id
        self.role = role

    async def create_note(self, note_in: NoteCreate) -> Note:
        async with self.db.begin():
            new_note = Note(**note_in.dict(), user_id=self.user_id)
            self.db.add(new_note)
            log_action("Создана заметка", self.user_id, self.role)
            return new_note

    async def get_notes_by_user(self) -> List[Note]:
        async with self.db.begin():
            stmt = select(Note).filter(
                Note.user_id == self.user_id, Note.is_deleted == False
            )
            result = await self.db.execute(stmt)
            notes = result.scalars().all()
            log_action(
                f"Получен список заметок (кол-во: {len(notes)})",
                self.user_id,
                self.role,
            )
            return notes

    async def get_note_by_id(self, note_id: int) -> Note:
        async with self.db.begin():
            stmt = select(Note).filter(
                Note.id == note_id,
                Note.user_id == self.user_id,
                Note.is_deleted == False,
            )
            result = await self.db.execute(stmt)
            note = result.scalars().first()
            if not note:
                log_action(
                    f"Не найдена заметка с id={note_id}", self.user_id, self.role
                )
                raise HTTPException(status_code=404, detail="Note not found")
            log_action(f"Получена заметка id={note_id}", self.user_id, self.role)
            return note

    async def update_note(self, note_id: int, note_in: NoteCreate) -> Note:
        note = await self.get_note_by_id(note_id)
        async with self.db.begin():
            note.title = note_in.title
            note.body = note_in.body
            self.db.add(note)
            log_action(f"Обновлена заметка id={note_id}", self.user_id, self.role)
            return note

    async def soft_delete_note(self, note_id: int) -> None:
        note = await self.get_note_by_id(note_id)
        async with self.db.begin():
            note.is_deleted = True
            self.db.add(note)
            log_action(f"Удалена (soft) заметка id={note_id}", self.user_id, self.role)
