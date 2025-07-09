from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class NoteCreate(BaseModel):
    title: str = Field(
        ..., max_length=256, description="Заголовок длиной не более 256 символов"
    )
    body: str = Field(..., max_length=65536, description="Тело не более 65536 символов")


class NoteResponse(NoteCreate):
    id: int
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
