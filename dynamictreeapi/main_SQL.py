from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class Dataset(BaseModel):
    type: str
    name: str
    data: str
    url: Optional[str] = None


while True:
    try:
        conn = psycopg2.connect(host="localhost",dbname="fastapi", user="postgres", password="VotoNulo2023",cursor_factory=RealDictCursor)
        cur = conn.cursor()

        print("Connected to Database")
        break
    except Exception as error:
        print(error)
        time.sleep(10)


app = FastAPI()

datasets_db = [{"id":1,"type":"raw_data", "name":"apito", "data":"commander", "url":None}]

def find_dataset(id):
    for d in datasets_db:
        if d['id'] == id:
            return d

def find_index_dataset(id):
    i = 0
    for d in datasets_db:
        if d['id'] == id:
            return i
        i=i+1
        
@app.get("/")
async def root():
    return {"message": "Root"}

@app.get("/datasets")
async def get_datasets():
    cur.execute("""select * from datasets""")
    result = cur.fetchall();
    print(result)
    return {"message": result}

@app.get("/datasets/{id}")
async def get_dataset(id: int):

    dataset = find_dataset(id)
    if dataset == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"dataset ID {id} does not exist" )
    
    return {"message": dataset}

@app.delete("/datasets/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dataset(id: int):

    
    cur.execute("""
        delete from datasets
        where id = %s
        RETURNING *
        """, (str(id),))
    deleted_dataset =  cur.fetchone
    
    if deleted_dataset == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"dataset ID {id} does not exist" )
    
    conn.commit();

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/datasets")
async def create_dataset(dataset: Dataset):

    cur.execute("""
        insert into datasets (type,name,data)
        values (%s,%s,%s)
        RETURNING *
        """, (dataset.type, dataset.name, dataset.data))

    conn.commit();

    return {"new post": cur.fetchone()}


@app.put("/datasets/{id}")
async def replace_dataset(id: int, dataset: Dataset):

    cur.execute("""
        UPDATE datasets 
        set type=%s,name=%s,data=%s
        where id=%s
        RETURNING *
        """, (dataset.type, dataset.name, dataset.data,id)
    )

    conn.commit()

    updated_dataset =  cur.fetchone

    if updated_dataset == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"dataset ID {id} does not exist" )
 

    return {"data": updated_dataset}

#@app.post("/datasets")
#async def send_data(payload: dict = Body(...)):

#Receive RAW data, no particular structure
#@app.post("/datasets")
#async def send_data(payload: dict = Body(...)):
#    print(payload)
#    return {"new training data": f"title {payload['title']} content:{payload['content']}"}

#TO RUN: 
# conda activate .condaenv
# conda activate ./.condaenv 
# uvicorn dynamic-tree-api.main:app
