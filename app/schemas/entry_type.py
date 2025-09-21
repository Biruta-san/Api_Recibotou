from pydantic import BaseModel

class EntryTypeBase(BaseModel):
    name: str

class EntryTypeCreate(EntryTypeBase):
    pass

class EntryTypeUpdate(EntryTypeBase):
    pass

class EntryTypeOut(EntryTypeBase):
    id: int

    class Config:
        from_attributes = True