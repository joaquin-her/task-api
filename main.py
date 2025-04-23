from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
DATABASE_URL = config['database']['DATABASE_URL']

app = FastAPI()

class Task(BaseModel):
    description:str
    status:str 
    def __str__(self):
        return f"description: {self.description}, status: {self.description}"

@app.get("/")
def get_hello_world():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            return {"message": "Hello world", "database-status":"Succesfull connection"}

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def post_task(task:Task):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""INSERT INTO tasks (description) VALUES (%s) RETURNING *;""", (task.description,))
            added_task = cursor.fetchone()
            conn.commit()
            return {"response": f"new task '{added_task}' added", "status": 200}
    return {"response": f"new task '{task.description}' failed to add", "status": 500}

@app.get("/tasks")
def get_tasks():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM tasks ORDER BY task_id ASC LIMIT 100;""")
            tasks = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            result = [dict(zip(column_names, row)) for row in tasks]
            return {"tasks":result} 
        return {"response": "failed to get tasks", "status": 500}

@app.get("/tasks/{id}")
def get_task(id:int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM tasks WHERE task_id = %s ;""", (str(id),))
            requested_task = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]
    if requested_task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f"Task with id:{id} not found")
    result = dict(zip(column_names, requested_task))            
    return {"data": result}
        
@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id:int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""DELETE FROM tasks WHERE task_id = %s RETURNING *;""", (str(id),))
            deleted_task = cursor.fetchone()
    if deleted_task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f"Task with id:{id} not found")
    
@app.patch("/tasks/{id}", status_code=status.HTTP_200_OK)
def update_task(id, task:Task):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""UPDATE tasks SET description = %s, status = %s WHERE task_id = %s RETURNING *;""", (task.description, task.status, str(id)))
            patched_task = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]
    if patched_task == None:        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f"Task with id:{id} not found")
    patched_task = dict(zip(column_names, patched_task))
    return {"data":patched_task}
    