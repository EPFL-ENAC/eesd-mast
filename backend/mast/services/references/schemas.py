from pydantic import BaseModel

class ReferenceBase(BaseModel):
    reference: str | None = None
    full_reference: str | None = None
    publication_year: int | None = None
    request_data_available: str | None = None
    link_to_request_data: str | None = None
    link_to_experimental_paper: str | None = None
    corresponding_author_name: str | None = None
    corresponding_author_email: str | None = None

class ReferenceCreate(ReferenceBase):
    pass

class Reference(ReferenceBase):
    id: int

    class Config:
        orm_mode = True