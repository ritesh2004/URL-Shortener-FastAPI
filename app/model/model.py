from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List


class URLBaseModel(SQLModel):
    original_url: str = Field(index=True, nullable=False)
    

class URL(URLBaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    short_url: Optional[str] = Field(default=None, index=True, nullable=False)
    code: str = Field(index=True, unique=True, nullable=False)
    clicks: int = Field(default=0, nullable=False)
    expiration_time: Optional[str] = Field(default=None, nullable=True)
    created_at: Optional[str] = Field(default=None, nullable=False)
    updated_at: Optional[str] = Field(default=None, nullable=False)
    
class URLCreate(URLBaseModel):
    pass

class URLRead(URLBaseModel):
    id: int
    short_url: str
    original_url: str
    created_at: str
    updated_at: str
    
class URLDelete(URLBaseModel):
    id: int
