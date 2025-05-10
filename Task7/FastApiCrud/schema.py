from datetime import date
from typing import Optional
from pydantic import BaseModel


class ResourceCreate(BaseModel):
    resourceName:str

class ResourceResponse(BaseModel):
    resourceId: int
    resourceName: str
    isActive:bool

class BenchResponse(BaseModel):
    resourceId: int
    resourceName: str

class ProjectCreate(BaseModel):
    name: str
    project_manager: int
    end_date: Optional[date] = None
    soft_deadline: Optional[date] = None
    hard_deadline: Optional[date] = None

class ResourceAssignmentCreate(BaseModel):
    projectId: int
    resourceId: int
    onBoard: Optional[date] = None
    offBoard: Optional[date] = None

class AssignedResourceResponse(BaseModel):
    resourceId: int
    resourceName: str
    onBoard: str
    offBoard: str | None

class ProjectResponse(BaseModel):
    id: int
    name: str
    project_manager: int
    project_manager_name:str
    start_date: date
    end_date: Optional[date]
    soft_deadline: Optional[date]
    hard_deadline: Optional[date]
    project_ongoing: bool | None