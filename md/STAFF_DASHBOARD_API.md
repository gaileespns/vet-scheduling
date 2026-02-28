# Staff Dashboard API Documentation

## Overview
This document details all API endpoints needed for the staff dashboard improvements.

---

## Existing Endpoints (Already Available)

### 1. Get All Appointments
**Endpoint:** `GET /api/v1/appointments`
**Auth:** Required (Admin sees all, clients see only their own)
**Query Parameters:**
- `status` (optional): Filter by status (pending, confirmed, completed, cancelled)
- `from_date` (optional): Filter appointments from this date
- `to_date` (optional): Filter appointments until this date

**Response:**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "pet_id": "123e4567-e89b-12d3-a456-426614174001",
    "user_id": "123e4567-e89b-12d3-a456-426614174002",
    "start_time": "2026-03-04T10:00:00",
    "end_time": "2026-03-04T10:45:00",
    "service_type": "Routine Check-up",
    "status": "pending",
    "notes": "First visit",
    "created_at": "2026-03-01T08:00:00",
    "updated_at": "2026-03-01T08:00:00"
  }
]
```

### 2. Update Appointment Status
**Endpoint:** `PATCH /api/v1/appointments/{appointment_id}/status`
**Auth:** Required (Admin only)
**Request Body:**
```json
{
  "status": "confirmed"
}
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "confirmed",
  "updated_at": "2026-03-01T09:00:00"
}
```

### 3. Get Available Time Slots
**Endpoint:** `GET /api/v1/appointments/available-slots`
**Auth:** Not required
**Query Parameters:**
- `date` (required): Date in YYYY-MM-DD format
- `service_type` (optional): Type of service (default: "routine")

**Response:**
```json
[
  {
    "start_time": "2026-03-04T08:00:00",
    "end_time": "2026-03-04T08:45:00"
  },
  {
    "start_time": "2026-03-04T08:30:00",
    "end_time": "2026-03-04T09:15:00"
  }
]
```

### 4. Get All Pets
**Endpoint:** `GET /api/v1/pets`
**Auth:** Required (Admin sees all, clients see only their own)

**Response:**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174001",
    "user_id": "123e4567-e89b-12d3-a456-426614174002",
    "name": "Max",
    "species": "dog",
    "breed": "Golden Retriever",
    "date_of_birth": "2020-05-15",
    "sex": "male",
    "notes": "Friendly, loves treats",
    "last_vaccination": "2025-12-01",
    "created_at": "2025-01-15T10:00:00"
  }
]
```

### 5. Get User Profile
**Endpoint:** `GET /api/v1/users/profile`
**Auth:** Required

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174002",
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+63 917 123 4567",
  "city": "Manila",
  "role": "pet_owner",
  "is_active": true,
  "preferences": null,
  "created_at": "2025-01-01T00:00:00"
}
```

---

## New Endpoints Needed

### 1. Get All Users (Admin Only)
**Endpoint:** `GET /api/v1/users`
**Auth:** Required (Admin only)
**Purpose:** Staff needs to see pet owner names for appointments

**Implementation Required:**
```python
# File: backend/app/features/users/router.py

@router.get("", response_model=List[UserProfileResponse])
def get_all_users(
    current_user: User = Depends(require_role(["admin"])),
    session: Session = Depends(get_session)
) -> List[UserProfileResponse]:
    """
    Get all users (admin only).
    
    Returns list of all users in the system.
    """
    user_repo = UserRepository(session)
    users = user_repo.get_all_users()
    return [UserProfileResponse.model_validate(user) for user in users]
```

**Response:**
```json
[
  {
    "id": "uuid",
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+63 917 123 4567",
    "city": "Manila",
    "role": "pet_owner",
    "is_active": true,
    "created_at": "2025-01-01T00:00:00"
  }
]
```

### 2. Get Clinic Status
**Endpoint:** `GET /api/v1/clinic/status`
**Auth:** Not required
**Purpose:** Display clinic hours and status

**Implementation Required:**
```python
# File: backend/app/features/clinic/router.py

@router.get("/status", response_model=ClinicStatusResponse)
def get_clinic_status(
    session: Session = Depends(get_session)
) -> ClinicStatusResponse:
    """
    Get current clinic status and hours.
    
    No authentication required - public information.
    """
    clinic_repo = ClinicStatusRepository(session)
    status = clinic_repo.get_current_status()
    return ClinicStatusResponse.model_validate(status)
```

**Response:**
```json
{
  "id": "uuid",
  "is_open": true,
  "opening_time": "08:00:00",
  "closing_time": "20:00:00",
  "special_message": null,
  "updated_at": "2026-03-01T00:00:00"
}
```

### 3. Update Clinic Hours
**Endpoint:** `PATCH /api/v1/clinic/hours`
**Auth:** Required (Admin only)
**Purpose:** Staff can update clinic operating hours

**Request Body:**
```json
{
  "opening_time": "08:00",
  "closing_time": "20:00",
  "is_open": true,
  "special_message": "Closed for holiday on March 15"
}
```

**Implementation Required:**
```python
# File: backend/app/features/clinic/router.py

@router.patch("/hours", response_model=ClinicStatusResponse)
def update_clinic_hours(
    request: ClinicHoursUpdate,
    current_user: User = Depends(require_role(["admin"])),
    session: Session = Depends(get_session)
) -> ClinicStatusResponse:
    """
    Update clinic operating hours (admin only).
    
    Allows staff to set opening/closing times and status.
    """
    clinic_repo = ClinicStatusRepository(session)
    clinic_service = ClinicService(clinic_repo)
    
    status = clinic_service.update_hours(
        opening_time=request.opening_time,
        closing_time=request.closing_time,
        is_open=request.is_open,
        special_message=request.special_message
    )
    
    session.commit()
    return ClinicStatusResponse.model_validate(status)
```

**Response:**
```json
{
  "id": "uuid",
  "is_open": true,
  "opening_time": "08:00:00",
  "closing_time": "20:00:00",
  "special_message": "Closed for holiday on March 15",
  "updated_at": "2026-03-01T10:30:00"
}
```

---

## Schema Definitions Needed

### ClinicStatusResponse
```python
# File: backend/app/features/clinic/schemas.py

from pydantic import BaseModel
from datetime import time, datetime
from typing import Optional
import uuid

class ClinicStatusResponse(BaseModel):
    """Response schema for clinic status."""
    id: uuid.UUID
    is_open: bool
    opening_time: time
    closing_time: time
    special_message: Optional[str]
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

### ClinicHoursUpdate
```python
# File: backend/app/features/clinic/schemas.py

class ClinicHoursUpdate(BaseModel):
    """Request schema for updating clinic hours."""
    opening_time: str  # Format: "HH:MM"
    closing_time: str  # Format: "HH:MM"
    is_open: bool
    special_message: Optional[str] = None
```

---

## Repository Methods Needed

### UserRepository
```python
# File: backend/app/features/users/repository.py

def get_all_users(self) -> List[User]:
    """Get all users (admin only)."""
    return self.session.exec(select(User)).all()
```

### ClinicStatusRepository
```python
# File: backend/app/features/clinic/repository.py

def get_current_status(self) -> ClinicStatus:
    """Get current clinic status."""
    status = self.session.exec(
        select(ClinicStatus).order_by(ClinicStatus.updated_at.desc())
    ).first()
    
    if not status:
        # Create default status if none exists
        status = ClinicStatus(
            is_open=True,
            opening_time=time(8, 0),
            closing_time=time(20, 0)
        )
        self.session.add(status)
        self.session.commit()
    
    return status

def update_hours(
    self,
    opening_time: time,
    closing_time: time,
    is_open: bool,
    special_message: Optional[str] = None
) -> ClinicStatus:
    """Update clinic hours."""
    status = self.get_current_status()
    status.opening_time = opening_time
    status.closing_time = closing_time
    status.is_open = is_open
    status.special_message = special_message
    status.updated_at = datetime.utcnow()
    
    self.session.add(status)
    return status
```

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Not authorized to perform this action"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 409 Conflict (Double Booking)
```json
{
  "detail": "Time slot is not available"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "opening_time"],
      "msg": "Invalid time format",
      "type": "value_error"
    }
  ]
}
```

---

## Frontend Integration Examples

### Load All Data for Staff Dashboard
```javascript
async function loadStaffDashboardData() {
  const token = localStorage.getItem('access_token');
  
  try {
    const [appointmentsRes, petsRes, usersRes, clinicRes] = await Promise.all([
      fetch(`${API_BASE_URL}/api/v1/appointments`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      fetch(`${API_BASE_URL}/api/v1/pets`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      fetch(`${API_BASE_URL}/api/v1/users`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      fetch(`${API_BASE_URL}/api/v1/clinic/status`)
    ]);
    
    const appointments = await appointmentsRes.json();
    const pets = await petsRes.json();
    const users = await usersRes.json();
    const clinicStatus = await clinicRes.json();
    
    // Process and display data
    displayStaffDashboard(appointments, pets, users, clinicStatus);
    
  } catch (error) {
    console.error('Failed to load dashboard data:', error);
  }
}
```

### Confirm Appointment
```javascript
async function confirmAppointment(appointmentId) {
  const token = localStorage.getItem('access_token');
  
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/appointments/${appointmentId}/status`,
      {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: 'confirmed' })
      }
    );
    
    if (response.ok) {
      showToast('Appointment confirmed!', '✓');
      loadStaffDashboardData(); // Reload data
    } else {
      const error = await response.json();
      showToast(error.detail || 'Failed to confirm appointment', '❌');
    }
  } catch (error) {
    console.error('Error confirming appointment:', error);
  }
}
```

### Update Clinic Hours
```javascript
async function updateClinicHours() {
  const token = localStorage.getItem('access_token');
  const openingTime = document.getElementById('opening-time').value;
  const closingTime = document.getElementById('closing-time').value;
  const isOpen = document.getElementById('clinic-open').checked;
  const specialMessage = document.getElementById('special-message').value;
  
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/clinic/hours`,
      {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          opening_time: openingTime,
          closing_time: closingTime,
          is_open: isOpen,
          special_message: specialMessage || null
        })
      }
    );
    
    if (response.ok) {
      showToast('Clinic hours updated!', '✓');
      loadClinicStatus(); // Reload status
    } else {
      const error = await response.json();
      showToast(error.detail || 'Failed to update hours', '❌');
    }
  } catch (error) {
    console.error('Error updating clinic hours:', error);
  }
}
```

---

## Testing Endpoints

### Using cURL

**Get All Appointments:**
```bash
curl -X GET "http://localhost:8000/api/v1/appointments" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Confirm Appointment:**
```bash
curl -X PATCH "http://localhost:8000/api/v1/appointments/APPOINTMENT_ID/status" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "confirmed"}'
```

**Get Clinic Status:**
```bash
curl -X GET "http://localhost:8000/api/v1/clinic/status"
```

**Update Clinic Hours:**
```bash
curl -X PATCH "http://localhost:8000/api/v1/clinic/hours" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "opening_time": "08:00",
    "closing_time": "20:00",
    "is_open": true,
    "special_message": null
  }'
```

---

## Summary

### Existing Endpoints (Ready to Use):
- ✅ GET /api/v1/appointments
- ✅ PATCH /api/v1/appointments/{id}/status
- ✅ GET /api/v1/appointments/available-slots
- ✅ GET /api/v1/pets
- ✅ GET /api/v1/users/profile

### New Endpoints Needed:
- ❌ GET /api/v1/users (admin only)
- ❌ GET /api/v1/clinic/status
- ❌ PATCH /api/v1/clinic/hours (admin only)

**Next Step:** Implement the 3 new endpoints before starting frontend work.
