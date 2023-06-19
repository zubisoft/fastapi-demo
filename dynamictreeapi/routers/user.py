
from typing import List

from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session

from ..database import  get_db
from .. import models, utils,schemas, authentication

router = APIRouter( prefix="/users",tags=["Users"] )

@router.get("/", response_model=List[schemas.UserResponse])
async def get_datasets(db: Session = Depends(get_db), current_user: str = Depends(authentication.get_current_user)):
    users = db.query(models.Users).all()

    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(new_user: schemas.User, db: Session = Depends(get_db), current_user: str = Depends(authentication.get_current_user)):


    user = db.query(models.Users).filter(models.Users.email == new_user.email).first()
    if user != None:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED
                            ,detail=f"User {new_user.email} already exists" )
    

    user = models.Users(**(new_user.dict()))
    user.password = utils.hash(user.password)



    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.get("/{id}", response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db), current_user: str = Depends(authentication.get_current_user)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"User ID {id} does not exist" )
    
    return user