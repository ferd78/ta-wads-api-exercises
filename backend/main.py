# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import Optional

# app = FastAPI()

# students = {
#     1 : {
#         "name" : "bol",
#         "age" : 17,
#         "year" : "grade 7"
#     }
# }



# class Student(BaseModel):
#     name: Optional[str] = None
#     age: Optional[int] = None
#     year: Optional[str] = None

# @app.get("/")
# def index():
#     return {"message" : "Hello, World!"}


# #path parameter
# @app.get("/students/{student_id}")
# def get_students(student_id: int):
#     return students[student_id]

# #query parameter -> used for filtering/sorting of the resources

# @app.get("/students")

# def get_students_by_name(name: str):
#     for student_id in students:
#         if students[student_id]["name"] == name:
#             return students[student_id]
#     return {"Error" : "students do not exist"}

# @app.post("/students/new/{student_id}")
# def create_student(student_id: int, student: Student):
#     if student_id in students:
#         return {"Error" : "Student exists"}
#     student[student_id] = student
#     return students[student_id]


# @app.delete("/students/update/{student_id}")
# def update_student(student_id: int, student: Student):
#     if student_id not in students:
#         return {"Error" : "Does not exist"}
    
#     if student.name != None:
#         students[student_id].name = student.name
#     if student.age != None:
#         students[student_id].age = student.age
#     if student.year != None:
#         students[student_id].year = student.year

#     return students[student_id]

# @app.delete("/students/delete/{student_id}")
# def delete_student(student_id: int):
#     if student_id not in students:
#         return {"Error" : "Does not exist"}
#     del students[student_id]
#     return {"Message" : "Deleted succesfully"}
    

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import UUID, uuid4
from fastapi.middleware.cors import CORSMiddleware # import here

app = FastAPI()

# declare origin/s
origins = [
    "http://localhost:5173",
    "localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Task(BaseModel):
    id: int
    title: str
    completed: bool = False  


task_id_count = 0


tasks = {}


@app.post("/createTask")
def create_task(task: Task):
    global task_id_count
    task_id = task_id_count
    task.id = task_id
    tasks[task_id] = task
    task_id_count += 1 
    return task


@app.get("/getTaskById/{task_id}")
def get_task_by_id(task_id: int):
    if task_id in tasks:
        return tasks[task_id]
    else:
        return {"error": "Task not found"}


@app.get("/getTaskByTitle/{title}")
def get_task_by_title(title: str):
    filtered_tasks = [task for task in tasks.values() if task.title == title]
    if filtered_tasks:
        return filtered_tasks
    else:
        return {"error": f"No tasks found with title '{title}'"}


@app.delete("/deleteById/{task_id}")
def delete_task_by_id(task_id: int):
    if task_id in tasks:
        del tasks[task_id]
        return {"message": "Task deleted successfully"}
    else:
        return {"error": "Task not found"}


@app.delete("/deleteByTitle/{title}")
def delete_task_by_title(title: str):
    tasks_to_delete = [task_id for task_id, task in tasks.items() if task.title == title]
    if tasks_to_delete:
        for task_id in tasks_to_delete:
            del tasks[task_id]
        return {"message": f"All tasks with title '{title}' deleted successfully"}
    else:
        return {"error": f"No tasks found with title '{title}'"}

@app.delete("/deleteAll")
def delete_all_tasks():
    tasks.clear()
    return {"message": "All tasks deleted successfully"}

@app.get("/getAllTasks")
def get_all_tasks():
    return list(tasks.values())


@app.put("/updateTask/{task_id}")
def update_task(task_id: int, updated_task: Task):
    if task_id in tasks:
        tasks[task_id] = updated_task
        return {"message": "Task updated successfully"}
    else:
        return {"error": "Task not found"}
    
