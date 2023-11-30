"""
Handle / requests
"""
from fastapi import Cookie, Header, APIRouter

from typing import Union

router = APIRouter()

@router.get("/ping", status_code=200, description="-- service check --")
async def ping(AuthSession: Union[str, None] = Cookie(default=None),
               Authorization: Union[str, None] = Header(default=None)):

    return {
        "status": "success"
    }
