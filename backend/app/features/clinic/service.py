"""
Clinic service layer for business logic.

This module implements the business logic for clinic status management including:
- Getting current clinic status (public access)
- Updating clinic status (admin only)

Requirements: 8.1, 8.2
"""

from app.features.clinic.models import ClinicStatus
from app.features.clinic.repository import ClinicStatusRepository


class ClinicService:
    """
    Service layer for clinic status management operations.
    
    This class implements business logic for clinic status operations,
    coordinating between the router layer and repository layer.
    
    The clinic status is publicly accessible (no authentication required for reading),
    but only administrators can update it.
    """
    
    def __init__(self, clinic_status_repo: ClinicStatusRepository):
        """
        Initialize the service with a clinic status repository.
        
        Args:
            clinic_status_repo: ClinicStatusRepository instance for database operations
        """
        self.clinic_status_repo = clinic_status_repo
    
    def get_status(self) -> ClinicStatus:
        """
        Get current clinic status (public endpoint).
        
        This method retrieves the current operational status of the clinic.
        No authentication is required - this is a public endpoint that anyone
        can access to check if the clinic is open.
        
        Returns:
            ClinicStatus object with current status and updated_at timestamp
        
        Requirements: 8.1
        """
        return self.clinic_status_repo.get_current_status()
    
    def update_status(self, new_status: str) -> ClinicStatus:
        """
        Update clinic status (admin only).
        
        This method updates the operational status of the clinic.
        Authorization is handled at the router layer - only admin users
        should be able to call this method.
        
        Args:
            new_status: New status value (open, close, closing_soon)
        
        Returns:
            Updated ClinicStatus object with new status and updated timestamp
        
        Requirements: 8.2
        """
        return self.clinic_status_repo.update_status(new_status)
