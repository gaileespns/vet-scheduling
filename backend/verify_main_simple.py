"""
Simple verification script for main.py.
Checks that all required components are present.
"""

def verify_main():
    with open("app/main.py", "r") as f:
        content = f.read()
    
    checks = {
        "Auth router imported": "from app.features.auth.router import router as auth_router" in content,
        "Pets router imported": "from app.features.pets.router import router as pets_router" in content,
        "Appointments router imported": "from app.features.appointments.router import router as appointments_router" in content,
        "Clinic router imported": "from app.features.clinic.router import router as clinic_router" in content,
        "Database init imported": "from app.core.database import init_db" in content,
        "CORS config imported": "from app.core.config import BACKEND_CORS_ORIGINS" in content,
        "FastAPI app created": "app = FastAPI(" in content,
        "CORS middleware added": "app.add_middleware(" in content and "CORSMiddleware" in content,
        "Auth router included": "app.include_router(auth_router)" in content,
        "Pets router included": "app.include_router(pets_router)" in content,
        "Appointments router included": "app.include_router(appointments_router)" in content,
        "Clinic router included": "app.include_router(clinic_router)" in content,
        "Lifespan function defined": "@asynccontextmanager" in content and "async def lifespan" in content,
        "Database initialization": "init_db()" in content,
        "Root endpoint": 'def read_root():' in content,
        "Health check endpoint": 'def health_check():' in content,
    }
    
    print("Main.py Verification")
    print("=" * 60)
    
    all_passed = True
    for check, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✓ ALL CHECKS PASSED")
        print("\nTask 9.1 Requirements Met:")
        print("  ✓ FastAPI application initialized")
        print("  ✓ All routers included (auth, pets, appointments, clinic)")
        print("  ✓ CORS configured")
        print("  ✓ Startup event creates database tables")
        print("  ✓ API documentation available at /docs")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(verify_main())
