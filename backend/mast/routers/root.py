"""
Handle / requests
"""
from fastapi import APIRouter

from mast import __name__ as name
from mast import __version__

router = APIRouter()


@router.get("/")
async def root():
    """
    Get Info
    """
    return {"name": name, "version": __version__}
