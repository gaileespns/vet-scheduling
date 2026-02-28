# PawCare Authentication System Guide

## Overview

The PawCare system now has a fully integrated authentication system connecting the frontend with the FastAPI backend. Both clients (pet owners) and staff (admin) can register and login through the same interface.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Vite)                       │
│  - Landing Page (landing.html)                          │
│  - Authentication Page (auth.html)                      │
│  - Application Dashboard (app.html)                     │
└─────────────────────────────────────────────────────────┘
                            ↓
                    JWT Token (Bearer)
                            ↓
┌─────────────────────────────────────────────────────────┐
│                Backend (FastAPI + PostgreSQL)            │
│  - User Registration & Login                            │
│  - Role-Based Access Control (Admin/Pet Owner)          │
│  - JWT Token Management                                 │
│  - Token Blacklist for Logout                           │
└─────────────────────────────────────────────────────────┘
```

## URLs

- **Landing Page**: http://localhost:5173/landing.html
- **Authentication**: http://localhost:5173/auth.html
- **Application**: http://localhost:5173/app.html
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## User Roles

### 1. Pet Owner (Client)
- Default role for all registered users
- Can manage their own pets
- Can book and manage their own appointments
- Can view and update their profile

### 2. Admin (Staff)
- Assigned to users with email matching `ADMIN_EMAIL` in backend `.env`
- Default admin email: `admin@vetclinic.com`
- Full access to all resources
- Can manage all pets and appointments
- Can update clinic status
- Can confirm/complete appointments

## How to Use

### For Pet Owners (Clients)

1. **Visit Landing Page**: http://localhost:5173/landing.html
2. **Click "Get Started" or "Sign In"**
3. **Register**:
   - Click "Register" tab
   - **Select "🐾 Pet Owner (Client)"** from the role dropdown
   - Enter full name, email, and password (min 8 characters)
   - Click "Create Account"
   - You'll be automatically logged in and redirected to the dashboard (0.5 seconds)

4. **Login** (if already registered):
   - Enter email and password
   - Click "Sign In"
   - Redirected to dashboard immediately (0.5 seconds)

5. **Use the Application**:
   - View upcoming appointments
   - Manage your pets
   - Book new appointments
   - Update your profile
   - See "Client" badge in the top navigation

6. **Logout**:
   - Click on your avatar in the top right
   - Confirm logout
   - Your token will be invalidated

### For Staff (Admin)

1. **Register with Staff Role**:
   - Click "Register" tab
   - **Select "👨‍⚕️ Clinic Staff (Admin)"** from the role dropdown
   - Enter your details (any email will work)
   - The system will automatically convert your email to admin format
   - Complete registration
   - You'll automatically get admin role and be redirected immediately

2. **Admin Capabilities**:
   - View all appointments (not just your own)
   - Manage all pets in the system
   - Update clinic status (open/closed)
   - Confirm and complete appointments
   - Access all user data
   - See "Staff" badge in the top navigation (amber color)

## Role Selection

During registration, users must select their role:

- **🐾 Pet Owner (Client)**: For pet owners who want to book appointments
  - Email: Uses the email you provide
  - Badge: Green "Client" badge
  - Access: Own pets and appointments only

- **👨‍⚕️ Clinic Staff (Admin)**: For clinic staff managing operations
  - Email: Automatically converted to `admin+yourname@vetclinic.com` format
  - Badge: Amber "Staff" badge
  - Access: Full system access

The role selection ensures proper access control and user experience from the start.

## Authentication Flow

### Registration
```
User → auth.html → POST /api/v1/auth/register → Backend
                                                    ↓
                                            Create User
                                            Hash Password
                                            Assign Role
                                            Generate JWT
                                                    ↓
                                            Return Token
                                                    ↓
                                        Store in localStorage
                                                    ↓
                                        Redirect to app.html
```

### Login
```
User → auth.html → POST /api/v1/auth/login → Backend
                                                  ↓
                                          Verify Credentials
                                          Check Token Blacklist
                                          Generate JWT
                                                  ↓
                                          Return Token
                                                  ↓
                                      Store in localStorage
                                                  ↓
                                      Redirect to app.html
```

### Protected Requests
```
User → app.html → API Request + Bearer Token → Backend
                                                    ↓
                                            Verify Token
                                            Check Blacklist
                                            Check Expiration
                                                    ↓
                                            Return Data
```

### Logout
```
User → app.html → POST /api/v1/auth/logout + Token → Backend
                                                          ↓
                                                  Add to Blacklist
                                                  Store Expiration
                                                          ↓
                                                  Return Success
                                                          ↓
                                              Remove from localStorage
                                                          ↓
                                              Redirect to auth.html
```

## Security Features

1. **Password Hashing**: All passwords are hashed using bcrypt before storage
2. **JWT Tokens**: Secure token-based authentication with 24-hour expiration
3. **Token Blacklist**: Logout invalidates tokens immediately
4. **Automatic Cleanup**: Expired tokens are removed from blacklist daily
5. **CORS Protection**: Backend only accepts requests from configured origins
6. **Role-Based Access**: Endpoints are protected based on user role
7. **HTTPS Ready**: System is ready for production with HTTPS

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login existing user
- `POST /api/v1/auth/logout` - Logout and invalidate token (requires auth)

### Users
- `GET /api/v1/users/me` - Get current user profile (requires auth)
- `PATCH /api/v1/users/profile` - Update profile (requires auth)

### Pets
- `GET /api/v1/pets` - List pets (requires auth)
- `POST /api/v1/pets` - Create pet (requires auth)
- `PATCH /api/v1/pets/{id}` - Update pet (requires auth)
- `DELETE /api/v1/pets/{id}` - Delete pet (requires auth)

### Appointments
- `GET /api/v1/appointments` - List appointments (requires auth)
- `POST /api/v1/appointments` - Create appointment (requires auth)
- `PATCH /api/v1/appointments/{id}/reschedule` - Reschedule (requires auth)
- `PATCH /api/v1/appointments/{id}/status` - Update status (admin only)
- `DELETE /api/v1/appointments/{id}` - Cancel appointment (requires auth)

### Clinic
- `GET /api/v1/clinic/status` - Get clinic status (public)
- `PATCH /api/v1/clinic/status` - Update status (admin only)

## Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@host:port/db?sslmode=require
JWT_SECRET_KEY=your-super-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
ADMIN_EMAIL=admin@vetclinic.com
BACKEND_CORS_ORIGINS=http://localhost:5173,http://localhost:3000
ENVIRONMENT=development
LOG_LEVEL=INFO
CLINIC_TIMEZONE=Asia/Manila
```

### Frontend (auth.html & app.html)
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## Troubleshooting

### "Connection error. Please make sure the backend is running."
- Check if backend is running: http://localhost:8000/health
- Verify CORS settings in backend `.env`
- Check browser console for detailed errors

### "Invalid email or password"
- Verify credentials are correct
- Check if user is registered
- Ensure password meets requirements (min 8 characters)

### "Token has been invalidated"
- User has logged out
- Token was manually blacklisted
- Login again to get a new token

### Redirected to auth page when already logged in
- Token may have expired (24 hours default)
- Token may be invalid or corrupted
- Clear localStorage and login again

### Backend not starting
- Check if PostgreSQL database is accessible
- Verify DATABASE_URL in `.env`
- Check if port 8000 is available
- Review backend logs for errors

## Testing

### Test User Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Test Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Test Protected Endpoint
```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Test Logout
```bash
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Development Notes

- Frontend uses localStorage to store JWT tokens
- Tokens are automatically included in all API requests
- App checks authentication on page load
- Expired or invalid tokens redirect to auth page
- User data is fetched and displayed on successful auth
- Logout invalidates token server-side and clears localStorage

## Production Deployment

Before deploying to production:

1. **Change JWT_SECRET_KEY** to a strong random value
2. **Update BACKEND_CORS_ORIGINS** to your production domain
3. **Enable HTTPS** for both frontend and backend
4. **Update API_BASE_URL** in frontend files to production URL
5. **Set ENVIRONMENT=production** in backend
6. **Use strong DATABASE_URL** with SSL
7. **Configure proper logging** (LOG_LEVEL=WARNING or ERROR)
8. **Set up monitoring** for failed login attempts
9. **Implement rate limiting** for auth endpoints
10. **Regular security audits** and dependency updates

## Support

For issues or questions:
- Check backend logs: `LOG_LEVEL=DEBUG` in `.env`
- Check browser console for frontend errors
- Review API documentation: http://localhost:8000/docs
- Check database connectivity
- Verify all environment variables are set correctly
