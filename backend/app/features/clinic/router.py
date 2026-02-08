"""
Clinic router for API endpoints.

This module implements the HTTP endpoints for clinic status management:
- GET /api/v1/clinic/status: Get current clinic status (public, no auth required)
- PATCH /api/v1/clinic/status: Update clinic status (admin-only)

The GET endpoint is public to allow anyone to check if the clinic is open.
The PATCH endpoint requires admin authentication to update the status.

Requirements: 8.1, 8.2, 8.3
"""

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.common.dependencies import require_role
from app.features.users.models import User
from app.features.clinic.schemas import ClinicStatusResponse, ClinicStatusUpdateRequest
from app.features.clinic.repository import ClinicStatusRepository
from app.features.clinic.service import ClinicService


router = APIRouter(prefix="/api/v1/clinic", tags=["Clinic"])


@router.get("/status", response_model=ClinicStatusResponse)
def get_clinic_status(
    session: Session = Depends(get_session)
) -> ClinicStatusResponse:
    """
    Get clinic status (public endpoint, no auth required).
    
    This endpoint is publicly accessible without authentication, allowing
    anyone to check the current operational status of the clinic.
    
    Args:
        session: Database session
        
    Returns:
        Current clinic status and last updated timestamp
        
    Example Response:
        {
            "status": "open",
            "updated_at": "2024-01-15T10:30:00Z"
        }
        
    Requirements: 8.1
    """
    clinic_status_repo = ClinicStatusRepository(session)
    clinic_service = ClinicService(clinic_status_repo)
    
    clinic_status = clinic_service.get_status()
    
    return ClinicStatusResponse.model_validate(clinic_status)


@router.patch("/status", response_model=ClinicStatusResponse)
def update_clinic_status(
    request: ClinicStatusUpdateRequest,
    current_user: User = Depends(require_role(["admin"])),
    session: Session = Depends(get_session)
) -> ClinicStatusResponse:
    """
    Update clinic status (admin only).
    
    This endpoint allows administrators to change the operational status
    of the clinic. Only users with the "admin" role can access this endpoint.
    
    Valid status values:
    - "open": Clinic is open for appointments
    - "close": Clinic is closed, no new appointments can be created
    - "closing_soon": Clinic is closing soon
    
    Args:
        request: Clinic status update request with new status
        current_user: Authenticated admin user (from JWT token)
        session: Database session
        
    Returns:
        Updated clinic status and timestamp
        
    Raises:
        401: If authentication fails
        403: If user is not an admin
        422: If request data is invalid
        
    Example Request:
        {
            "status": "close"
        }
        
    Example Response:
        {
            "status": "close",
            "updated_at": "2024-01-15T10:35:00Z"
        }
        
    Requirements: 8.2, 8.3
    """
    clinic_status_repo = ClinicStatusRepository(session)
    clinic_service = ClinicService(clinic_status_repo)
    
    clinic_status = clinic_service.update_status(request.status)
    
    session.commit()
    
    return ClinicStatusResponse.model_validate(clinic_status)
