"""
Appointment request and response schemas for the Vet Clinic Scheduling System.

This module defines Pydantic schemas for appointment-related API operations:
- AppointmentCreateRequest: Schema for creating a new appointment
- AppointmentUpdateStatusRequest: Schema for updating appointment status
- AppointmentReschedule: Schema for rescheduling an appointment
- AppointmentResponse: Schema for appointment responses

Requirements: 5.1, 6.1, 6.2
"""

from pydantic import BaseModel, Field, field_validator
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


class AppointmentReschedule(BaseModel):
    """
    Request schema for rescheduling an appointment.
    
    Both start_time and end_time are required. The end_time must be after
    the start_time to ensure a valid time range.
    
    Attributes:
        start_time: New start time for the appointment (required)
        end_time: New end time for the appointment (required, must be after start_time)
    
    Requirements: 6.2
    """
    start_time: datetime = Field(..., description="New start time for the appointment")
    end_time: datetime = Field(..., description="New end time for the appointment")
    
    @field_validator('end_time')
    @classmethod
    def end_after_start(cls, v: datetime, info) -> datetime:
        """
        Validate that end_time is after start_time.
        
        Args:
            v: The end_time value to validate
            info: Validation context containing other field values
            
        Returns:
            The validated end_time value
            
        Raises:
            ValueError: If end_time is not after start_time
        """
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time must be after start_time')
        return v


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
