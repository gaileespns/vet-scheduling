"""
Appointment router for API endpoints.

This module implements the HTTP endpoints for appointment management:
- POST /api/v1/appointments: Create a new appointment
- GET /api/v1/appointments: List appointments with filters (status, from_date, to_date)
- PATCH /api/v1/appointments/{appointment_id}/status: Update appointment status (admin only)
- DELETE /api/v1/appointments/{appointment_id}: Cancel/delete an appointment

All endpoints require authentication. Pet owners can only access appointments for
their own pets, while admins can access all appointments.

Requirements: 5.1, 6.1, 7.1, 7.3, 7.4, 7.5
"""

from fastapi import APIRouter, Depends, status, Query
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime
import uuid

from app.core.database import get_session
from app.common.dependencies import get_current_user, require_role
from app.features.users.models import User
from app.features.appointments.schemas import (
    AppointmentCreateRequest,
    AppointmentUpdateStatusRequest,
    AppointmentResponse
)
from app.features.appointments.repository import AppointmentRepository
from app.features.appointments.service import AppointmentService
from app.features.pets.repository import PetRepository
from app.features.clinic.repository import ClinicStatusRepository


router = APIRouter(prefix="/api/v1/appointments", tags=["Appointments"])


@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(
    request: AppointmentCreateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> AppointmentResponse:
    """
    Create a new appointment.
    
    The appointment is validated against business rules:
    - Pet must exist and be owned by the user (or user is admin)
    - Start time must be in the future
    - Clinic must not be closed
    - Time slot must not overlap with existing pending/confirmed appointments
    - End time is automatically calculated based on service type
    
    The created appointment has status "pending".
    
    Args:
        request: Appointment creation request data
        current_user: Authenticated user (from JWT token)
        session: Database session
        
    Returns:
        Created appointment
        
    Raises:
        401: If authentication fails
        403: If pet owner tries to book for another user's pet
        404: If pet doesn't exist
        400: If validation fails (past time, clinic closed, overlap)
        422: If request data is invalid
        
    Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.10, 5.11, 5.12
    """
    appointment_repo = AppointmentRepository(session)
    pet_repo = PetRepository(session)
    clinic_status_repo = ClinicStatusRepository(session)
    
    appointment_service = AppointmentService(
        appointment_repo, pet_repo, clinic_status_repo
    )
    
    appointment = appointment_service.create_appointment(
        pet_id=request.pet_id,
        start_time=request.start_time,
        service_type=request.service_type,
        notes=request.notes,
        current_user=current_user
    )
    
    session.commit()
    return AppointmentResponse.model_validate(appointment)


@router.get("", response_model=List[AppointmentResponse])
def get_appointments(
    status: Optional[str] = Query(None, description="Filter by appointment status"),
    from_date: Optional[datetime] = Query(None, description="Filter appointments starting on or after this date"),
    to_date: Optional[datetime] = Query(None, description="Filter appointments starting on or before this date"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> List[AppointmentResponse]:
    """
    Get appointments with optional filters.
    
    - Admin users: Returns all appointments in the system
    - Pet owners: Returns only appointments for pets owned by the authenticated user
    
    Supports filtering by:
    - status: Filter by appointment status (pending, confirmed, cancelled, completed)
    - from_date: Only appointments starting on or after this date
    - to_date: Only appointments starting on or before this date
    
    Multiple filters can be combined.
    
    Args:
        status: Optional status filter
        from_date: Optional start date filter
        to_date: Optional end date filter
        current_user: Authenticated user (from JWT token)
        session: Database session
        
    Returns:
        List of appointments matching the filters
        
    Raises:
        401: If authentication fails
        
    Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6
    """
    appointment_repo = AppointmentRepository(session)
    pet_repo = PetRepository(session)
    clinic_status_repo = ClinicStatusRepository(session)
    
    appointment_service = AppointmentService(
        appointment_repo, pet_repo, clinic_status_repo
    )
    
    appointments = appointment_service.get_appointments(
        current_user=current_user,
        status=status,
        from_date=from_date,
        to_date=to_date
    )
    
    return [AppointmentResponse.model_validate(apt) for apt in appointments]


@router.patch("/{appointment_id}/status", response_model=AppointmentResponse)
def update_appointment_status(
    appointment_id: uuid.UUID,
    request: AppointmentUpdateStatusRequest,
    current_user: User = Depends(require_role(["admin"])),
    session: Session = Depends(get_session)
) -> AppointmentResponse:
    """
    Update appointment status (admin only).
    
    This endpoint is restricted to admin users only. Admins can:
    - Confirm pending appointments (pending -> confirmed)
    - Complete confirmed appointments (confirmed -> completed)
    - Cancel appointments (any status -> cancelled, except completed)
    
    Status transition rules:
    - Cannot change status of completed appointments
    - Cannot change status of cancelled appointments
    - Cannot cancel completed appointments
    
    Args:
        appointment_id: UUID of the appointment to update
        request: Status update request data
        current_user: Authenticated admin user (from JWT token)
        session: Database session
        
    Returns:
        Updated appointment
        
    Raises:
        401: If authentication fails
        403: If user is not an admin
        404: If appointment doesn't exist
        400: If status transition is invalid
        422: If request data is invalid
        
    Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6
    """
    appointment_repo = AppointmentRepository(session)
    pet_repo = PetRepository(session)
    clinic_status_repo = ClinicStatusRepository(session)
    
    appointment_service = AppointmentService(
        appointment_repo, pet_repo, clinic_status_repo
    )
    
    appointment = appointment_service.update_appointment_status(
        appointment_id=appointment_id,
        new_status=request.status,
        current_user=current_user
    )
    
    session.commit()
    return AppointmentResponse.model_validate(appointment)


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_appointment(
    appointment_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> None:
    """
    Cancel/delete an appointment.
    
    - Admin users: Can cancel any appointment
    - Pet owners: Can only cancel appointments for their own pets
    
    Cannot cancel completed appointments.
    
    Args:
        appointment_id: UUID of the appointment to cancel
        current_user: Authenticated user (from JWT token)
        session: Database session
        
    Returns:
        No content (204 status code)
        
    Raises:
        401: If authentication fails
        403: If pet owner tries to cancel another user's appointment
        404: If appointment doesn't exist
        400: If trying to cancel a completed appointment
        
    Requirements: 6.7, 6.8, 6.9, 6.10
    """
    appointment_repo = AppointmentRepository(session)
    pet_repo = PetRepository(session)
    clinic_status_repo = ClinicStatusRepository(session)
    
    appointment_service = AppointmentService(
        appointment_repo, pet_repo, clinic_status_repo
    )
    
    appointment_service.cancel_appointment(appointment_id, current_user)
    
    session.commit()
