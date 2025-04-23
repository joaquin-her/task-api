from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
DATABASE_URL = config['database']['DATABASE_URL']

app = FastAPI()
db = JsonDataBase("tasks.json")

class Task(BaseModel):
    description:str
    status:str 
    def __str__(self):
        return f"description: {self.description}, status: {self.description}"

@app.get("/")
def get_hello_world():
    return {"message": "Hello world"}

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def post_task(task:Task):
    db.add(task.description)
    return {"response": f"new task '{task.description}' added", "status": 200}

@app.get("/tasks")
def get_tasks():
    tasks = db.getItems()
    return tasks 

@app.get("/tasks/{id}")
def get_task(id:int):
    try:
        task = db.getItem(id)   
        return {"task":task}
    except UnknownIndexException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f"Task with id:{id} not found")
        
@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id:int):
    try:
        db.removeItem(id)   
    except UnknownIndexException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f"Task with id:{id} not found")
    
@app.patch("/tasks/{id}", status_code=status.HTTP_200_OK)
def update_task(id, task:Task):
    try:
        db.updateFromObject(id, task)
    except UnknownIndexException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f"Task with id:{id} not found")
    