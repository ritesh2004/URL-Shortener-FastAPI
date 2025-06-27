from fastapi import APIRouter, HTTPException, Response

from app.model.model import URLBaseModel, URLCreate, URLRead, URLDelete, URL
from app.config.db import SessionLocal

from typing import Annotated
from sqlmodel import Session, select
from fastapi import Depends

from app.utils import generate_hash

from app.config.config import settings

import datetime

router = APIRouter(prefix="/url", tags=["url"])

def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()

@router.post("/generate", response_model=URLRead)
async def generate_url(url: URLBaseModel, session: Session = Depends(get_db)):
    """
    Generate a new URL.
    """
    url_data = url.model_dump()
    
    hash_code = await generate_hash(url_data["original_url"])
    
    is_exist = select(URL).where(URL.code == hash_code)
    result = session.exec(is_exist).first()
    
    if result:
        raise HTTPException(status_code=400, detail="URL already exists")
    
    url_data["code"] = hash_code
    url_data["short_url"] = f"http://localhost:8000/api/v1/url/{url_data['code']}"
    url_data["expiration_time"] = (datetime.datetime.now() + datetime.timedelta(days=settings.EXPIRATION_TIME)).isoformat()
    url_data["created_at"] = datetime.datetime.now().isoformat()
    url_data["updated_at"] = datetime.datetime.now().isoformat()
    
    url_obj = URL(**url_data)
    session.add(url_obj)
    session.commit()
    session.refresh(url_obj)
    return url_obj

@router.get("/{code}", response_model=URLRead)
async def read_url(code: str, session: Session=Depends(get_db)):
    """Read a URL by its code.
    """
    query = select(URL).where(URL.code == code)
    url = session.exec(query).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    url.clicks += 1
    url.updated_at = datetime.datetime.now().isoformat()
    
    if url.expiration_time and datetime.datetime.fromisoformat(url.expiration_time) < datetime.datetime.now():
        session.delete(url)
        session.commit()
        raise HTTPException(status_code=410, detail="URL has expired")
    
    session.add(url)
    session.commit()
    
    return Response(status_code=302, headers={"Location": url.original_url})