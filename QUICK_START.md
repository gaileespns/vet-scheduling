# PawCare - Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Prerequisites
- ✅ Backend running on port 8000
- ✅ Frontend running on port 5173
- ✅ Database connected

### Step 1: Open the Landing Page
```
http://localhost:5173/landing.html
```

### Step 2: Register Your Account

#### For Pet Owners (Clients):
1. Click "Get Started" or "Sign In"
2. Click "Register" tab
3. Select **"🐾 Pet Owner (Client)"**
4. Fill in your details:
   - Name: Your full name
   - Email: your@email.com
   - Password: At least 8 characters
5. Click "Create Account"
6. ✨ You're in! Redirected to dashboard in 0.5 seconds

#### For Clinic Staff (Admin):
1. Click "Get Started" or "Sign In"
2. Click "Register" tab
3. Select **"👨‍⚕️ Clinic Staff (Admin)"**
4. Fill in your details:
   - Name: Your full name
   - Email: your@email.com (will be converted to admin email)
   - Password: At least 8 characters
5. Click "Create Account"
6. ✨ You're in! Redirected to dashboard in 0.5 seconds

### Step 3: Explore the Dashboard

#### What You'll See:
- **Top Right**: Your role badge (Green "Client" or Amber "Staff")
- **Dashboard**: Upcoming appointments, stats, and quick actions
- **Navigation**: Switch between Dashboard, Appointments, Pets, and Profile

#### Quick Actions:
- 📅 Book an appointment
- 🐾 Add a pet
- 👤 Update your profile
- 🚪 Logout (click avatar)

## 🎯 Key Features

### For Clients:
- ✅ Book appointments for your pets
- ✅ View appointment history
- ✅ Manage pet profiles
- ✅ Update personal information
- ✅ Real-time appointment status

### For Staff:
- ✅ View all appointments
- ✅ Manage all pets in system
- ✅ Update clinic status
- ✅ Confirm/complete appointments
- ✅ Full system access

## 🔐 Security

- 🔒 Passwords hashed with bcrypt
- 🎫 JWT token authentication
- ⏰ 24-hour token expiration
- 🚫 Token blacklist on logout
- 🛡️ Role-based access control

## 📱 URLs

| Page | URL | Description |
|------|-----|-------------|
| Landing | http://localhost:5173/landing.html | Marketing page |
| Auth | http://localhost:5173/auth.html | Login/Register |
| App | http://localhost:5173/app.html | Dashboard |
| API Docs | http://localhost:8000/docs | Backend API |
| Health | http://localhost:8000/health | Backend status |

## 🎨 Visual Indicators

### Role Badges:
- **Client**: 🟢 Green badge with "Client" text
- **Staff**: 🟠 Amber badge with "Staff" text

### Status Colors:
- **Success**: Green background
- **Error**: Red background
- **Pending**: Yellow/Amber
- **Completed**: Blue

## ⚡ Quick Tips

1. **Fast Login**: Credentials are remembered in browser
2. **Quick Logout**: Click your avatar → Confirm
3. **Role Check**: Look at badge color (Green = Client, Amber = Staff)
4. **Errors**: Check browser console (F12) for details
5. **Backend**: Check logs if API calls fail

## 🐛 Troubleshooting

### "Connection error"
→ Make sure backend is running: http://localhost:8000/health

### Not redirecting after login
→ Check browser console for errors
→ Clear localStorage and try again

### "Invalid credentials"
→ Double-check email and password
→ Remember: Staff emails are converted to admin format

### Token expired
→ Login again (tokens last 24 hours)

### Backend not starting
→ Check DATABASE_URL in backend/.env
→ Verify PostgreSQL is running

## 📞 Need Help?

1. Check `AUTHENTICATION_GUIDE.md` for detailed docs
2. Check `TEST_AUTHENTICATION.md` for testing guide
3. Check `LATEST_UPDATES.md` for recent changes
4. Check backend logs: Set `LOG_LEVEL=DEBUG` in .env
5. Check browser console (F12)

## 🎉 You're All Set!

Start by registering an account and exploring the dashboard. The system will guide you through the rest!

---

**Quick Links:**
- 🏠 [Landing Page](http://localhost:5173/landing.html)
- 🔐 [Login/Register](http://localhost:5173/auth.html)
- 📊 [Dashboard](http://localhost:5173/app.html)
- 📚 [API Docs](http://localhost:8000/docs)

**Last Updated**: February 28, 2026
