from fastapi import Depends, status, HTTPException, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy import and_
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/vote', tags=['votes']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(payLoad: schemas.VoteReq, db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):
    # check if post exists
    post_query = db.query(models.Post).filter(
        models.Post.id == payLoad.post_id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post doesn't exist")

    vote_query = db.query(models.Vote).filter(and_(models.Vote.post_id ==
                                                   payLoad.post_id, models.Vote.usr_id == current_user.id))

    if payLoad.dir == 1:
        if vote_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id} has liked the post {vote_query.first().post_id}")
        new_vote = models.Vote(post_id=payLoad.post_id, usr_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added new vote"}
    else:
        if not vote_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote doesn't exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}
