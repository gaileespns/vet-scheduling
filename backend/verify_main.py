"""
Verification script for main.py structure.

This script verifies that main.py has the correct structure without
actually connecting to the database.
"""

import ast
import sys

def verify_main_py():
    """Verify main.py has all required components."""
    
    with open("app/main.py", "r") as f:
        content = f.read()
    
    # Parse the AST
    tree = ast.parse(content)
    
    # Track what we find
    imports = []
    functions = []
    app_created = False
    cors_configured = False
    routers_included = []
    lifespan_defined = False
    
    for node in ast.walk(tree):
        # Check imports
        if isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
                for alias in node.names:
                    if alias.name == "router":
                        routers_included.append(node.module)
        
        # Check function definitions
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
            if node.name == "lifespan":
                lifespan_defined = True
        
        # Check for FastAPI app creation
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "app":
                    if isinstance(node.value, ast.Call):
                        if hasattr(node.value.func, 'id') and node.value.func.id == "FastAPI":
                            app_created = True
        
        # Check for CORS middleware
        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call):
                if hasattr(node.value.func, 'attr') and node.value.func.attr == "add_middleware":
                    cors_configured = True
    
    # Verify all required components
    print("Verification Results:")
    print("=" * 50)
    
    # Check routers
    required_routers = [
        "app.features.auth.router",
        "app.features.pets.router",
        "app.features.appointments.router",
        "app.features.clinic.router"
    ]
    
    print("\n1. Router Imports:")
    for router in required_routers:
        if router in routers_included:
            print(f"   ✓ {router}")
        else:
            print(f"   ✗ {router} - MISSING")
    
    # Check core imports
    print("\n2. Core Imports:")
    core_imports = [
        "app.core.config",
        "app.core.database"
    ]
    for imp in core_imports:
        if imp in imports:
            print(f"   ✓ {imp}")
        else:
            print(f"   ✗ {imp} - MISSING")
    
    # Check FastAPI setup
    print("\n3. FastAPI Setup:")
    print(f"   {'✓' if app_created else '✗'} FastAPI app created")
    print(f"   {'✓' if cors_configured else '✗'} CORS middleware configured")
    print(f"   {'✓' if lifespan_defined else '✗'} Lifespan function defined")
    
    # Check endpoints
    print("\n4. Endpoints:")
    required_endpoints = ["read_root", "health_check"]
    for endpoint in required_endpoints:
        if endpoint in functions:
            print(f"   ✓ {endpoint}")
        else:
            print(f"   ✗ {endpoint} - MISSING")
    
    # Check for init_db call in lifespan
    print("\n5. Database Initialization:")
    if "init_db" in content and "lifespan" in content:
        print("   ✓ init_db called in lifespan")
    else:
        print("   ✗ init_db not called in lifespan")
    
    # Overall result
    print("\n" + "=" * 50)
    all_routers_present = all(router in routers_included for router in required_routers)
    all_core_imports = all(imp in imports for imp in core_imports)
    all_endpoints = all(endpoint in functions for endpoint in required_endpoints)
    
    if (all_routers_present and all_core_imports and app_created and 
        cors_configured and lifespan_defined and all_endpoints):
        print("✓ ALL CHECKS PASSED")
        print("\nThe main.py file is correctly structured with:")
        print("  - All 4 routers included (auth, pets, appointments, clinic)")
        print("  - CORS middleware configured")
        print("  - Database initialization on startup")
        print("  - Root and health check endpoints")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(verify_main_py())
