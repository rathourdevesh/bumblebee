from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .BaseConfig import BaseConfig
from app.db.db import Base
from app.core.constant import UserRole


class User(Base, BaseConfig):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String(15), nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default="user")

    services_created = relationship("Service", foreign_keys="[Service.created_by]", back_populates="created_by_user")
    services_updated = relationship("Service", foreign_keys="[Service.updated_by]", back_populates="updated_by_user")

class Service(Base, BaseConfig):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))

    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="services_created")
    updated_by_user = relationship("User", foreign_keys=[updated_by], back_populates="services_updated")

    sub_services = relationship("SubService", back_populates="service")


class SubService(Base, BaseConfig):
    __tablename__ = "sub_services"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))

    service = relationship("Service", back_populates="sub_services")
    created_by_user = relationship("User", foreign_keys=[created_by])
    updated_by_user = relationship("User", foreign_keys=[updated_by])

class Project(Base, BaseConfig):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    input_links = Column(JSON, nullable=True)
    response_text = Column(String, nullable=True)
    response_links = Column(JSON, nullable=True)
    status_id = Column(Integer, ForeignKey("project_status.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    sub_service_id = Column(Integer, ForeignKey("sub_services.id"))

    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))

    status = relationship("ProjectStatus")
    service = relationship("Service")
    sub_service = relationship("SubService")

class ProjectStatus(Base, BaseConfig):
    __tablename__ = "project_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
