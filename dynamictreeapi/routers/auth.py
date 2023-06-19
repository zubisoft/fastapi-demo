
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from .. import database, models, schemas, utils, authentication

router = APIRouter(prefix='/login',tags=['Authentication'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Token)
async def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):


    user = db.query(models.Users).filter(models.Users.email == credentials.username).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN
                            ,detail=f"Authentication details email incorrect" )
    

    if not (utils.validate(credentials.password,user.password)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN
                            ,detail=f"Authentication details incorrect" )
    
    token = authentication.create_access_token({"user_id":user.id})

    return token
