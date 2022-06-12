from fastapi import Depends, status, HTTPException, APIRouter
from .. import schemas, database, models
from sqlalchemy.orm import Session



router = APIRouter(
    prefix='/posts', tags=['Posts']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostRes)
def create_post(payLoad: schemas.PostReq, db: Session = Depends(database.get_db)):
    post = models.Post(**payLoad.dict())
    db.add(post)  # stage change to db
    db.commit()  # commit to db
    db.refresh(post)  # refresh the new post and store in the same variable
    return post


@router.get('/')
def get_posts():
    pass


@router.get('/{id}')
def get_post():
    pass


@router.delete('/{id}')
def delete_post():
    pass


@router.put('/{id}')
def update_post():
    pass
