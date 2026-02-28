# Vet Clinic Frontend

A modern, responsive veterinary clinic management application with separate dashboards for clients and staff. Built with vanilla HTML, CSS, and JavaScript for simplicity and performance.

## 🚀 Quick Start

```bash
# Install dependencies (for development server only)
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

The application will be available at `http://localhost:5173`

## 📋 Prerequisites

- Node.js 18+ or higher (for development server)
- npm 9+ or higher (for development server)
- Backend API running on `http://localhost:8000` or deployed URL

## 🏗️ Architecture

### Simple, Performant Structure

```
frontend/
├── public/                 # Static HTML pages
│   ├── landing.html       # Landing page
│   ├── auth.html          # Login/Register page
│   ├── app.html           # Client dashboard
│   └── staff-dashboard.html # Staff dashboard
├── src/                   # React components (legacy)
├── .env                   # Environment variables
└── package.json           # Dependencies
```

### Technology Stack

- **Vanilla HTML/CSS/JavaScript** - No framework overhead
- **CSS Variables** - Consistent theming
- **LocalStorage** - Client-side state management
- **JWT Authentication** - Secure token-based auth
- **Fetch API** - Native HTTP requests

## 🎨 Styling System

### Vanilla CSS with CSS Variables

No CSS framework dependencies! The app uses a custom CSS system with:

- **CSS Variables** for consistent theming
- **Component Classes** for reusable patterns
- **Utility Classes** for common layouts
- **Responsive Design** with media queries

#### CSS Variables
```css
--color-primary: #2563eb
--color-success: #16a34a
--color-danger: #dc2626
--spacing-md: 1rem
--radius-lg: 0.75rem
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1)
```

#### Component Classes
```css
.btn, .btn-primary, .btn-sm
.input, .input-group, .input-label
.card, .card-header, .card-body
.modal, .modal-backdrop
.alert, .alert-success
.badge, .badge-primary
```

## 🎯 Key Features

### 🔐 Authentication & Authorization
- **Client-only registration** - Simplified registration flow
- **Secure login** with JWT tokens
- **Token blacklisting** on logout
- **Role-based access** (Admin/Client)
- **10 pre-created staff accounts** (Admin1-Admin10)

### 👤 Client Dashboard (`app.html`)
- **Pet Management**
  - Add, edit, and delete pets
  - Track species, breed, date of birth, and notes
  - Vaccination status (Unvaccinated/Vaccinated)
  - Sex tracking (Male/Female/Unknown)
- **Appointment Booking**
  - Book appointments with available time slots
  - Respects clinic hours (no booking on closed days)
  - Service types: Vaccination (30min), Routine (45min), Surgery (120min), Emergency (15min)
  - View upcoming appointments
  - Reschedule appointments
  - Cancel appointments
- **Profile Management**
  - View and update profile information
  - Email, phone, and full name
- **Dashboard Stats**
  - Upcoming appointments count
  - Total pets registered
  - Next visit information
  - Total visits count

### 👨‍⚕️ Staff Dashboard (`staff-dashboard.html`)
- **Three-Tab Interface**
  - **Dashboard Tab**: Calendar view and statistics
  - **All Appointments Tab**: Complete appointment list with filters
  - **Settings Tab**: Clinic hours management
- **Appointment Management**
  - View all appointments with pet and owner details
  - Filter by status: All, Pending, Confirmed, Today, Completed
  - Confirm pending appointments
  - Complete confirmed appointments
  - Cancel appointments
  - Calendar view with appointment details
- **Clinic Hours Management**
  - Set hours for Monday-Friday, Saturday, Sunday
  - Mark days as closed
  - Hours saved to localStorage
  - Automatically controls booking availability
- **Statistics Dashboard**
  - Pending appointments count
  - Confirmed appointments count
  - Today's appointments count
  - Total appointments count
- **Calendar View**
  - Monthly calendar with appointment indicators
  - Shows appointment times and pet names
  - Color-coded by status (pending/confirmed)
  - Click date to filter appointments

### 🏥 Clinic Hours Integration
- **Staff sets hours** in Settings tab
- **Client booking respects hours** automatically
- **Closed days blocked** from booking
- **Time slots filtered** to match clinic hours
- **Default hours**: Mon-Fri 8AM-8PM, Sat 9AM-5PM, Sun Closed

### 🎨 Design System
- **Consistent color palette** - Forest green, sage, amber accents
- **Playfair Display** - Elegant serif for headings
- **Instrument Sans** - Clean sans-serif for body
- **Responsive design** - Mobile, tablet, desktop optimized
- **Custom modals** - No browser confirm dialogs
- **Toast notifications** - User feedback system

## 🔧 Technology Stack

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with variables
- **Vanilla JavaScript** - No framework dependencies
- **Vite** - Development server and build tool
- **LocalStorage** - Client-side data persistence
- **Fetch API** - HTTP requests
- **JWT** - Token-based authentication

## 📁 File Structure

### `/public` - Application Pages

```
public/
├── landing.html           # Landing page with features
├── auth.html             # Login/Register (client-only)
├── app.html              # Client dashboard
└── staff-dashboard.html  # Staff dashboard
```

### Page Responsibilities

**landing.html**
- Marketing page
- Feature showcase
- Call-to-action buttons
- Navigation to auth

**auth.html**
- Client registration (no role selection)
- Login for both clients and staff
- Auto-redirect based on role
- Password validation (min 8 chars)

**app.html** (Client Dashboard)
- Pet management (CRUD)
- Appointment booking with clinic hours check
- Profile management
- Dashboard statistics
- Tab navigation (Dashboard, Appointments, Pets, Profile)

**staff-dashboard.html** (Staff Dashboard)
- Three-tab interface (Dashboard, All Appointments, Settings)
- Appointment management (confirm, complete, cancel)
- Calendar view with appointment details
- Clinic hours management
- Statistics dashboard
- Filter appointments by status

## 🔐 Authentication Flow

### Registration (Client Only)
1. User fills registration form (email, password, full name)
2. Backend creates user with `pet_owner` role
3. Auto-login after registration
4. JWT token stored in localStorage
5. Redirect to client dashboard

### Login (Client or Staff)
1. User enters credentials
2. Backend validates and returns JWT token
3. Token stored in localStorage
4. User profile fetched to determine role
5. **Auto-redirect based on role:**
   - `admin` → `/staff-dashboard.html`
   - `pet_owner` → `/app.html`

### Logout
1. User clicks logout button
2. Custom modal confirms action
3. Token sent to backend for blacklisting
4. Token removed from localStorage
5. Redirect to auth page

### Staff Accounts
Pre-created admin accounts:
- **Usernames**: Admin1, Admin2, ..., Admin10
- **Emails**: admin1@vetclinic.com, admin2@vetclinic.com, etc.
- **Password**: `admin123` (all accounts)
- **Role**: `admin` (auto-assigned by backend)

## 🌐 API Integration

### Environment Configuration

Create `.env` file in frontend directory:

```env
# Development
VITE_API_BASE_URL=http://localhost:8000

# Production (example)
# VITE_API_BASE_URL=https://vet-scheduling-uiob.onrender.com
```

### API Base URL Detection

The application automatically detects the environment:

```javascript
const API_BASE_URL = location.hostname.includes("localhost")
  ? "http://localhost:8000"
  : "https://vet-scheduling-uiob.onrender.com";
```

### Authentication Headers

All authenticated requests include JWT token:

```javascript
const response = await fetch(`${API_BASE_URL}/api/v1/pets`, {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

### Error Handling

Consistent error handling across all pages:

```javascript
try {
  const response = await fetch(url, options);
  if (!response.ok) {
    const error = await response.json();
    showToast(error.detail || 'Operation failed', '❌');
    return;
  }
  // Success handling
} catch (error) {
  console.error('Error:', error);
  showToast('Connection error', '❌');
}
```

## 📱 Responsive Design

The application is fully responsive with breakpoints:

- **Mobile** (< 768px): 
  - Single column layouts
  - Stacked navigation
  - Touch-friendly buttons
  - Simplified calendar view
  
- **Tablet** (768px - 1024px):
  - 2-column grids
  - Side-by-side cards
  - Optimized spacing
  
- **Desktop** (> 1024px):
  - 3-4 column grids
  - Full navigation
  - Maximum content density
  - Enhanced calendar view

### Design Tokens

```css
/* Colors */
--forest: #1e3a2f;        /* Primary dark */
--sage: #7aaa85;          /* Primary light */
--amber: #c8843a;         /* Accent */
--cream: #f8f3ec;         /* Background */

/* Spacing */
--radius: 16px;           /* Border radius */
--shadow-sm: 0 2px 8px rgba(30,58,47,0.07);
--shadow-md: 0 8px 28px rgba(30,58,47,0.11);

/* Typography */
font-family: 'Playfair Display', serif;  /* Headings */
font-family: 'Instrument Sans', sans-serif;  /* Body */
```

## 🧪 Development Guidelines

### Code Organization

Each HTML file is self-contained with:
- Inline CSS in `<style>` tags
- Inline JavaScript in `<script>` tags
- No external dependencies (except fonts)

### Adding New Features

1. **Identify the page** (client or staff dashboard)
2. **Add HTML structure** in appropriate section
3. **Style with CSS** using existing variables
4. **Implement JavaScript** following existing patterns
5. **Test responsiveness** on all breakpoints

### JavaScript Patterns

**API Calls:**
```javascript
async function loadData() {
  const token = localStorage.getItem('access_token');
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/endpoint`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (response.ok) {
      const data = await response.json();
      // Handle success
    }
  } catch (error) {
    console.error('Error:', error);
    showToast('Error message', '❌');
  }
}
```

**Modal Management:**
```javascript
function openModal(id) {
  document.getElementById(id).classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal(id) {
  document.getElementById(id).classList.remove('open');
  document.body.style.overflow = '';
}
```

**Toast Notifications:**
```javascript
showToast('Success message', '✓');
showToast('Error message', '❌');
showToast('Warning message', '⚠️');
```

### CSS Patterns

**Cards:**
```css
.card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}
```

**Buttons:**
```css
.btn-primary {
  background: var(--forest);
  color: white;
  padding: 10px 20px;
  border-radius: 10px;
}
```

**Forms:**
```css
.form-input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
}
```

## 🚦 Available Scripts

```bash
# Development
npm run dev          # Start Vite dev server (port 5173)

# Production
npm run build        # Build static files to dist/
npm run preview      # Preview production build

# No linting or testing configured (vanilla JS)
```

## 🔗 API Endpoints Used

### Authentication
- `POST /api/v1/auth/register` - Register new client
- `POST /api/v1/auth/login` - Login (client or staff)
- `POST /api/v1/auth/logout` - Logout and blacklist token

### Users
- `GET /api/v1/users/profile` - Get current user profile
- `PATCH /api/v1/users/profile` - Update user profile
- `GET /api/v1/users` - List all users (admin only, for staff dashboard)

### Pets
- `GET /api/v1/pets` - List pets (filtered by role)
- `POST /api/v1/pets` - Create new pet
- `GET /api/v1/pets/{id}` - Get pet by ID
- `PATCH /api/v1/pets/{id}` - Update pet
- `DELETE /api/v1/pets/{id}` - Delete pet

### Appointments
- `GET /api/v1/appointments` - List appointments (with filters)
- `GET /api/v1/appointments/available-slots` - Get available time slots
- `POST /api/v1/appointments` - Create appointment
- `PATCH /api/v1/appointments/{id}/status` - Update status (admin only)
- `PATCH /api/v1/appointments/{id}/reschedule` - Reschedule appointment
- `DELETE /api/v1/appointments/{id}` - Cancel appointment

### Clinic (Not currently used in frontend)
- `GET /api/v1/clinic/status` - Get clinic status (public)
- `PATCH /api/v1/clinic/status` - Update status (admin only)

**Note:** Clinic hours are managed client-side in localStorage, not via API.

## 🐛 Troubleshooting

### API Connection Issues

**Error**: `Failed to fetch` or CORS errors

**Solution**: 
- Ensure backend is running
- Check API_BASE_URL in code matches backend
- Verify CORS settings in backend allow frontend origin
- Check browser console for specific error

### Authentication Issues

**Error**: `401 Unauthorized` or redirect loops

**Solution**:
- Token may be expired (24 hours default)
- Token may be blacklisted after logout
- Clear localStorage and login again:
  ```javascript
  localStorage.clear();
  ```
- Check if backend JWT_SECRET_KEY changed

### Staff Dashboard Not Loading

**Error**: "No appointments found" when appointments exist

**Solution**:
- Check browser console for errors
- Verify `/api/v1/users` endpoint is accessible (admin only)
- Ensure user has admin role
- Check network tab for failed requests

### Booking Not Working

**Error**: No time slots available or "Clinic is closed"

**Solution**:
- Check clinic hours in staff dashboard Settings tab
- Verify selected date is not marked as closed
- Ensure selected date is in the future
- Check if time slots fall within clinic hours

### Modal Not Closing

**Error**: Modal stays open or multiple modals stack

**Solution**:
- Check for JavaScript errors in console
- Ensure modal overlay has correct ID
- Verify closeModal() function is called
- Refresh page to reset state

### LocalStorage Issues

**Error**: Settings not persisting or data loss

**Solution**:
- Check browser allows localStorage
- Verify not in private/incognito mode
- Check localStorage size limits
- Clear and reset:
  ```javascript
  localStorage.removeItem('clinicHours');
  localStorage.removeItem('access_token');
  ```

## 🎯 Environment Variables

Create a `.env` file in the frontend directory:

```env
# API Configuration (optional - auto-detected)
VITE_API_BASE_URL=http://localhost:8000

# Production example
# VITE_API_BASE_URL=https://vet-scheduling-uiob.onrender.com
```

**Note:** The application auto-detects environment based on hostname, so `.env` is optional.

## 📦 Dependencies

### Production Dependencies
- None! Pure vanilla HTML/CSS/JavaScript

### Development Dependencies
- `vite` - Development server and build tool
- `@vitejs/plugin-react-swc` - React plugin (legacy, not used)

### External Resources
- **Google Fonts** - Playfair Display & Instrument Sans
- **Backend API** - FastAPI REST API

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

Output will be in the `dist/` directory containing:
- `landing.html`
- `auth.html`
- `app.html`
- `staff-dashboard.html`
- Other static assets

### Deploy to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Set environment variable: `VITE_API_BASE_URL=your-backend-url`

Or use Vercel dashboard:
- Connect GitHub repository
- Set build command: `npm run build`
- Set output directory: `dist`
- Add environment variable

### Deploy to Netlify

1. Install Netlify CLI: `npm i -g netlify-cli`
2. Run: `netlify deploy --prod --dir=dist`

Or use Netlify dashboard:
- Connect GitHub repository
- Set build command: `npm run build`
- Set publish directory: `dist`
- Add environment variable

### Deploy to Static Hosting

The `dist/` folder contains static HTML files that can be hosted anywhere:
- GitHub Pages
- AWS S3 + CloudFront
- Azure Static Web Apps
- Google Cloud Storage
- Any static file server

### Important: Update API URL

For production, update the API_BASE_URL in each HTML file:

```javascript
// Change from auto-detection to hardcoded production URL
const API_BASE_URL = "https://your-backend-api.com";
```

Or use environment variable replacement during build.

## 📚 Additional Documentation

- `QUICKSTART.md` - Quick start guide
- `backend/README.md` - Backend API documentation
- `backend/STAFF_ACCOUNTS.md` - Staff account details
- `CLINIC_HOURS_INTEGRATION.md` - Clinic hours feature documentation

## 🤝 Contributing

1. Follow the existing code structure
2. Use vanilla JavaScript (no frameworks)
3. Maintain consistent styling with CSS variables
4. Keep HTML files self-contained
5. Test on multiple screen sizes
6. Write descriptive commit messages

## 📄 License

[Your License Here]

## 👥 Support

For issues and questions:
1. Check this README
2. Review `backend/README.md` for API details
3. Check browser console for errors
4. Review network tab for API issues
5. Check localStorage for token/data issues

## 🎉 Success Checklist

- [ ] Backend running and accessible
- [ ] Frontend running on port 5173
- [ ] Can access landing page
- [ ] Can register new client
- [ ] Can login as client
- [ ] Can login as staff (admin1@vetclinic.com / admin123)
- [ ] Client can add pets
- [ ] Client can book appointments
- [ ] Client can update profile
- [ ] Staff can view all appointments
- [ ] Staff can confirm appointments
- [ ] Staff can set clinic hours
- [ ] Booking respects clinic hours
- [ ] Calendar shows appointments
- [ ] Filters work correctly

## 🔑 Key Differences from React Version

This version uses vanilla HTML/CSS/JavaScript instead of React:

**Advantages:**
- ✅ No build step required for development
- ✅ Faster page loads (no framework overhead)
- ✅ Simpler deployment (static files)
- ✅ Easier to understand for beginners
- ✅ No dependency management issues

**Trade-offs:**
- ❌ More code duplication
- ❌ Manual DOM manipulation
- ❌ No component reusability
- ❌ No type safety (no TypeScript)

---

Built with ❤️ using vanilla HTML, CSS, and JavaScript
