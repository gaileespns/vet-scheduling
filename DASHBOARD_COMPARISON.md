# Dashboard Comparison - Client vs Staff

## Quick Overview

| Feature | Client Dashboard | Staff Dashboard |
|---------|-----------------|-----------------|
| **URL** | `/app.html` | `/staff-dashboard.html` |
| **Access** | Pet Owners | Clinic Staff (Admin) |
| **Badge Color** | 🟢 Green "Client" | 🟠 Amber "Staff" |
| **Auto Redirect** | No | Yes (from app.html) |

## Features Comparison

### Appointments

| Feature | Client | Staff |
|---------|--------|-------|
| View own appointments | ✅ | ✅ |
| View all appointments | ❌ | ✅ |
| Book appointments | ✅ | ✅ |
| Confirm appointments | ❌ | ✅ |
| Cancel own appointments | ✅ | ✅ |
| Cancel any appointment | ❌ | ✅ |
| Reschedule | ✅ | ✅ |
| Filter by status | ❌ | ✅ |
| Filter by date | ❌ | ✅ |

### Calendar

| Feature | Client | Staff |
|---------|--------|-------|
| Calendar view | ❌ | ✅ |
| Month navigation | ❌ | ✅ |
| Visual indicators | ❌ | ✅ |
| Click to filter | ❌ | ✅ |
| Appointment dots | ❌ | ✅ |

### Statistics

| Feature | Client | Staff |
|---------|--------|-------|
| Upcoming count | ✅ | ✅ |
| Pending count | ❌ | ✅ |
| Confirmed count | ❌ | ✅ |
| Today count | ❌ | ✅ |
| Total count | ❌ | ✅ |
| My pets count | ✅ | ❌ |
| Next visit | ✅ | ❌ |

### Pets Management

| Feature | Client | Staff |
|---------|--------|-------|
| View own pets | ✅ | ✅ |
| View all pets | ❌ | ✅ |
| Add pet | ✅ | ✅ |
| Edit own pet | ✅ | ✅ |
| Edit any pet | ❌ | ✅ |
| Delete own pet | ✅ | ✅ |
| Delete any pet | ❌ | ✅ |

### Profile

| Feature | Client | Staff |
|---------|--------|-------|
| View profile | ✅ | ✅ |
| Edit profile | ✅ | ✅ |
| Role display | "Pet Owner" | "Clinic Staff" |

## Visual Differences

### Client Dashboard
```
┌─────────────────────────────────────┐
│ 🐾 PawCare    [Client] [Avatar]    │
├─────────────────────────────────────┤
│ Good morning, John!                 │
│                                     │
│ [Stats: Upcoming | Pets | Next]    │
│                                     │
│ Upcoming Appointments               │
│ ├─ Mon 9:00 AM - Noodles           │
│ ├─ Wed 2:30 PM - Mochi             │
│ └─ Fri 11:00 AM - Noodles          │
│                                     │
│ [Book Appointment CTA]              │
│                                     │
│ My Pets                             │
│ ├─ 🐶 Noodles                      │
│ ├─ 🐱 Mochi                        │
│ └─ [+ Add Pet]                     │
└─────────────────────────────────────┘
```

### Staff Dashboard
```
┌─────────────────────────────────────┐
│ 🐾 PawCare    [Staff] [Avatar]     │
├─────────────────────────────────────┤
│ Staff Dashboard                     │
│ Saturday, February 28, 2026         │
│                                     │
│ [Pending] [Confirmed] [Today] [Total]│
│                                     │
│ Appointment Calendar                │
│ ┌─────────────────────────────┐   │
│ │ [<] February 2026 [>]       │   │
│ │ S  M  T  W  T  F  S         │   │
│ │ 1  2  3  4  5  6  7         │   │
│ │ 8  9 10 11 12 13 14         │   │
│ │...                          │   │
│ └─────────────────────────────┘   │
│                                     │
│ All Appointments                    │
│ [All] [Pending] [Confirmed] [Today]│
│ ├─ 9:00 AM - Noodles [Confirm]    │
│ ├─ 2:30 PM - Mochi [Confirm]      │
│ └─ 11:00 AM - Buddy [Cancel]      │
└─────────────────────────────────────┘
```

## User Flows

### Client Flow
```
Login → app.html → Stay on Client Dashboard
```

### Staff Flow
```
Login → app.html → Auto-redirect → staff-dashboard.html
```

## Access URLs

### Client Dashboard
```
http://localhost:5173/app.html
```
- Accessible by: Clients and Staff
- Staff are auto-redirected to staff dashboard

### Staff Dashboard
```
http://localhost:5173/staff-dashboard.html
```
- Accessible by: Staff only
- Clients see "Access denied" and redirect to app.html

## When to Use Which

### Use Client Dashboard When:
- You're a pet owner
- You want to manage your own pets
- You want to book appointments for your pets
- You want to view your appointment history
- You want to update your profile

### Use Staff Dashboard When:
- You're clinic staff/admin
- You need to see all appointments
- You need to confirm pending appointments
- You need to manage clinic schedule
- You need overview of daily operations
- You need to use the calendar view

## Key Differences Summary

### Client Dashboard Focus:
- **Personal**: Own pets and appointments
- **Booking**: Easy appointment creation
- **Management**: Pet profiles and history
- **Simple**: Streamlined interface

### Staff Dashboard Focus:
- **Overview**: All appointments and pets
- **Management**: Confirm/cancel appointments
- **Planning**: Calendar view for scheduling
- **Operations**: Statistics and monitoring
- **Comprehensive**: Full system access

## Navigation

### Client Dashboard Tabs:
1. Dashboard - Overview
2. Appointments - My appointments
3. My Pets - Pet management
4. Profile - Personal info

### Staff Dashboard Sections:
1. Statistics - Quick metrics
2. Calendar - Monthly view
3. Appointments - All appointments with filters
4. (Profile accessible via avatar)

## Color Coding

### Client Dashboard:
- Primary: Green (Sage)
- Accent: Forest Green
- Badge: Green "Client"

### Staff Dashboard:
- Primary: Forest Green
- Accent: Amber
- Badge: Amber "Staff"

## Permissions

### Client Can:
- ✅ View own data
- ✅ Create appointments
- ✅ Manage own pets
- ✅ Update own profile
- ❌ See other users' data
- ❌ Confirm appointments
- ❌ Access staff dashboard

### Staff Can:
- ✅ View all data
- ✅ Create appointments
- ✅ Manage all pets
- ✅ Update own profile
- ✅ Confirm appointments
- ✅ Cancel any appointment
- ✅ Access both dashboards
- ✅ View statistics
- ✅ Use calendar

## Best Practices

### For Clients:
1. Use the client dashboard for daily tasks
2. Book appointments through the CTA button
3. Keep pet profiles updated
4. Check upcoming appointments regularly

### For Staff:
1. Start day by checking staff dashboard
2. Review pending appointments first
3. Use calendar for planning ahead
4. Filter by "Today" for current focus
5. Confirm appointments as they're verified

## Technical Notes

### Authentication:
- Both dashboards check JWT token
- Staff dashboard verifies admin role
- Auto-redirect based on role

### API Calls:
- Client: Filtered by user_id
- Staff: Returns all records

### State Management:
- Client: Local user data
- Staff: All appointments cached

---

**Last Updated**: February 28, 2026
**Version**: 1.0.0
