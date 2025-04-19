from fastapi import FastAPI
from DataBase import JsonDataBase
from pydantic import BaseModel

app = FastAPI()
db = JsonDataBase("tasks.json")

class Task(BaseModel):
    description:str
    status:str 
    def __str__(self):
        return f"description: {self.description}, status: {self.description}"

@app.get("/")
def root():
    return {"message": "Hello world"}

@app.post("/tasks")
def post_task(task:Task):
    db.add(task.description)
    return {"response": f"new task '{task.description}' added", "status": 200}

@app.get("/tasks")
def get_tasks():
    tasks = db.getItems()
    return tasks 

@app.get("/tasks/{id}")
def get_task(id:int):
    task = db.getItem(id)
    return {"data":task}
