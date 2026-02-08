"""Authentication infrastructure for JWT and password hashing"""
from datetime import datetime, timedelta
from typing import Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core import config
from app.common.exceptions import UnauthorizedException

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    
    Args:
        password: The plaintext password to hash
        
    Returns:
        The hashed password string
        
    Example:
        >>> hashed = hash_password("mypassword123")
        >>> hashed != "mypassword123"
        True
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.
    
    Args:
        plain_password: The plaintext password to verify
        hashed_password: The hashed password to verify against
        
    Returns:
        True if the password matches, False otherwise
        
    Example:
        >>> hashed = hash_password("mypassword123")
        >>> verify_password("mypassword123", hashed)
        True
        >>> verify_password("wrongpassword", hashed)
        False
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Create a JWT access token with expiration.
    
    Args:
        data: Dictionary containing token payload data (e.g., {"sub": user_id, "role": role})
        
    Returns:
        Encoded JWT token string
        
    Example:
        >>> token = create_access_token({"sub": "user123", "role": "admin"})
        >>> isinstance(token, str)
        True
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: The JWT token string to verify
        
    Returns:
        Dictionary containing the decoded token payload
        
    Raises:
        UnauthorizedException: If the token is invalid, expired, or malformed
        
    Example:
        >>> token = create_access_token({"sub": "user123", "role": "admin"})
        >>> payload = verify_token(token)
        >>> payload["sub"]
        'user123'
    """
    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM]
        )
        return payload
    except JWTError as e:
        raise UnauthorizedException("Could not validate credentials")
