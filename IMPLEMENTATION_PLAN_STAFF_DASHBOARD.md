# Staff Dashboard - Complete Implementation Plan

## Overview
This document outlines the complete implementation plan for improving the staff dashboard with backend integration, double booking prevention, and clinic hours management.

---

## Feature 1: Staff Dashboard Backend Integration & UI Improvements

### 1.1 Add Appointments Tab
**Current State:** Appointments list is on the main view
**Target State:** Separate tab for appointments, calendar stays on main view

**Changes Required:**
- Add tab navigation (Dashboard, Appointments, Settings)
- Move appointments list to Appointments tab
- Keep calendar and stats on Dashboard tab

**Files to Modify:**
- `frontend/public/staff-dashboard.html`

**Implementation Approach:**
```html
<!-- Add tab navigation -->
<div class="tabs">
  <button class="tab active" onclick="switchStaffTab('dashboard')">Dashboard</button>
  <button class="tab" onclick="switchStaffTab('appointments')">Appointments</button>
  <button class="tab" onclick="switchStaffTab('settings')">Settings</button>
</div>

<!-- Dashboard Tab (Calendar + Stats) -->
<div id="staff-dashboard-tab" class="tab-content active">
  <!-- Stats cards -->
  <!-- Calendar -->
</div>

<!-- Appointments Tab -->
<div id="staff-appointments-tab" class="tab-content">
  <!-- Appointments list with filters -->
</div>

<!-- Settings Tab (for clinic hours) -->
<div id="staff-settings-tab" class="tab-content">
  <!-- Clinic hours management -->
</div>
```

### 1.2 Load Real Appointments from Backend
**Current State:** Static/dummy data
**Target State:** Load from `/api/v1/appointments` endpoint

**API Endpoint:** `GET /api/v1/appointments`
**Response Format:**
```json
[
  {
    "id": "uuid",
    "pet_id": "uuid",
    "user_id": "uuid",
    "start_time": "2026-03-04T10:00:00",
    "end_time": "2026-03-04T10:45:00",
    "service_type": "Routine Check-up",
    "status": "pending",
    "notes": "First visit",
    "created_at": "2026-03-01T08:00:00"
  }
]
```

**Implementation:**
```javascript
async function loadAllAppointments() {
  const token = localStorage.getItem('access_token');
  
  try {
    // Fetch appointments and pets in parallel
    const [appointmentsRes, petsRes, usersRes] = await Promise.all([
      fetch(`${API_BASE_URL}/api/v1/appointments`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      fetch(`${API_BASE_URL}/api/v1/pets`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      // Note: Need to add endpoint to get all users (admin only)
      fetch(`${API_BASE_URL}/api/v1/users`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
    ]);
    
    const appointments = await appointmentsRes.json();
    const pets = await petsRes.json();
    const users = await usersRes.json();
    
    // Create lookup maps
    const petMap = {};
    pets.forEach(pet => {
      petMap[pet.id] = pet;
    });
    
    const userMap = {};
    users.forEach(user => {
      userMap[user.id] = user;
    });
    
    // Enrich appointments with pet and owner data
    const enrichedAppointments = appointments.map(appt => {
      const pet = petMap[appt.pet_id];
      const owner = pet ? userMap[pet.user_id] : null;
      
      return {
        ...appt,
        pet_name: pet?.name || 'Unknown',
        pet_species: pet?.species || 'unknown',
        owner_name: owner?.full_name || 'Unknown',
        owner_email: owner?.email || ''
      };
    });
    
    renderStaffAppointments(enrichedAppointments);
    renderStaffCalendar(enrichedAppointments);
    updateStaffStats(enrichedAppointments);
    
  } catch (error) {
    console.error('Failed to load appointments:', error);
  }
}
```

### 1.3 Display Appointment Details
**Required Information:**
- Pet name and species
- Owner name
- Service type
- Date and time
- Status (pending, confirmed, completed, cancelled)
- Notes
- Actions (Confirm, Cancel)

**Appointment Card Template:**
```html
<div class="appointment-card">
  <div class="appt-header">
    <div class="appt-date">
      <div class="date-day">4</div>
      <div class="date-month">MAR</div>
    </div>
    <div class="appt-info">
      <div class="appt-time">10:00 AM - 10:45 AM</div>
      <div class="appt-pet">🐶 Max (Golden Retriever)</div>
      <div class="appt-owner">Owner: John Doe</div>
      <div class="appt-service">Routine Check-up</div>
    </div>
    <div class="appt-status status-pending">Pending</div>
  </div>
  <div class="appt-notes">Notes: First visit, dog is anxious</div>
  <div class="appt-actions">
    <button class="btn btn-success" onclick="confirmAppointment('uuid')">Confirm</button>
    <button class="btn btn-danger" onclick="cancelAppointment('uuid')">Cancel</button>
  </div>
</div>
```

### 1.4 Add Logout Button
**Location:** Top right corner next to Staff Dashboard badge

**Implementation:**
```html
<!-- In navigation -->
<div class="nav-right">
  <div class="staff-badge">Staff Dashboard</div>
  <div class="avatar">A1</div>
  <button class="btn-logout" onclick="openModal('logout-modal')">
    <svg><!-- logout icon --></svg>
  </button>
</div>

<!-- Logout Modal -->
<div class="modal-overlay" id="logout-modal">
  <div class="modal">
    <div class="modal-header">
      <div class="modal-title">Confirm Logout</div>
    </div>
    <div class="modal-body">
      <p>Are you sure you want to logout?</p>
    </div>
    <div class="modal-footer">
      <button class="btn btn-outline" onclick="closeModal('logout-modal')">Cancel</button>
      <button class="btn btn-danger" onclick="handleStaffLogout()">Logout</button>
    </div>
  </div>
</div>
```

---

## Feature 2: Double Booking Prevention

### 2.1 Check Time Conflicts
**Goal:** Prevent clients from booking appointments that overlap with existing appointments

**Backend Validation:**
The backend already has this logic in `AppointmentService.create_appointment()`:
```python
# Check for overlapping appointments
overlapping = self.appointment_repo.find_overlapping_appointments(
    start_time=start_time,
    end_time=end_time
)
if overlapping:
    raise ConflictException("Time slot is not available")
```

**Frontend Implementation:**
Need to fetch available slots before showing booking modal.

### 2.2 Show Available Time Slots
**Current State:** Static time slots in booking modal
**Target State:** Dynamic slots based on existing appointments

**New API Endpoint (Already exists!):**
`GET /api/v1/appointments/available-slots?date=2026-03-04&service_type=routine`

**Implementation:**
```javascript
async function openBookingModal() {
  openModal('book-modal');
  
  // Get selected date and service type
  const date = document.getElementById('book-date').value;
  const serviceType = document.getElementById('book-service-type').value;
  
  if (date && serviceType) {
    await loadAvailableSlots(date, serviceType);
  }
}

async function loadAvailableSlots(date, serviceType) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/appointments/available-slots?date=${date}&service_type=${serviceType}`
    );
    
    const slots = await response.json();
    renderTimeSlots(slots);
    
  } catch (error) {
    console.error('Failed to load available slots:', error);
  }
}

function renderTimeSlots(slots) {
  const container = document.getElementById('time-slots-container');
  
  container.innerHTML = slots.map(slot => {
    const startTime = new Date(slot.start_time);
    const timeStr = startTime.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit' 
    });
    
    return `
      <button class="time-slot" 
              data-start="${slot.start_time}" 
              data-end="${slot.end_time}"
              onclick="selectTimeSlot(this)">
        ${timeStr}
      </button>
    `;
  }).join('');
}
```

### 2.3 Update Booking Modal
**Changes Required:**
1. Remove static time slots
2. Add date picker change listener
3. Add service type change listener
4. Dynamically load and display available slots
5. Disable booking button if no slot selected

---

## Feature 3: Clinic Hours Management

### 3.1 Database Schema
**Current State:** Clinic hours are hardcoded
**Target State:** Store in database, editable by staff

**Table:** `clinic_status` (already exists!)
**Columns:**
- id (UUID)
- is_open (boolean)
- opening_time (time)
- closing_time (time)
- special_message (text, nullable)
- updated_at (timestamp)

**Check existing schema:**
```bash
# Check if table exists and structure
psql -d vet_scheduling -c "\d clinic_status"
```

### 3.2 Backend API Endpoints

**Endpoint 1: Get Clinic Status**
`GET /api/v1/clinic/status`

**Response:**
```json
{
  "is_open": true,
  "opening_time": "08:00:00",
  "closing_time": "20:00:00",
  "special_message": null
}
```

**Endpoint 2: Update Clinic Hours (Admin Only)**
`PATCH /api/v1/clinic/hours`

**Request:**
```json
{
  "opening_time": "08:00",
  "closing_time": "20:00",
  "is_open": true
}
```

**Implementation Location:**
- File: `backend/app/features/clinic/router.py`
- Service: `backend/app/features/clinic/service.py`

### 3.3 Staff Dashboard UI
**Location:** Settings tab

**UI Design:**
```html
<div class="settings-section">
  <h3>Clinic Hours</h3>
  <div class="form-group">
    <label>Opening Time</label>
    <input type="time" id="opening-time" value="08:00">
  </div>
  <div class="form-group">
    <label>Closing Time</label>
    <input type="time" id="closing-time" value="20:00">
  </div>
  <div class="form-group">
    <label>
      <input type="checkbox" id="clinic-open" checked>
      Clinic is Open
    </label>
  </div>
  <div class="form-group">
    <label>Special Message (optional)</label>
    <textarea id="special-message" placeholder="e.g., Closed for holiday"></textarea>
  </div>
  <button class="btn btn-primary" onclick="updateClinicHours()">Save Changes</button>
</div>
```

### 3.4 Display Clinic Status
**Client Dashboard:**
- Show in "Clinic Status" card
- Update opening/closing times dynamically
- Show special message if any

**Staff Dashboard:**
- Show current status in header
- Allow quick toggle open/closed

**Implementation:**
```javascript
async function loadClinicStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/clinic/status`);
    const status = await response.json();
    
    // Update UI
    document.getElementById('clinic-opening-time').textContent = 
      formatTime(status.opening_time);
    document.getElementById('clinic-closing-time').textContent = 
      formatTime(status.closing_time);
    document.getElementById('clinic-status-badge').textContent = 
      status.is_open ? 'Open' : 'Closed';
    
    if (status.special_message) {
      document.getElementById('special-message-display').textContent = 
        status.special_message;
    }
    
  } catch (error) {
    console.error('Failed to load clinic status:', error);
  }
}
```

---

## Implementation Order & Estimates

### Phase 1: Staff Dashboard Improvements (45 min)
1. ✅ Add tab navigation (10 min)
2. ✅ Move appointments to separate tab (5 min)
3. ✅ Load real appointments from backend (15 min)
4. ✅ Display appointment details (10 min)
5. ✅ Add logout button and modal (5 min)

### Phase 2: Double Booking Prevention (30 min)
1. ✅ Update booking modal to use date picker (5 min)
2. ✅ Implement available slots loading (10 min)
3. ✅ Render dynamic time slots (10 min)
4. ✅ Add slot selection logic (5 min)

### Phase 3: Clinic Hours Management (60 min)
1. ✅ Check/update database schema (5 min)
2. ✅ Create backend API endpoints (20 min)
3. ✅ Build settings UI in staff dashboard (15 min)
4. ✅ Implement update clinic hours function (10 min)
5. ✅ Display clinic status on both dashboards (10 min)

**Total Estimated Time: ~2.5 hours**

---

## Files to Create/Modify

### Frontend Files:
1. `frontend/public/staff-dashboard.html` - Major updates
2. `frontend/public/app.html` - Update booking modal, clinic status display

### Backend Files:
1. `backend/app/features/clinic/router.py` - Add/update endpoints
2. `backend/app/features/clinic/service.py` - Business logic
3. `backend/app/features/clinic/schemas.py` - Request/response schemas

### Documentation:
1. `STAFF_DASHBOARD_API.md` - API documentation
2. `CLINIC_HOURS_GUIDE.md` - User guide for managing hours

---

## Testing Checklist

### Staff Dashboard:
- [ ] Tabs switch correctly
- [ ] Appointments load from backend
- [ ] Appointment details display correctly
- [ ] Confirm/cancel actions work
- [ ] Calendar shows correct appointments
- [ ] Stats update correctly
- [ ] Logout button works

### Double Booking:
- [ ] Available slots load correctly
- [ ] Unavailable slots are not shown
- [ ] Booking fails for overlapping times
- [ ] Success message on successful booking

### Clinic Hours:
- [ ] Staff can update hours
- [ ] Changes reflect on client dashboard
- [ ] Changes reflect on staff dashboard
- [ ] Bookings outside hours are prevented
- [ ] Special message displays correctly

---

## Next Steps

**Please review this plan and let me know:**
1. Does this approach look good?
2. Any changes or additions needed?
3. Should I proceed with implementation?
4. Which phase should I start with?

Once approved, I'll begin implementation phase by phase, testing each feature before moving to the next.
