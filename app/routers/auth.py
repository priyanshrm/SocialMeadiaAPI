from fastapi import Depends, status, HTTPException, APIRouter
from .. import schemas, database, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_

router = APIRouter(
   tags=['Authenticate']
)


@router.post('/login', response_model=schemas.Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
   user = db.query(models.User).filter(or_(models.User.email.like(
       credentials.username), models.User.username.like(credentials.username))).first()

   if not user:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                           detail=f"Invalid Credentials")

   if not utils.verify(credentials.password, user.password):
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                           detail=f"Invalid Credentials")

   # create token
   access_token = oauth2.create_access_token(data={"user_id": user.id})

   # return token
   return {"access_token": access_token, "token_type": "bearer"}
