"""
Common enums for the Vet Clinic Scheduling System.

This module defines all enumeration types used throughout the application
for user roles, appointment statuses, service types, clinic status, and
vaccination status.
"""

from enum import Enum


class UserRole(str, Enum):
    """User role enumeration.
    
    Defines the two types of users in the system:
    - ADMIN: Clinic owner with full system access
    - PET_OWNER: Customer who can manage their own pets and appointments
    """
    ADMIN = "admin"
    PET_OWNER = "pet_owner"


class AppointmentStatus(str, Enum):
    """Appointment status enumeration.
    
    Defines the lifecycle states of an appointment:
    - PENDING: Initial state when appointment is created
    - CONFIRMED: Admin has confirmed the appointment
    - CANCELLED: Appointment has been cancelled
    - COMPLETED: Appointment has been completed
    """
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class ServiceType(str, Enum):
    """Service type enumeration.
    
    Defines the types of veterinary services available:
    - VACCINATION: Vaccination service (30 minutes)
    - ROUTINE: Routine checkup (45 minutes)
    - SURGERY: Surgical procedure (120 minutes)
    - EMERGENCY: Emergency service (15 minutes)
    """
    VACCINATION = "vaccination"
    ROUTINE = "routine"
    SURGERY = "surgery"
    EMERGENCY = "emergency"


class ClinicStatusEnum(str, Enum):
    """Clinic operational status enumeration.
    
    Defines the operational states of the clinic:
    - OPEN: Clinic is open and accepting appointments
    - CLOSE: Clinic is closed, no new appointments allowed
    - CLOSING_SOON: Clinic is closing soon
    """
    OPEN = "open"
    CLOSE = "close"
    CLOSING_SOON = "closing_soon"


class VaccinationStatus(str, Enum):
    """Vaccination status enumeration.
    
    Defines the validity states of a pet's vaccination:
    - VALID: Vaccination is current (within 365 days)
    - EXPIRED: Vaccination has expired (more than 365 days ago)
    - UNKNOWN: No vaccination date recorded
    """
    VALID = "valid"
    EXPIRED = "expired"
    UNKNOWN = "unknown"
