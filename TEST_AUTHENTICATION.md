# Authentication System Test Guide

## Quick Test Checklist

### ✅ Pre-Test Setup
- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Database connected and initialized
- [ ] Browser console open (F12) for debugging

### Test 1: Client Registration Flow
**Objective**: Register a new pet owner and verify access

1. **Navigate to Auth Page**
   ```
   URL: http://localhost:5173/auth.html
   ```

2. **Fill Registration Form**
   - Click "Register" tab
   - Role: Select "🐾 Pet Owner (Client)"
   - Full Name: `John Smith`
   - Email: `john.smith@example.com`
   - Password: `password123`
   - Confirm Password: `password123`

3. **Submit and Verify**
   - Click "Create Account"
   - ✅ Should see: "Client account created successfully! Redirecting..."
   - ✅ Should redirect to `/app.html` in 0.5 seconds
   - ✅ Should see green "Client" badge in top right
   - ✅ Should see "Good morning, John!" in dashboard
   - ✅ Avatar should show "JS"

4. **Check Browser Storage**
   - Open DevTools → Application → Local Storage
   - ✅ Should see `access_token` with JWT value
   - ✅ Should see `user_role` = "client"

5. **Verify API Call**
   - Check Network tab
   - ✅ POST to `/api/v1/auth/register` returned 201
   - ✅ Response contains `access_token` and `token_type: "bearer"`

### Test 2: Staff Registration Flow
**Objective**: Register clinic staff and verify admin access

1. **Navigate to Auth Page**
   ```
   URL: http://localhost:5173/auth.html
   ```

2. **Fill Registration Form**
   - Click "Register" tab
   - Role: Select "👨‍⚕️ Clinic Staff (Admin)"
   - Full Name: `Dr. Sarah Johnson`
   - Email: `sarah.johnson@example.com`
   - Password: `staffpass123`
   - Confirm Password: `staffpass123`

3. **Submit and Verify**
   - Click "Create Account"
   - ✅ Should see: "Staff account created successfully! Redirecting..."
   - ✅ Should redirect to `/app.html` in 0.5 seconds
   - ✅ Should see amber "Staff" badge in top right
   - ✅ Should see "Good morning, Sarah!" in dashboard
   - ✅ Avatar should show "DS"

4. **Check Backend Email Conversion**
   - Open backend logs
   - ✅ Should see email converted to: `admin+sarah.johnson@vetclinic.com`
   - ✅ Should see role assigned as: "admin"

5. **Verify Admin Access**
   - Check profile page
   - ✅ Role should show "Clinic Staff"
   - ✅ Should have access to admin features

### Test 3: Login Flow (Existing User)
**Objective**: Test login with previously registered account

1. **Logout First**
   - Click avatar in top right
   - Confirm logout
   - ✅ Should redirect to `/auth.html`
   - ✅ Local storage should be cleared

2. **Login as Client**
   - Email: `john.smith@example.com`
   - Password: `password123`
   - Click "Sign In"

3. **Verify Login**
   - ✅ Should see: "Login successful! Redirecting..."
   - ✅ Should redirect in 0.5 seconds
   - ✅ Should see green "Client" badge
   - ✅ Dashboard loads with user data

4. **Test Staff Login**
   - Logout again
   - Email: `admin+sarah.johnson@vetclinic.com` (converted email)
   - Password: `staffpass123`
   - Click "Sign In"
   - ✅ Should see amber "Staff" badge

### Test 4: Validation Tests
**Objective**: Verify form validation works correctly

1. **Test Missing Role**
   - Go to Register tab
   - Leave role dropdown as "Select your role"
   - Fill other fields
   - Click "Create Account"
   - ✅ Should see error: "Please select whether you are a Pet Owner or Clinic Staff"

2. **Test Password Mismatch**
   - Select a role
   - Password: `password123`
   - Confirm: `password456`
   - Click "Create Account"
   - ✅ Should see error: "Passwords do not match"

3. **Test Short Password**
   - Password: `pass` (less than 8 chars)
   - ✅ HTML5 validation should prevent submission
   - ✅ Should see browser message about minimum length

4. **Test Invalid Email**
   - Email: `notanemail`
   - ✅ HTML5 validation should prevent submission
   - ✅ Should see browser message about email format

5. **Test Duplicate Email**
   - Try to register with `john.smith@example.com` again
   - ✅ Should see error: "Email already registered"

### Test 5: Invalid Login Tests
**Objective**: Verify security measures work

1. **Test Wrong Password**
   - Email: `john.smith@example.com`
   - Password: `wrongpassword`
   - Click "Sign In"
   - ✅ Should see error: "Invalid email or password"
   - ✅ Should NOT redirect

2. **Test Non-existent User**
   - Email: `nobody@example.com`
   - Password: `password123`
   - Click "Sign In"
   - ✅ Should see error: "Invalid email or password"

3. **Test Empty Fields**
   - Leave email empty
   - ✅ HTML5 validation should prevent submission

### Test 6: Token & Session Tests
**Objective**: Verify JWT token handling

1. **Test Protected Route Access**
   - Logout completely
   - Try to access: `http://localhost:5173/app.html` directly
   - ✅ Should redirect to `/auth.html`

2. **Test Token Expiration**
   - Login successfully
   - In DevTools, modify `access_token` to invalid value
   - Refresh `/app.html`
   - ✅ Should redirect to `/auth.html`

3. **Test Logout Token Blacklist**
   - Login successfully
   - Copy the `access_token` from localStorage
   - Logout
   - Try to use the copied token in API request
   - ✅ Should get 401 Unauthorized
   - ✅ Error: "Token has been invalidated"

### Test 7: UI/UX Tests
**Objective**: Verify user experience quality

1. **Test Loading States**
   - Click "Sign In" or "Create Account"
   - ✅ Button should show "Signing in..." or "Creating account..."
   - ✅ Button should be disabled during request
   - ✅ Should not allow double-submission

2. **Test Success Messages**
   - Complete registration
   - ✅ Green success alert should appear
   - ✅ Message should be clear and specific
   - ✅ Should auto-dismiss before redirect

3. **Test Error Messages**
   - Trigger various errors
   - ✅ Red error alert should appear
   - ✅ Messages should be helpful
   - ✅ Should stay visible until dismissed or new action

4. **Test Tab Switching**
   - Switch between Login and Register tabs
   - ✅ Forms should switch smoothly
   - ✅ Alerts should clear when switching
   - ✅ Form data should reset

5. **Test Role Badge**
   - Login as client
   - ✅ Badge should be green with "Client" text
   - Login as staff
   - ✅ Badge should be amber with "Staff" text

### Test 8: Backend Integration Tests
**Objective**: Verify backend API responses

1. **Test Registration API**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "full_name": "Test User",
       "email": "test@example.com",
       "password": "testpass123"
     }'
   ```
   - ✅ Should return 201 Created
   - ✅ Should include `access_token`

2. **Test Login API**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "password": "testpass123"
     }'
   ```
   - ✅ Should return 200 OK
   - ✅ Should include `access_token`

3. **Test Protected Endpoint**
   ```bash
   curl -X GET http://localhost:8000/api/v1/users/me \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```
   - ✅ Should return user data
   - ✅ Should include role information

4. **Test Logout API**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/logout \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```
   - ✅ Should return 200 OK
   - ✅ Message: "Successfully logged out"

### Test 9: Cross-Browser Tests
**Objective**: Ensure compatibility

- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if available)
- [ ] Mobile browsers

For each browser:
- ✅ Registration works
- ✅ Login works
- ✅ Redirect works
- ✅ UI displays correctly
- ✅ Badges show proper colors

### Test 10: Performance Tests
**Objective**: Verify speed and responsiveness

1. **Measure Redirect Time**
   - Use browser DevTools Performance tab
   - ✅ Should redirect within 500-600ms
   - ✅ No unnecessary delays

2. **Measure API Response Time**
   - Check Network tab
   - ✅ Registration: < 500ms
   - ✅ Login: < 300ms
   - ✅ User data fetch: < 200ms

3. **Test Concurrent Registrations**
   - Open multiple tabs
   - Register different users simultaneously
   - ✅ All should succeed
   - ✅ No race conditions

## Common Issues & Solutions

### Issue: "Connection error"
**Solution**: 
- Check backend is running: `http://localhost:8000/health`
- Verify CORS settings in backend `.env`
- Check browser console for CORS errors

### Issue: Redirect not working
**Solution**:
- Check browser console for JavaScript errors
- Verify `window.location.href` is being called
- Check if there are any popup blockers

### Issue: Token not stored
**Solution**:
- Check if localStorage is enabled
- Verify browser privacy settings
- Check for incognito/private mode restrictions

### Issue: Role badge not showing
**Solution**:
- Check if user data is loaded (console.log currentUser)
- Verify API returns role field
- Check CSS for badge element

### Issue: Backend returns 500 error
**Solution**:
- Check backend logs for stack trace
- Verify database connection
- Check if all environment variables are set

## Success Criteria

All tests should pass with:
- ✅ 0 console errors
- ✅ 0 network errors
- ✅ Smooth user experience
- ✅ Fast response times
- ✅ Proper error handling
- ✅ Secure token management
- ✅ Correct role assignment
- ✅ Visual feedback for all actions

## Test Results Template

```
Date: _______________
Tester: _______________
Browser: _______________

Test 1 (Client Registration): ☐ Pass ☐ Fail
Test 2 (Staff Registration): ☐ Pass ☐ Fail
Test 3 (Login Flow): ☐ Pass ☐ Fail
Test 4 (Validation): ☐ Pass ☐ Fail
Test 5 (Invalid Login): ☐ Pass ☐ Fail
Test 6 (Token & Session): ☐ Pass ☐ Fail
Test 7 (UI/UX): ☐ Pass ☐ Fail
Test 8 (Backend Integration): ☐ Pass ☐ Fail
Test 9 (Cross-Browser): ☐ Pass ☐ Fail
Test 10 (Performance): ☐ Pass ☐ Fail

Overall Status: ☐ All Pass ☐ Some Failures

Notes:
_________________________________
_________________________________
_________________________________
```

---

**Last Updated**: February 28, 2026
**Test Version**: 1.0
