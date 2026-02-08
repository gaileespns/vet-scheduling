"""User repository for database operations."""
from sqlmodel import Session, select
from typing import Optional
import uuid

from app.features.users.models import User


class UserRepository:
    """Repository for User database operations.
    
    This class handles all database queries related to users,
    following the repository pattern to abstract data access.
    """
    
    def __init__(self, session: Session):
        """Initialize the repository with a database session.
        
        Args:
            session: SQLModel database session
        """
        self.session = session
    
    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID.
        
        Args:
            user_id: UUID of the user to retrieve
            
        Returns:
            User object if found, None otherwise
        """
        return self.session.get(User, user_id)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address.
        
        Args:
            email: Email address to search for
            
        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()
    
    def create(self, user: User) -> User:
        """Create a new user in the database.
        
        Args:
            user: User object to create
            
        Returns:
            Created User object with database-generated fields populated
        """
        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)
        return user
