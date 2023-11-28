from sqlalchemy import Column, Integer, String

from mast.database import Base

class Reference(Base):
    __tablename__ = "reference"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, unique=True, index=True)
    full_reference = Column(String, unique=True, index=True)
    publication_year = Column(Integer)
    link_to_experimental_paper = Column(String)
    corresponding_author_name = Column(String)
    corresponding_author_email = Column(String)
    request_data_available = Column(String)
    link_to_request_data = Column(String)
