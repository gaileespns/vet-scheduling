"""
Common utilities and shared components for the Vet Clinic Scheduling System.

This package contains enums, exceptions, dependencies, and utility functions
that are used across multiple features in the application.
"""

from .enums import (
    UserRole,
    AppointmentStatus,
    ServiceType,
    ClinicStatusEnum,
    VaccinationStatus,
)

__all__ = [
    "UserRole",
    "AppointmentStatus",
    "ServiceType",
    "ClinicStatusEnum",
    "VaccinationStatus",
]
