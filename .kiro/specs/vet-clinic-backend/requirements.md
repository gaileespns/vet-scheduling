# Requirements Document

## Introduction

This document specifies the requirements for a REST API backend system for a single veterinary clinic. The system enables pet owners to register their pets and book appointments, while allowing clinic administrators to manage all resources, appointments, and clinic operational status. The system implements role-based access control with two user types: Admin (clinic owner) and Pet Owners (customers).

## Glossary

- **System**: The Vet Clinic Scheduling System backend API
- **User**: Any authenticated person using the system (Admin or Pet Owner)
- **Admin**: The clinic owner with full system access, identified by matching ADMIN_EMAIL configuration
- **Pet_Owner**: A customer who can manage only their own pets and appointments
- **Pet**: An animal registered in the system with an owner
- **Appointment**: A scheduled visit for a pet at the clinic
- **Clinic_Status**: The operational state of the clinic (open, close, closing_soon)
- **Service_Type**: The type of veterinary service (vaccination, routine, surgery, emergency)
- **Appointment_Status**: The state of an appointment (pending, confirmed, cancelled, completed)
- **Vaccination_Status**: The validity state of a pet's vaccination (valid, expired, unknown)
- **JWT**: JSON Web Token used for authentication
- **Overlapping_Appointment**: Two appointments with time ranges that intersect

## Requirements

### Requirement 1: User Registration and Authentication

**User Story:** As a new user, I want to register an account and log in, so that I can access the system securely.

#### Acceptance Criteria

1. WHEN a user submits registration with email and password, THE System SHALL create a new user account with a hashed password
2. WHEN a user registers with an email matching ADMIN_EMAIL configuration, THE System SHALL assign the role "admin"
3. WHEN a user registers with an email not matching ADMIN_EMAIL configuration, THE System SHALL assign the role "pet_owner"
4. WHEN a user attempts to register with an existing email, THE System SHALL reject the registration and return an error
5. WHEN a user submits valid credentials to login, THE System SHALL return a JWT token
6. WHEN a user submits invalid credentials to login, THE System SHALL reject the login and return an error
7. THE System SHALL hash all passwords using bcrypt before storage
8. THE System SHALL validate email format during registration

### Requirement 2: Role-Based Access Control

**User Story:** As a system administrator, I want different access levels for admins and pet owners, so that users can only perform authorized actions.

#### Acceptance Criteria

1. WHEN an Admin accesses any endpoint, THE System SHALL grant full access to all resources
2. WHEN a Pet_Owner accesses pet endpoints, THE System SHALL restrict access to only their own pets
3. WHEN a Pet_Owner attempts to access another user's pet, THE System SHALL reject the request and return an authorization error
4. WHEN a Pet_Owner attempts to access admin-only endpoints, THE System SHALL reject the request and return an authorization error
5. WHEN a request includes a valid JWT token, THE System SHALL extract the user identity and role
6. WHEN a request includes an invalid or expired JWT token, THE System SHALL reject the request and return an authentication error
7. WHEN a request to a protected endpoint has no JWT token, THE System SHALL reject the request and return an authentication error

### Requirement 3: Pet Registration and Management

**User Story:** As a pet owner, I want to register and manage my pets, so that I can book appointments for them.

#### Acceptance Criteria

1. WHEN a Pet_Owner creates a pet, THE System SHALL associate the pet with the authenticated user as owner
2. WHEN a Pet_Owner lists pets, THE System SHALL return only pets owned by that user
3. WHEN an Admin lists pets, THE System SHALL return all pets in the system
4. WHEN a user retrieves a specific pet, THE System SHALL return the pet details including computed vaccination status
5. WHEN a Pet_Owner updates a pet, THE System SHALL verify the pet belongs to that user before allowing the update
6. WHEN a Pet_Owner deletes a pet, THE System SHALL verify the pet belongs to that user before allowing the deletion
7. WHEN an Admin updates or deletes any pet, THE System SHALL allow the operation
8. THE System SHALL store pet information including name, species, breed, date_of_birth, last_vaccination, and medical_history
9. THE System SHALL store medical_history as a JSON field

### Requirement 4: Vaccination Status Tracking

**User Story:** As a pet owner, I want to see my pet's vaccination status, so that I know when vaccinations are due.

#### Acceptance Criteria

1. WHEN a pet's last_vaccination is NULL, THE System SHALL compute vaccination_status as "unknown"
2. WHEN a pet's last_vaccination is more than 365 days in the past, THE System SHALL compute vaccination_status as "expired"
3. WHEN a pet's last_vaccination is 365 days or less in the past, THE System SHALL compute vaccination_status as "valid"
4. WHEN a pet is retrieved, THE System SHALL include the computed vaccination_status in the response
5. THE System SHALL compute vaccination_status dynamically and not store it in the database

### Requirement 5: Appointment Creation and Validation

**User Story:** As a pet owner, I want to book appointments for my pets, so that they can receive veterinary care.

#### Acceptance Criteria

1. WHEN a user creates an appointment, THE System SHALL verify the pet exists
2. WHEN a Pet_Owner creates an appointment, THE System SHALL verify the pet belongs to that user
3. WHEN an Admin creates an appointment, THE System SHALL allow appointment creation for any pet
4. WHEN a user creates an appointment with a start time in the past, THE System SHALL reject the appointment
5. WHEN a user creates an appointment, THE System SHALL automatically calculate end_time as start_time plus service duration
6. WHEN service_type is "vaccination", THE System SHALL set duration to 30 minutes
7. WHEN service_type is "routine", THE System SHALL set duration to 45 minutes
8. WHEN service_type is "surgery", THE System SHALL set duration to 120 minutes
9. WHEN service_type is "emergency", THE System SHALL set duration to 15 minutes
10. WHEN a user creates an appointment and Clinic_Status is "close", THE System SHALL reject the appointment
11. WHEN a user creates an appointment that overlaps with an existing "pending" or "confirmed" appointment, THE System SHALL reject the appointment
12. WHEN a user creates an appointment with no overlaps and valid conditions, THE System SHALL create the appointment with status "pending"

### Requirement 6: Appointment Status Management

**User Story:** As an admin, I want to manage appointment statuses, so that I can confirm, complete, or track appointment states.

#### Acceptance Criteria

1. WHEN an Admin updates an appointment status to "confirmed", THE System SHALL update the status
2. WHEN an Admin updates an appointment status to "completed", THE System SHALL update the status
3. WHEN a Pet_Owner attempts to update an appointment status to "confirmed", THE System SHALL reject the request
4. WHEN a Pet_Owner attempts to update an appointment status to "completed", THE System SHALL reject the request
5. WHEN a user attempts to update the status of a "completed" appointment, THE System SHALL reject the request
6. WHEN a user attempts to update the status of a "cancelled" appointment, THE System SHALL reject the request
7. WHEN a Pet_Owner cancels their own appointment, THE System SHALL update the status to "cancelled"
8. WHEN a Pet_Owner attempts to cancel another user's appointment, THE System SHALL reject the request
9. WHEN an Admin cancels any appointment, THE System SHALL update the status to "cancelled"
10. WHEN a user attempts to cancel a "completed" appointment, THE System SHALL reject the request

### Requirement 7: Appointment Listing and Filtering

**User Story:** As a user, I want to view and filter appointments, so that I can see relevant scheduled visits.

#### Acceptance Criteria

1. WHEN a Pet_Owner lists appointments, THE System SHALL return only appointments for pets owned by that user
2. WHEN an Admin lists appointments, THE System SHALL return all appointments in the system
3. WHEN a user filters appointments by status, THE System SHALL return only appointments matching that status
4. WHEN a user filters appointments by from_date, THE System SHALL return only appointments starting on or after that date
5. WHEN a user filters appointments by to_date, THE System SHALL return only appointments starting on or before that date
6. WHEN a user applies multiple filters, THE System SHALL return appointments matching all filter criteria

### Requirement 8: Clinic Status Management

**User Story:** As an admin, I want to manage the clinic's operational status, so that I can control when appointments can be booked.

#### Acceptance Criteria

1. WHEN anyone requests the clinic status, THE System SHALL return the current status without requiring authentication
2. WHEN an Admin updates the clinic status, THE System SHALL update the status to the provided value
3. WHEN a Pet_Owner attempts to update the clinic status, THE System SHALL reject the request
4. THE System SHALL support clinic status values: "open", "close", "closing_soon"
5. WHEN Clinic_Status is "close", THE System SHALL prevent new appointment creation

### Requirement 9: Overlap Detection for Appointments

**User Story:** As a system, I want to prevent double-booking, so that the clinic can manage resources effectively.

#### Acceptance Criteria

1. WHEN checking for overlaps, THE System SHALL consider only "pending" and "confirmed" appointments
2. WHEN checking for overlaps, THE System SHALL ignore "cancelled" and "completed" appointments
3. WHEN two appointments have overlapping time ranges, THE System SHALL identify them as Overlapping_Appointment
4. WHEN appointment A starts before appointment B ends AND appointment A ends after appointment B starts, THE System SHALL identify them as overlapping
5. WHEN appointments have adjacent times with no overlap, THE System SHALL allow both appointments

### Requirement 10: Data Validation and Error Handling

**User Story:** As a developer, I want comprehensive validation and error handling, so that the API provides clear feedback.

#### Acceptance Criteria

1. WHEN invalid data is submitted, THE System SHALL return a validation error with specific field information
2. WHEN a resource is not found, THE System SHALL return a 404 error with a descriptive message
3. WHEN authorization fails, THE System SHALL return a 403 error with a descriptive message
4. WHEN authentication fails, THE System SHALL return a 401 error with a descriptive message
5. THE System SHALL validate all required fields are present in requests
6. THE System SHALL validate data types match expected types
7. THE System SHALL validate enum values are within allowed sets
8. WHEN an unexpected error occurs, THE System SHALL return a 500 error and log the error details

### Requirement 11: API Documentation

**User Story:** As a developer, I want auto-generated API documentation, so that I can understand and test the API easily.

#### Acceptance Criteria

1. THE System SHALL provide interactive API documentation at /docs endpoint
2. THE System SHALL document all request schemas with field descriptions
3. THE System SHALL document all response schemas with field descriptions
4. THE System SHALL document all error responses
5. THE System SHALL allow testing API endpoints directly from the documentation interface

### Requirement 12: Database Schema and Persistence

**User Story:** As a system, I want to persist data reliably, so that information is not lost.

#### Acceptance Criteria

1. THE System SHALL store user data in a users table with fields: id, email, hashed_password, role, created_at
2. THE System SHALL store pet data in a pets table with fields: id, name, species, breed, date_of_birth, last_vaccination, medical_history, owner_id, created_at, updated_at
3. THE System SHALL store appointment data in an appointments table with fields: id, pet_id, user_id, start_time, end_time, service_type, status, notes, created_at, updated_at
4. THE System SHALL store clinic status in a clinic_status table with fields: id, status, updated_at
5. THE System SHALL enforce foreign key relationships between tables
6. THE System SHALL use PostgreSQL as the database engine
7. THE System SHALL use SQLModel for ORM operations
8. WHEN the application starts, THE System SHALL create all required database tables if they do not exist

### Requirement 13: Three-Layer Architecture

**User Story:** As a developer, I want a clean architecture, so that the codebase is maintainable and testable.

#### Acceptance Criteria

1. THE System SHALL implement a Repository layer for all database operations
2. THE System SHALL implement a Service layer for all business logic
3. THE System SHALL implement a Router layer for all HTTP endpoint handling
4. WHEN a router receives a request, THE System SHALL delegate business logic to the service layer
5. WHEN a service needs data, THE System SHALL delegate database operations to the repository layer
6. THE System SHALL not allow routers to directly access repositories
7. THE System SHALL not allow repositories to contain business logic
8. THE System SHALL use dependency injection for layer communication
