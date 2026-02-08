"""
Authentication request/response schemas.

This module defines Pydantic schemas for authentication endpoints:
- RegisterRequest: User registration with email and password
- LoginRequest: User login with email and password
- TokenResponse: JWT token response after successful authentication
"""

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """
    Request schema for user registration.
    
    Attributes:
        email: Valid email address for the user account
        password: Password for the user account (will be hashed before storage)
    """
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """
    Request schema for user login.
    
    Attributes:
        email: Email address of the user
        password: Password for authentication
    """
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    Response schema for successful authentication.
    
    Attributes:
        access_token: JWT access token for authenticated requests
        token_type: Type of token (always "bearer")
    """
    access_token: str
    token_type: str = "bearer"
