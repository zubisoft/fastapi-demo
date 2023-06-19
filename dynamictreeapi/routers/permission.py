from typing import List, Optional

from fastapi import  Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, authentication


router = APIRouter( prefix="/permissions",tags=["Permissions"] )

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_permission(permission_payload: schemas.Permission, db: Session = Depends(get_db)
                         , current_user: int = Depends(authentication.get_current_user)):

    dataset = db.query(models.Permissions).filter(models.Permissions.dataset_id==permission_payload.dataset_id)

    if dataset.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                    ,detail=f"Dataset does not exist")


    permission = db.query(models.Permissions).filter(models.Permissions.user_id == current_user.id).filter(models.Permissions.dataset_id==permission_payload.dataset_id)

 

    if permission_payload.flag==1:

        if permission.first() != None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT
                        ,detail=f"permission already exists" )

        new_permission = models.Permissions(user_id = current_user.id, dataset_id=permission_payload.dataset_id)
        db.add(new_permission)
        db.commit()
        db.refresh(new_permission)

        return new_permission

    elif permission_payload.flag==0:
        
        if permission.first() == None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT
                        ,detail=f"permission does not exist" )

        permission.delete(synchronize_session=False)
        db.commit();
    
        return {"message":"removed permission"}

    return {"message":"no changes applied"}
