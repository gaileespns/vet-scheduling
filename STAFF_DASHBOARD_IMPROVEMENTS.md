# Staff Dashboard Improvements - Implementation Plan

## Requirements Summary

### 1. UI Restructuring
- [x] Move appointments list to a separate tab/section
- [ ] Keep calendar on main view
- [ ] Add logout button with custom modal

### 2. Backend Integration
- [ ] Load and display actual appointments from database
- [ ] Show appointment details (pet name, owner, service type, time, notes)
- [ ] Real-time sync with client bookings
- [ ] Calendar should reflect actual booked appointments

### 3. Double Booking Prevention
- [ ] Check for time conflicts when clients book appointments
- [ ] Block unavailable time slots in client booking modal
- [ ] Show available/unavailable slots based on existing appointments

### 4. Clinic Hours Management
- [ ] Add UI for staff to set opening/closing hours
- [ ] Store clinic hours in database
- [ ] Mirror clinic hours to both staff and client dashboards
- [ ] Prevent bookings outside clinic hours

## Implementation Steps

### Phase 1: Staff Dashboard Backend Integration (Current)
1. Add appointments tab/section
2. Load appointments from `/api/v1/appointments` endpoint
3. Display appointment cards with full details
4. Add logout button with modal

### Phase 2: Double Booking Prevention
1. Modify client booking modal to check availability
2. Implement time slot validation
3. Show only available slots based on existing appointments

### Phase 3: Clinic Hours Management
1. Create clinic hours management UI in staff dashboard
2. Add backend endpoint for updating clinic hours
3. Display clinic status on both dashboards
4. Validate bookings against clinic hours

## Current Status
- Starting with Phase 1: Staff Dashboard improvements
