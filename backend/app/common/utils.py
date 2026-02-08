"""
Utility functions for the Vet Clinic Scheduling System.

This module provides helper functions for common operations including:
- Service duration calculations
- Vaccination status computation
"""

from datetime import datetime, timedelta
from typing import Optional

from app.common.enums import VaccinationStatus


# Service duration constants (in minutes)
# Requirements: 5.6, 5.7, 5.8, 5.9
SERVICE_DURATIONS = {
    "vaccination": 30,
    "routine": 45,
    "surgery": 120,
    "emergency": 15
}


def calculate_end_time(start_time: datetime, service_type: str) -> datetime:
    """
    Calculate appointment end time based on service type.
    
    The end time is computed by adding the service duration to the start time.
    Service durations are:
    - vaccination: 30 minutes
    - routine: 45 minutes
    - surgery: 120 minutes
    - emergency: 15 minutes
    
    Args:
        start_time: The appointment start time
        service_type: The type of service (vaccination, routine, surgery, emergency)
    
    Returns:
        The calculated end time as a datetime object
    
    Requirements: 5.5
    """
    duration_minutes = SERVICE_DURATIONS.get(service_type, 30)
    return start_time + timedelta(minutes=duration_minutes)


def get_vaccination_status(last_vaccination: Optional[datetime]) -> str:
    """
    Compute vaccination status based on last vaccination date.
    
    The vaccination status is determined as follows:
    - If last_vaccination is None: returns "unknown"
    - If last_vaccination is more than 365 days ago: returns "expired"
    - If last_vaccination is 365 days or less ago: returns "valid"
    
    Args:
        last_vaccination: The date of the pet's last vaccination, or None if unknown
    
    Returns:
        The vaccination status as a string: "valid", "expired", or "unknown"
    
    Requirements: 4.1, 4.2, 4.3
    """
    if not last_vaccination:
        return VaccinationStatus.UNKNOWN.value
    
    # Use timezone-aware datetime for comparison
    # If last_vaccination is naive (no timezone), treat it as UTC
    now = datetime.utcnow()
    one_year_ago = now - timedelta(days=365)
    
    if last_vaccination < one_year_ago:
        return VaccinationStatus.EXPIRED.value
    else:
        return VaccinationStatus.VALID.value
