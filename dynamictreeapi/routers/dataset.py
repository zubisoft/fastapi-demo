from typing import List, Optional

from fastapi import  Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from .. import models, schemas, authentication


router = APIRouter( prefix="/datasets",tags=["Datasets"] )

@router.get("/",response_model=List[schemas.DatasetResponseExt])
async def get_datasets(db: Session = Depends(get_db), current_user: str = Depends(authentication.get_current_user)
                       , limit: Optional[int]=10
                       , search_title: Optional[str]=""):
    
    # datasets = db.query(models.Dataset, func.count(models.Permissions.dataset_id).label("num users with access"))\
    #     .filter(models.Dataset.name.contains(search_title))\
    #     .join(models.Permissions, models.Permissions.dataset_id == models.Dataset.id, isouter=True)\
    #     .group_by(models.Dataset.id)\
    #     .limit(limit).all()
    
    # datasets = db.query(models.Dataset, func.count(models.Permissions.dataset_id))\
    #     .filter(models.Dataset.name.contains(search_title))\
    #     .join(models.Permissions, models.Permissions.dataset_id == models.Dataset.id, isouter=True)\
    #     .group_by(models.Dataset.id)\
    #     .limit(limit)

    datasets = db.query(models.Dataset,func.count(models.Permissions.dataset_id).label("num"))\
        .filter(models.Dataset.name.contains(search_title))\
        .join(models.Permissions, models.Permissions.dataset_id == models.Dataset.id, isouter=True)\
        .group_by(models.Dataset.id)\
        .limit(limit)
    
    print(datasets)
    print(datasets.all())

    return datasets.all()

@router.get("/{id}", response_model=schemas.DatasetResponse)
async def get_dataset(id: int, db: Session = Depends(get_db), current_user: str = Depends(authentication.get_current_user)):
    dataset = db.query(models.Dataset).filter(models.Dataset.id == id).first()
    if dataset == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"dataset ID {id} does not exist" )
    
    return dataset

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dataset(id: int, db: Session = Depends(get_db), current_user: str = Depends(authentication.get_current_user)):

    
    dataset = db.query(models.Dataset).filter(models.Dataset.id == id)
    
    if dataset.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"dataset ID {id} does not exist" )
    
    if dataset.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN
                            ,detail=f"The user is not authorized to delete Dataset ID {id}" )

    dataset.delete(synchronize_session=False)

    db.commit();

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DatasetResponse)
async def create_dataset(dataset: schemas.Dataset, db: Session = Depends(get_db)
                         , current_user: int = Depends(authentication.get_current_user)):

    print(current_user)
    new_dataset = models.Dataset(owner_id = current_user.id, **(dataset.dict()))
    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)
    return new_dataset


@router.put("/{id}", response_model=schemas.DatasetResponse)
async def replace_dataset(id: int, dataset: schemas.Dataset, db: Session = Depends(get_db), current_user: str = Depends(authentication.get_current_user)):

    update_dataset = db.query(models.Dataset).filter(models.Dataset.id == id)

    if update_dataset.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"dataset ID {id} does not exist" )
    

    if update_dataset.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN
                            ,detail=f"The user is not authorized to edit Dataset ID {id}" )
 
    update_dataset.update(dataset.dict())
    db.commit()


    return update_dataset.first()