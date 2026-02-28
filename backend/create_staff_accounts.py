"""
Script to create 10 staff accounts for the vet clinic system.

This script creates admin users with predefined credentials that staff can use to login.
All staff accounts use the admin@vetclinic.com email pattern to be recognized as admin users.
"""

import asyncio
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from sqlmodel import Session, select
from app.core.database import engine
from app.features.users.models import User
from app.features.pets.models import Pet  # Import Pet model to resolve relationships
from app.features.appointments.models import Appointment  # Import Appointment model
from app.infrastructure.auth import hash_password


# Staff account data
STAFF_ACCOUNTS = [
    {
        "full_name": "Admin1",
        "email": "admin1@vetclinic.com",
        "password": "admin123",
        "role": "admin"
    },
    {
        "full_name": "Admin2",
        "email": "admin2@vetclinic.com",
        "password": "admin123",
        "role": "admin"
    },
    {
        "full_name": "Admin3",
        "email": "admin3@vetclinic.com",
        "password": "admin123",
        "role": "admin"
    },
    {
        "full_name": "Admin4",
        "email": "admin4@vetclinic.com",
        "password": "admin123",
        "role": "admin"
    },
    {
        "full_name": "Admin5",
        "email": "admin5@vetclinic.com",
        "password": "admin123",
        "role": "admin"
    },
    {
        "full_name": "Admin6",
        "email": "admin6@vetclinic.com",
        "password": "admin123",
        "role": "admin"
    },
    {
        "full_name": "Admin7",
        "email": "admin7@vetclinic.com",
        "password": "admin123",
        "role": "admin"
    },
    {
        "full_name": "Admin8",
        "email": "admin8@vetclinic.com",
        "password": "admin123",
        "role": "admin"
    },
    {
        "full_name": "Admin9",
        "email": "admin9@vetclinic.com",
        "password": "admin123",
        "role": "admin"
    },
    {
        "full_name": "Admin10",
        "email": "admin10@vetclinic.com",
        "password": "admin123",
        "role": "admin"
    }
]


def create_staff_accounts():
    """Create staff accounts in the database."""
    
    print("=" * 60)
    print("Creating Staff Accounts for PawCare Vet Clinic")
    print("=" * 60)
    print()
    
    with Session(engine) as session:
        created_count = 0
        skipped_count = 0
        
        for staff_data in STAFF_ACCOUNTS:
            # Check if user already exists
            existing_user = session.exec(
                select(User).where(User.email == staff_data["email"])
            ).first()
            
            if existing_user:
                print(f"⏭️  Skipped: {staff_data['full_name']} ({staff_data['email']}) - Already exists")
                skipped_count += 1
                continue
            
            # Create new staff user
            hashed_password = hash_password(staff_data["password"])
            
            new_user = User(
                full_name=staff_data["full_name"],
                email=staff_data["email"],
                hashed_password=hashed_password,
                role=staff_data["role"],
                is_active=True
            )
            
            session.add(new_user)
            print(f"✅ Created: {staff_data['full_name']} ({staff_data['email']})")
            created_count += 1
        
        # Commit all changes
        session.commit()
        
        print()
        print("=" * 60)
        print(f"Summary:")
        print(f"  ✅ Created: {created_count} accounts")
        print(f"  ⏭️  Skipped: {skipped_count} accounts (already exist)")
        print("=" * 60)
        print()
        print("Staff Login Credentials:")
        print("-" * 60)
        for staff in STAFF_ACCOUNTS:
            print(f"  Email:    {staff['email']}")
            print(f"  Password: {staff['password']}")
            print(f"  Name:     {staff['full_name']}")
            print()
        print("=" * 60)
        print()
        print("✨ All staff can now login using their credentials!")
        print()


if __name__ == "__main__":
    try:
        create_staff_accounts()
    except Exception as e:
        print(f"❌ Error creating staff accounts: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
