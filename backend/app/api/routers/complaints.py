from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import crud
from app.api import deps
from app.schemas.complaints import ComplaintCreate, ComplaintResponse, ComplaintUpdate
from app.services.email_service import notify_new_complaint

router = APIRouter()

@router.post("/", response_model=ComplaintResponse, status_code=201)
def create_complaint(
    complaint_in: ComplaintCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    complaint = crud.create_complaint(db=db, complaint=complaint_in, user_id=current_user.id)

    # sending email in background so it's faster
    background_tasks.add_task(
        notify_new_complaint,
        complaint_id=complaint.id,
        plate=complaint.plate,
        description=complaint.description,
        incident_time=complaint.date,
        user_email=current_user.email
    )

    return complaint

@router.get("/", response_model=List[ComplaintResponse])
def get_complaints(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """
    get complaints.
    admins see all, officers see theirs.
    """
    if current_user.role == "admin":
        complaints = crud.get_all_complaints(db, skip=skip, limit=limit)
    else:
        complaints = crud.get_complaints_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return complaints

@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(
    complaint_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """get one complaint by id"""
    complaint = crud.get_complaint_by_id(db, complaint_id=complaint_id)

    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # Check if user has permission to view this complaint
    if current_user.role != "admin" and complaint.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this complaint")

    return complaint

@router.put("/{complaint_id}", response_model=ComplaintResponse)
@router.patch("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(
    complaint_id: int,
    complaint_update: ComplaintUpdate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """
    update status.
    admin only.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update complaints")

    complaint = crud.update_complaint(
        db,
        complaint_id=complaint_id,
        status=complaint_update.status,
        admin_note=complaint_update.admin_note
    )

    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    return complaint
