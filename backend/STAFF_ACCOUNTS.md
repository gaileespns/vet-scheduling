# Staff Accounts for PawCare Vet Clinic

This document contains the login credentials for all staff accounts.

## Creating Staff Accounts

To create the staff accounts, run the following command from the `backend` directory:

```bash
python create_staff_accounts.py
```

This will create 10 staff accounts in the database.

## Staff Login Credentials

All staff accounts use the password: `admin123`

| Name | Email | Password |
|------|-------|----------|
| Admin1 | admin1@vetclinic.com | admin123 |
| Admin2 | admin2@vetclinic.com | admin123 |
| Admin3 | admin3@vetclinic.com | admin123 |
| Admin4 | admin4@vetclinic.com | admin123 |
| Admin5 | admin5@vetclinic.com | admin123 |
| Admin6 | admin6@vetclinic.com | admin123 |
| Admin7 | admin7@vetclinic.com | admin123 |
| Admin8 | admin8@vetclinic.com | admin123 |
| Admin9 | admin9@vetclinic.com | admin123 |
| Admin10 | admin10@vetclinic.com | admin123 |

## How Staff Login Works

1. Staff members use their email and password to login at `/auth.html`
2. The system recognizes emails with these patterns as admin users:
   - `admin@vetclinic.com` (main admin)
   - `admin1@vetclinic.com`, `admin2@vetclinic.com`, etc. (numbered admins)
   - `admin+*@vetclinic.com` (admin with any suffix)
3. After login, staff are automatically redirected to the staff dashboard at `/staff-dashboard.html`
4. Staff have full access to:
   - View all appointments
   - Confirm/cancel appointments
   - View all pets and clients
   - Manage clinic operations

## Client Registration

- Clients can register freely at `/auth.html` using any email address
- Client accounts are automatically created with the `pet_owner` role
- Clients are redirected to the client dashboard at `/app.html`
- Clients can only view and manage their own pets and appointments

## Security Notes

- The default password `admin123` should be changed in production
- Staff accounts are pre-created and cannot be registered through the public registration form
- Only emails matching the admin patterns are recognized as staff
