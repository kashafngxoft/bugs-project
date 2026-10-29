
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Application Debugging Demo API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    status: str = "Open"
    priority: str = "Medium"


tasks = [
    {
        "id": 1,
        "title": "Fix API error handling",
        "status": "In Progress",
        "priority": "High",
    },
    {
        "id": 2,
        "title": "Add dashboard filters",
        "status": "Open",
        "priority": "Medium",
    },
    {
        "id": 3,
        "title": "Test form validation",
        "status": "Completed",
        "priority": "Low",
    },
]


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "FastAPI"}


@app.get("/api/tasks")
def get_tasks(search: str = "", status: str = "All"):
    results = tasks.copy()

    if search.strip():
        results = [
            task for task in results
            if search.lower() in task["title"].lower()
        ]

    if status != "All":
        results = [
            task for task in results
            if task["status"] == status
        ]

    return {"items": results, "total": len(results)}


@app.post("/api/tasks", status_code=201)
def create_task(task: TaskCreate):
    if task.status not in ["Open", "In Progress", "Completed"]:
        raise HTTPException(400, "Invalid task status")

    if task.priority not in ["Low", "Medium", "High"]:
        raise HTTPException(400, "Invalid priority")

    new_task = {
        "id": max((item["id"] for item in tasks), default=0) + 1,
        **task.model_dump(),
    }
    tasks.append(new_task)
    return new_task


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    raise HTTPException(404, "Task not found")
