from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import admin_required
from app.db.db import get_db_session
from app.models.models import Service, SubService, User
from app.schemas.schemas import ServiceCreate, SubServiceCreate

router = APIRouter()

@router.get("/list")
def list_services(session: Session = Depends(get_db_session)):
    """
    Retrieve all available services and their sub-services from the database.
    """
    services = session.query(Service).all()
    servicesData = []
    for service in services:
        sub_services = session.query(SubService).filter_by(service_id=service.id).all()
        subServicesList = [
            {
                "id": sub_service.id,
                "name": sub_service.name,
                "description": sub_service.description
            }
            for sub_service in sub_services
        ]
        servicesData.append({
            "id": service.id,
            "name": service.name,
            "subServices": subServicesList
        })

    return servicesData


@router.post("/create")
def create_service(
    serviceCreate: ServiceCreate,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(admin_required)
):
    # Create new service
    new_service = Service(
        name=serviceCreate.name,
        description=serviceCreate.description,
        created_by=current_user.id,
        updated_by=current_user.id
    )
    session.add(new_service)
    session.commit()
    session.refresh(new_service)
    return new_service


@router.put("/create/{service_id}")
def update_service(
    service_id: int,
    serviceUpdate: ServiceCreate,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(admin_required)
):
    service = session.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Update fields
    service.name = serviceUpdate.name
    service.description = serviceUpdate.description
    service.updated_by = current_user.id
    
    session.commit()
    return service


@router.post("/sub-services")
def create_sub_service(
    subServCreate: SubServiceCreate,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(admin_required)
):
    # Create new sub-service
    new_sub_service = SubService(
        service_id=subServCreate.service_id,
        name=subServCreate.name,
        description=subServCreate.description,
        created_by=current_user.id,
        updated_by=current_user.id
    )
    session.add(new_sub_service)
    session.commit()
    session.refresh(new_sub_service)
    return new_sub_service


@router.put("/sub-services/{sub_service_id}")
def update_sub_service(
    sub_service_id: int,
    name: str,
    description: str,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(admin_required)
):
    # Find the sub-service
    sub_service = session.query(SubService).filter(SubService.id == sub_service_id).first()
    if not sub_service:
        raise HTTPException(status_code=404, detail="Sub-Service not found")
    
    # Update fields
    sub_service.name = name
    sub_service.description = description
    sub_service.updated_by = current_user.id
    
    session.commit()
    return sub_service

