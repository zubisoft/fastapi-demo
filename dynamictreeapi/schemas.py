from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    email: EmailStr
    id: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
 

class Dataset(BaseModel):
    type: str
    name: str
    data: str
    url: Optional[str] = None
    

class DatasetCreate(Dataset):
    pass

class DatasetResponse(BaseModel):
    id: str
    type: str
    name: str
    created_date: datetime
    owner_id: str
    owner: UserResponse

    class Config:
        orm_mode = True

class DatasetResponseExt(BaseModel):
    Dataset: DatasetResponse
    num: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class Permission(BaseModel):
    dataset_id: str
    flag: conint(le=1, ge=0)

class PermissionResponse(BaseModel):
    dataset_id: str
    user_id: str