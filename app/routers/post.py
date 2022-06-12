from fastapi import Depends, Response, status, HTTPException, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix='/posts', tags=['Posts']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostRes)
def create_posts(payLoad: schemas.PostReq, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # ensures that payLoad is of PostCreate
    # Using ** it unpacks the payLoad dictionary
    post = models.Post(usr_id=current_user.id, **payLoad.dict())
    db.add(post)  # stage change to db
    db.commit()  # commit to db
    db.refresh(post)  # refresh the new post and store in the same variable
    return post


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostRes2])
def get_posts(db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                                                                                       isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).order_by('id').limit(limit).offset(skip).all()
    return posts


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostRes2)
def get_post(id: int, db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post with id {id} doesn't exist!")

    return post.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post with id {id} doesn't exist!")
    post_one = post.first()
    if post_one.usr_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You cannot delete this post!")
    post.delete(synchronize_session=False)
    db.commit()


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostRes2)
def update_post(id: int, payLoad: schemas.PostReq, db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
    if post.first().usr_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to update this post!")

    post.update(payLoad.dict(), synchronize_session=False)
    db.commit()  # commit to db
    post = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)
    return post.first()
