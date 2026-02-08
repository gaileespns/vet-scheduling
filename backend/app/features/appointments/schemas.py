"""
Appointment request and response schemas for the Vet Clinic Scheduling System.

This module defines Pydantic schemas for appointment-related API operations:
- AppointmentCreateRequest: Schema for creating a new appointment
- AppointmentUpdateStatusRequest: Schema for updating appointment status
- AppointmentResponse: Schema for appointment responses

Requirements: 5.1, 6.1
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid


class AppointmentCreateRequest(BaseModel):
    """
    Request schema for creating a new appointment.
    
    The end_time is automatically calculated based on the service_type:
    - vaccination: 30 minutes
    - routine: 45 minutes
    - surgery: 120 minutes
    - emergency: 15 minutes
    
    Attributes:
        pet_id: ID of the pet for this appointment (required)
        start_time: When the appointment starts (required, must be in the future)
        service_type: Type of service (required: vaccination, routine, surgery, emergency)
        notes: Optional notes about the appointment
    
    Requirements: 5.1
    """
    pet_id: uuid.UUID = Field(..., description="ID of the pet for this appointment")
    start_time: datetime = Field(..., description="When the appointment starts (must be in the future)")
    service_type: str = Field(..., description="Type of service: vaccination, routine, surgery, or emergency")
    notes: Optional[str] = Field(None, description="Optional notes about the appointment")


class AppointmentUpdateStatusRequest(BaseModel):
    """
    Request schema for updating an appointment's status.
    
    Valid status transitions:
    - pending -> confirmed (admin only)
    - pending -> cancelled (owner or admin)
    - confirmed -> completed (admin only)
    - confirmed -> cancelled (owner or admin)
    
    Invalid transitions:
    - Cannot change status of completed appointments
    - Cannot change status of cancelled appointments
    
    Attributes:
        status: New status (required: confirmed, completed, or cancelled)
    
    Requirements: 6.1
    """
    status: str = Field(..., description="New status: confirmed, completed, or cancelled")


class AppointmentResponse(BaseModel):
    """
    Response schema for appointment data.
    
    Includes all appointment fields with computed end_time based on service_type.
    
    Attributes:
        id: Unique identifier for the appointment
        pet_id: ID of the pet for this appointment
        user_id: ID of the user who booked this appointment
        start_time: When the appointment starts
        end_time: When the appointment ends (calculated based on service_type)
        service_type: Type of service (vaccination, routine, surgery, emergency)
        status: Current status (pending, confirmed, cancelled, completed)
        notes: Optional notes about the appointment
        created_at: Timestamp when the appointment was created
        updated_at: Timestamp when the appointment was last updated
    
    Requirements: 5.1, 6.1
    """
    id: uuid.UUID
    pet_id: uuid.UUID
    user_id: uuid.UUID
    start_time: datetime
    end_time: datetime
    service_type: str
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True
