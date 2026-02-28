# Debug Redirect Issue - Step by Step

## What I Fixed

1. **Changed endpoint**: `/api/v1/users/me` → `/api/v1/users/profile` (correct endpoint)
2. **Changed redirect method**: `window.location.href` → `window.location.replace()` (forces immediate redirect)
3. **Added console logging**: To track the authentication flow
4. **Removed setTimeout**: Direct redirect instead of 500ms delay

## How to Test

### Step 1: Open Browser Console
1. Press `F12` to open Developer Tools
2. Go to the "Console" tab
3. Keep it open during testing

### Step 2: Clear Previous Data
```javascript
// Run this in the console:
localStorage.clear();
```

### Step 3: Try Registration
1. Go to: http://localhost:5173/auth.html
2. Click "Register" tab
3. Fill in:
   - Role: Select "🐾 Pet Owner (Client)"
   - Name: Test User
   - Email: test@example.com
   - Password: password123
   - Confirm: password123
4. Click "Create Account"

### Step 4: Watch Console Output
You should see:
```
Registering user: {role: "client", email: "test@example.com"}
Registration successful, storing token and redirecting...
Redirecting to /app.html
```

Then on app.html:
```
Checking authentication, token exists: true
Verifying token with backend...
Token verification response status: 200
User authenticated successfully: {id: "...", email: "...", ...}
```

### Step 5: If It Still Doesn't Work

#### Check 1: Backend Running?
```bash
# Open in browser:
http://localhost:8000/health

# Should return:
{"status": "healthy"}
```

#### Check 2: CORS Issue?
Look in console for errors like:
```
Access to fetch at 'http://localhost:8000/...' from origin 'http://localhost:5173' has been blocked by CORS
```

**Fix**: Check backend `.env` file:
```env
BACKEND_CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

#### Check 3: Token Stored?
In console, run:
```javascript
localStorage.getItem('access_token')
```

Should return a long JWT string like:
```
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Check 4: API Response
In Network tab:
1. Look for POST to `/api/v1/auth/register` or `/api/v1/auth/login`
2. Check Response tab
3. Should see:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

#### Check 5: Profile Endpoint
In console, run:
```javascript
const token = localStorage.getItem('access_token');
fetch('http://localhost:8000/api/v1/users/profile', {
  headers: { 'Authorization': `Bearer ${token}` }
})
.then(r => r.json())
.then(data => console.log('Profile data:', data));
```

Should return user data:
```json
{
  "id": "...",
  "email": "test@example.com",
  "full_name": "Test User",
  "role": "pet_owner",
  ...
}
```

## Common Issues & Solutions

### Issue 1: "Token verification failed, status: 401"
**Cause**: Token is invalid or expired
**Solution**: 
```javascript
localStorage.clear();
// Then register/login again
```

### Issue 2: "Connection error"
**Cause**: Backend not running
**Solution**:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Issue 3: Redirect loop (keeps going back to auth)
**Cause**: Token validation failing
**Solution**: Check console logs to see exact error, then:
```javascript
localStorage.clear();
// Register new account
```

### Issue 4: "CORS policy" error
**Cause**: Backend CORS not configured
**Solution**: Update `backend/.env`:
```env
BACKEND_CORS_ORIGINS=http://localhost:5173
```
Then restart backend.

### Issue 5: Blank page after redirect
**Cause**: JavaScript error on app.html
**Solution**: Check console for errors, look for:
- Missing elements
- Undefined variables
- Network errors

## Manual Test Commands

### Test Registration API Directly
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "email": "test2@example.com",
    "password": "password123"
  }'
```

Expected response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Test Profile API
```bash
# Replace YOUR_TOKEN with actual token
curl -X GET http://localhost:8000/api/v1/users/profile \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Expected response:
```json
{
  "id": "...",
  "email": "test2@example.com",
  "full_name": "Test User",
  "role": "pet_owner",
  "phone": null,
  "city": null,
  "preferences": null,
  "is_active": true,
  "created_at": "2026-02-28T..."
}
```

## What Should Happen (Success Flow)

1. **User fills form** → Form validates
2. **Click submit** → Button shows "Creating account..."
3. **API call** → POST to `/api/v1/auth/register`
4. **Backend responds** → 201 with token
5. **Token stored** → localStorage.setItem('access_token', ...)
6. **Success message** → Green alert appears
7. **Redirect** → window.location.replace('/app.html')
8. **App loads** → Checks token
9. **Token valid** → Fetches user profile
10. **UI updates** → Shows user name, role badge, etc.

## Still Not Working?

### Last Resort: Hard Refresh
1. Clear browser cache: `Ctrl + Shift + Delete`
2. Clear localStorage: `localStorage.clear()`
3. Close all browser tabs
4. Restart browser
5. Try again

### Check Backend Logs
```bash
# In backend terminal, you should see:
INFO:     127.0.0.1:xxxxx - "POST /api/v1/auth/register HTTP/1.1" 201 Created
INFO:     127.0.0.1:xxxxx - "GET /api/v1/users/profile HTTP/1.1" 200 OK
```

If you see 401, 403, or 500 errors, there's a backend issue.

### Enable Debug Mode
In `backend/.env`:
```env
LOG_LEVEL=DEBUG
```

Restart backend, then check logs for detailed error messages.

## Success Indicators

✅ Console shows "Registration successful"
✅ Console shows "Redirecting to /app.html"
✅ URL changes to http://localhost:5173/app.html
✅ Dashboard loads with user data
✅ Role badge appears (green for client, amber for staff)
✅ User name appears in greeting
✅ No errors in console

---

**If you're still having issues after following this guide, please share:**
1. Console output (all messages)
2. Network tab (failed requests)
3. Backend logs (any errors)
4. Browser and version
