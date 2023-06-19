from fastapi import FastAPI, Depends

from . import models, database
from .database import  engine, get_db
from sqlalchemy.orm import Session

from .routers import dataset, user, auth, permission

from .config import settings

from fastapi.middleware.cors import CORSMiddleware


#Initialize SQLAlchemy Models
#models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(dataset.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(permission.router)
     
@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": "Root"}





#TO RUN: 
# conda activate .condaenv
# conda activate ./.condaenv 
# uvicorn dynamic-tree-api.main:app
