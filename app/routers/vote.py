from fastapi import Depends, status, HTTPException, APIRouter
from .. import schemas

router = APIRouter(
    prefix='/vote', tags=['votes']
)


@router.post('/')
def create_vote():
    pass
