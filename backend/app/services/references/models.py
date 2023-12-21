from sqlmodel import SQLModel, Field, UniqueConstraint


class ReferenceBase(SQLModel):
    reference: str = Field(default=None, index=True)
    full_reference: str | None
    publication_year: int | None
    link_to_experimental_paper: str | None
    corresponding_author_name: str | None
    corresponding_author_email: str | None
    request_data_available: str | None
    link_to_request_data: str | None


class Reference(ReferenceBase, table=True):
    __table_args__ = (UniqueConstraint("id"),)
    id: int = Field(
        default=None,
        nullable=False,
        primary_key=True,
        index=True,
    )


class ReferenceRead(ReferenceBase):
    id: int


class ReferenceCreate(ReferenceBase):
    pass


class ReferenceUpdate(ReferenceBase):
    pass
