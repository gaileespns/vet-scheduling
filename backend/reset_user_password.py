"""Reset password for a specific user"""
import sys
from sqlalchemy import text
from app.core.database import engine
from app.infrastructure.auth import hash_password

def reset_password(email: str, new_password: str):
    """Reset password for a user using raw SQL to avoid model relationship issues"""
    
    try:
        # Hash new password
        hashed = hash_password(new_password)
        
        # Use raw SQL to update password
        with engine.connect() as conn:
            # Check if user exists
            result = conn.execute(
                text("SELECT email FROM users WHERE email = :email"),
                {"email": email}
            )
            user = result.fetchone()
            
            if not user:
                print(f"❌ User not found: {email}")
                return False
            
            # Update password
            conn.execute(
                text("UPDATE users SET hashed_password = :hashed WHERE email = :email"),
                {"hashed": hashed, "email": email}
            )
            conn.commit()
        
        print(f"✅ Password reset successful for {email}")
        print(f"   New password: {new_password}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python reset_user_password.py <email> <new_password>")
        print("Example: python reset_user_password.py user@example.com newpass123")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    
    reset_password(email, password)
