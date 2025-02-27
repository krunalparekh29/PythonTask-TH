from datetime import datetime
from typing import List,Optional

from datetime import date
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import get_db,engine
from models import Resource,Project,ResourceAssignment
import schema



app=FastAPI()

# @app.on_event("startup")
# def on_startup():
#     print("Application started.")
#     models.Base.metadata.create_all(bind=engine)




@app.post("/resources/",response_model=dict)
def create_resource(resource:schema.ResourceCreate,db:Session=Depends(get_db)):
    existing_resource = db.query(Resource).filter(Resource.resourceName == resource.resourceName).first()
    if existing_resource:
        raise HTTPException(status_code=400, detail="Resource already exists")
    db_resource= Resource(**resource.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return {"message":"Resource created successfully","resource":{
        "name": db_resource.resourceName,
    }}

@app.get("/resources/",response_model=List[schema.ResourceResponse])
def get_resources(db: Session = Depends(get_db)):
    resources = db.query(Resource).all()
    return resources


@app.delete("/resources/{resource_id}", response_model=dict)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resources = db.query(Resource).filter(Resource.resourceId == resource_id).first()
    if not resources:
        raise HTTPException(status_code=404, detail="Resource not found")
    resources.isActive = False
    db.commit()
    return {"message": "Resource deleted successfully", "resourceId": resource_id}


@app.get("/resources/{resource_id}", response_model=schema.ResourceResponse)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resources = db.query(Resource).filter(Resource.resourceId == resource_id).first()
    if not resources:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resources


@app.post("/projects/", response_model=dict)
def create_project(project: schema.ProjectCreate, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(
        Resource.resourceId == project.project_manager,
        Resource.isActive == False
    ).first()
    if not resource:
        raise HTTPException(status_code=400, detail="Project manager not found or is inactive")
    resource.isActive=True
    db_project = Project(
        name=project.name,
        project_manager=project.project_manager,
        end_date=project.end_date,
        start_date=date.today(),
        soft_deadline=project.soft_deadline,
        hard_deadline=project.hard_deadline
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    resource_allocation = ResourceAssignment(
        resourceId=project.project_manager,
        projId=db_project.id,
        onBoard=date.today()
    )
    db.add(resource_allocation)
    db.commit()
    return {
        "message": "Project created successfully",
        "project": {
            "id": db_project.id,
            "name": db_project.name,
            "project_manager": db_project.project_manager,
            "end_date": db_project.end_date,
            "start_date": db_project.start_date,
            "soft_deadline": db_project.soft_deadline,
            "hard_deadline": db_project.hard_deadline
        }
    }

@app.post("/resource_assignments/", response_model=dict)
def allocate_resource(assignment: schema.ResourceAssignmentCreate, db: Session = Depends(get_db)):

    project = db.query(Project).filter(Project.id == assignment.projectId).first()
    if not project:
        raise HTTPException(status_code=400, detail="Project not found")

    resource = db.query(Resource).filter(Resource.resourceId == assignment.resourceId).first()
    if not resource:
        raise HTTPException(status_code=400, detail="Resource not found")
    resource.isActive = True

    db_assignment = ResourceAssignment(
        projId=assignment.projectId,
        resourceId=assignment.resourceId,
        onBoard=date.today(),
        offBoard=assignment.offBoard
    )

    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)

    return {
        "message": "Resource allocated successfully",
        "assignment": {
            "id": db_assignment.id,
            "projId": db_assignment.projId,
            "resourceId": db_assignment.resourceId,
            "onBoard": db_assignment.onBoard,
            "offBoard": db_assignment.offBoard
        }
    }

@app.get("/projects/", response_model=List[schema.ProjectResponse])
def get_all_projects(db: Session = Depends(get_db)):
    projects = (
        db.query(Project, Resource.resourceName)
        .join(Resource, Project.project_manager == Resource.resourceId)
        .filter(Project.project_ongoing == True)
        .all() )
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found")
    return [
        {
            "id": project.id,
            "name": project.name,
            "project_manager": project.project_manager,
            "project_manager_name": resource_name,
            "start_date": project.start_date,
            "end_date": project.end_date,
            "soft_deadline": project.soft_deadline,
            "hard_deadline": project.hard_deadline,
            "project_ongoing":project.project_ongoing
        }
        for project, resource_name in projects
    ]

@app.put("/projects/{id}/complete", response_model=dict)
def project_completion(id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.project_ongoing = False
    project.end_date = date.today()

    assigned_resources = db.query(ResourceAssignment).filter(ResourceAssignment.projId == id).all()

    for assignment in assigned_resources:
        assignment.offBoard = date.today()

        active_assignments = (
            db.query(ResourceAssignment)
            .join(Project, Project.id == ResourceAssignment.projId)
            .filter(
                ResourceAssignment.resourceId == assignment.resourceId,
                Project.project_ongoing == True
            )
            .count()
        )
        resource = db.query(Resource).filter(Resource.resourceId == assignment.resourceId).first()
        if resource and active_assignments == 0:
            resource.isActive = False
    db.commit()
    return {
        "message": "Project marked as completed, relevant resources updated",
        "project_id": id
    }


@app.get("/on_bench/", response_model=List[schema.BenchResponse])
def get_bench_resources(db: Session = Depends(get_db)):
    bench_resources = db.query(Resource).filter(Resource.isActive == False).all()
    if not bench_resources:
        raise HTTPException(status_code=404, detail="No one on bench")
    return [
        {
            "resourceId": resource.resourceId,
            "resourceName": resource.resourceName,
        }
        for resource in bench_resources
    ]

