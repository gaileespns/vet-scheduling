"""
Clinic status request and response schemas for the Vet Clinic Scheduling System.

This module defines Pydantic schemas for clinic status management:
- ClinicStatusResponse: Schema for clinic status responses
- ClinicStatusUpdateRequest: Schema for updating clinic status

Requirements: 8.1, 8.2
"""

from pydantic import BaseModel, Field
from datetime import datetime


class ClinicStatusResponse(BaseModel):
    """
    Response schema for clinic status.
    
    Returns the current operational status of the clinic and when it was last updated.
    This endpoint is public and does not require authentication.
    
    Attributes:
        status: Current operational status (open, close, closing_soon)
        updated_at: Timestamp when the status was last updated
    
    Requirements: 8.1
    """
    status: str = Field(..., description="Current operational status: open, close, or closing_soon")
    updated_at: datetime = Field(..., description="Timestamp when the status was last updated")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ClinicStatusUpdateRequest(BaseModel):
    """
    Request schema for updating clinic status.
    
    Allows administrators to change the operational status of the clinic.
    Only admin users can update the clinic status.
    
    Attributes:
        status: New operational status (open, close, closing_soon)
    
    Requirements: 8.2
    """
    status: str = Field(..., description="New operational status: open, close, or closing_soon")
