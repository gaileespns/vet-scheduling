# Staff Dashboard Guide

## Overview

The Staff Dashboard is a comprehensive management interface designed specifically for clinic staff (admin users) to manage all appointments, view schedules, and monitor clinic operations.

## Features

### 1. **Statistics Overview** 📊
Four key metrics displayed at the top:
- **Pending**: Appointments awaiting confirmation
- **Confirmed**: Appointments ready for today
- **Today**: Total appointments scheduled for today
- **Total**: All appointments in the system

### 2. **Interactive Calendar** 📅
- **Monthly View**: See all appointments at a glance
- **Visual Indicators**: Days with appointments are highlighted in green
- **Dots**: Each dot represents an appointment (up to 3 shown)
- **Navigation**: Use arrow buttons to move between months
- **Click to Filter**: Click any day to see appointments for that date

### 3. **Appointments Management** 📋
- **View All Appointments**: Complete list of all appointments
- **Filter Options**:
  - All: Show all appointments
  - Pending: Only pending appointments
  - Confirmed: Only confirmed appointments
  - Today: Only today's appointments
- **Quick Actions**:
  - Confirm pending appointments
  - Cancel appointments
  - View appointment details

### 4. **Appointment Cards** 🎫
Each appointment card shows:
- **Time**: Hour and date
- **Pet Information**: Pet name with emoji
- **Owner**: Pet owner's name
- **Service Type**: Type of appointment
- **Status Badge**: Visual status indicator
- **Action Buttons**: Confirm or Cancel

## Access

### URL
```
http://localhost:5173/staff-dashboard.html
```

### Requirements
- Must be logged in as staff (admin role)
- If you're a client, you'll be redirected to the regular dashboard
- If not logged in, you'll be redirected to the auth page

## How to Use

### For Staff Members:

1. **Login as Staff**:
   - Register with "👨‍⚕️ Clinic Staff (Admin)" role
   - Or login with existing staff credentials
   - You'll be automatically redirected to the staff dashboard

2. **View Statistics**:
   - Check the four stat cards at the top
   - Get a quick overview of appointment status

3. **Use the Calendar**:
   - Navigate months using arrow buttons
   - Green days have appointments
   - Click a day to filter appointments for that date
   - Dots show number of appointments (max 3 visible)

4. **Manage Appointments**:
   - Use filter tabs to view specific appointment types
   - Click "Confirm" to approve pending appointments
   - Click "Cancel" to cancel appointments
   - View all appointment details in the list

5. **Confirm Appointments**:
   - Find pending appointments (yellow badge)
   - Click "Confirm" button
   - Appointment status changes to confirmed (green badge)

6. **Cancel Appointments**:
   - Click "Cancel" button on any active appointment
   - Confirm the cancellation
   - Appointment is removed from active list

## Visual Guide

### Status Colors:
- 🟡 **Yellow (Pending)**: Awaiting staff confirmation
- 🟢 **Green (Confirmed)**: Approved and scheduled
- 🔵 **Blue (Completed)**: Appointment finished
- 🔴 **Red (Cancelled)**: Appointment cancelled

### Calendar Colors:
- **Cream**: Regular days without appointments
- **Green**: Days with appointments
- **Amber**: Today's date
- **Gray**: Days from other months

## API Integration

The staff dashboard connects to these backend endpoints:

### Get All Appointments
```
GET /api/v1/appointments
Authorization: Bearer {token}
```

Returns all appointments (staff can see all, not just their own).

### Confirm Appointment
```
PATCH /api/v1/appointments/{id}/status
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "confirmed"
}
```

### Cancel Appointment
```
DELETE /api/v1/appointments/{id}
Authorization: Bearer {token}
```

## Automatic Redirects

### Staff Login Flow:
```
Login as Staff → Auth Page → Regular Dashboard → Staff Dashboard
```

The system automatically detects staff role and redirects to the appropriate dashboard.

### Client Login Flow:
```
Login as Client → Auth Page → Regular Dashboard (stays here)
```

## Keyboard Shortcuts

- **←/→**: Navigate calendar months (when calendar is focused)
- **Esc**: Close any open modals or dialogs

## Responsive Design

The dashboard is fully responsive:
- **Desktop**: Full grid layout with all features
- **Tablet**: 2-column stats grid, adjusted calendar
- **Mobile**: Single column layout, stacked cards

## Troubleshooting

### "Access denied. This dashboard is for staff only."
**Solution**: You're logged in as a client. Staff dashboard requires admin role.

### Calendar not showing appointments
**Solution**: 
- Check if appointments exist in the database
- Verify backend is running
- Check browser console for errors

### Can't confirm appointments
**Solution**:
- Verify you have admin role
- Check backend logs for permission errors
- Ensure appointment is in "pending" status

### Appointments not loading
**Solution**:
- Check backend is running: http://localhost:8000/health
- Verify token is valid
- Check browser console for API errors

## Features Comparison

| Feature | Client Dashboard | Staff Dashboard |
|---------|-----------------|-----------------|
| View own appointments | ✅ | ✅ |
| View all appointments | ❌ | ✅ |
| Calendar view | ❌ | ✅ |
| Confirm appointments | ❌ | ✅ |
| Statistics overview | Limited | Full |
| Filter by status | ❌ | ✅ |
| Manage all pets | ❌ | ✅ |

## Future Enhancements

Planned features for future versions:
- [ ] Drag-and-drop appointment rescheduling
- [ ] Week view calendar
- [ ] Day view with hourly slots
- [ ] Export appointments to CSV
- [ ] Print daily schedule
- [ ] Email notifications
- [ ] SMS reminders
- [ ] Appointment notes and history
- [ ] Pet medical records integration
- [ ] Revenue tracking
- [ ] Staff scheduling

## Tips for Efficient Use

1. **Start with Statistics**: Check the stat cards to prioritize work
2. **Use Filters**: Filter by "Pending" to see what needs attention
3. **Calendar Overview**: Use calendar to plan ahead
4. **Batch Confirm**: Confirm multiple pending appointments at once
5. **Today Filter**: Use "Today" filter to focus on current appointments

## Security

- All API calls require valid JWT token
- Staff role verified on every request
- Automatic logout on token expiration
- Secure token storage in localStorage
- CORS protection on backend

## Performance

- Appointments cached after initial load
- Calendar renders efficiently with virtual scrolling
- Optimized for 1000+ appointments
- Lazy loading for large datasets
- Debounced search and filters

## Browser Support

- ✅ Chrome/Edge (Chromium) - Recommended
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Support

For issues or questions:
1. Check browser console (F12)
2. Check backend logs
3. Verify authentication
4. Review API responses in Network tab
5. Check `DEBUG_REDIRECT_ISSUE.md` for common problems

---

**Last Updated**: February 28, 2026
**Version**: 1.0.0
**Status**: ✅ Production Ready
