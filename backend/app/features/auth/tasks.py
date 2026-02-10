"""Background tasks for authentication and token management.

This module contains background tasks that can be scheduled to run periodically
for maintenance operations like cleaning up expired tokens from the blacklist.

Requirements:
    - 7.3: Provide mechanism to periodically remove expired tokens
    - 7.4: Delete expired tokens from Token_Blacklist
"""

import logging
from typing import Optional
from sqlmodel import Session

from app.core.database import engine
from app.features.auth.repository import TokenBlacklistRepository

logger = logging.getLogger(__name__)


def cleanup_expired_tokens(session: Optional[Session] = None) -> int:
    """Remove expired tokens from the blacklist.
    
    This function creates a database session (or uses the provided one) and calls
    the repository method to remove all tokens whose expiration timestamp has passed.
    It logs the number of tokens removed for monitoring and auditing purposes.
    
    This task should be scheduled to run periodically (e.g., daily) to prevent
    the token blacklist from growing indefinitely with expired tokens.
    
    Args:
        session: Optional database session. If not provided, creates a new session.
                 This parameter is primarily for testing purposes.
    
    Returns:
        Number of tokens removed from the blacklist
        
    Requirements:
        - 7.3: Provide mechanism to periodically remove expired tokens
        - 7.4: Delete all records where expiration timestamp is earlier than current time
        
    Example:
        >>> count = cleanup_expired_tokens()
        >>> print(f"Removed {count} expired tokens")
    """
    logger.info("Starting cleanup of expired tokens from blacklist")
    
    try:
        # Use provided session or create a new one
        if session is not None:
            # Use the provided session (for testing)
            token_blacklist_repo = TokenBlacklistRepository(session)
            removed_count = token_blacklist_repo.remove_expired_tokens()
            session.commit()
            logger.info(f"Successfully removed {removed_count} expired token(s) from blacklist")
            return removed_count
        else:
            # Create a database session for the cleanup operation (for production)
            with Session(engine) as db_session:
                # Initialize repository with the session
                token_blacklist_repo = TokenBlacklistRepository(db_session)
                
                # Remove expired tokens and get count
                removed_count = token_blacklist_repo.remove_expired_tokens()
                
                # Commit the transaction
                db_session.commit()
                
                # Log the result
                logger.info(f"Successfully removed {removed_count} expired token(s) from blacklist")
                
                return removed_count
            
    except Exception as e:
        logger.error(f"Error during token cleanup: {str(e)}", exc_info=True)
        raise
