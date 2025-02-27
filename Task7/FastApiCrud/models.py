from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date
Base = declarative_base()


class Resource(Base):
    __tablename__ = "resources"
    resourceId = Column(Integer, primary_key=True, index=True,autoincrement=True)
    resourceName = Column(String, nullable=False)
    isActive=Column(Boolean,default=False)



class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String, nullable=False)
    project_manager = Column(Integer, ForeignKey("resources.resourceId"), nullable=False)
    end_date = Column(Date, nullable=True)
    start_date = Column(Date,default=date.today())
    soft_deadline = Column(Date, nullable=True)
    hard_deadline = Column(Date, nullable=True)
    project_ongoing=Column(Boolean,default=True)


class ResourceAssignment(Base):
    __tablename__ = "resource_assignments"

    id = Column(Integer, primary_key=True, index=True)
    projId = Column(Integer, ForeignKey("projects.id"), nullable=False)
    resourceId = Column(Integer, ForeignKey("resources.resourceId"), nullable=False)
    onBoard = Column(Date, nullable=True)
    offBoard = Column(Date, nullable=True)

