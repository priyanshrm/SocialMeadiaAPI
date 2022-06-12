from fastapi import Depends, status, HTTPException, APIRouter, Response
from .. import schemas, database, models, utils, oauth2
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix='/users', tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRes)
def create_user(payLoad: schemas.UserReq, db: Session = Depends(database.get_db)):
    user_exist = db.query(models.User).filter(
        models.User.username == payLoad.username).first()
    if user_exist is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'user with username {payLoad.username} already exists')

    user_exist = db.query(models.User).filter(
        models.User.email == payLoad.email).first()

    if user_exist is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'user with email {payLoad.email} already exists')
    # hash the PASSWORD first before storing the user in the database
    payLoad.password = utils.hash(payLoad.password)

    user = models.User(**payLoad.dict())
    db.add(user)  # stage change to db
    db.commit()  # commit to db
    db.refresh(user)  # refresh the new post and store in the same variable
    return user


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.UserRes])
def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).order_by('id').all()
    return users


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserRes)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} not found')
    return user.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_user(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.username != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'You are not authorized to Delete this user!')
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} not found!')
    user.delete(synchronize_session=False)
    db.commit()
