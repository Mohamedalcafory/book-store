import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from werkzeug.security import check_password_hash, generate_password_hash
import re


class SecurityUtils:
    """Utility class for security-related operations"""
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """
        Validate password strength
        Returns: (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if len(password) > 128:
            return False, "Password must be less than 128 characters"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        
        if not re.search(r'[@$!%*?&]', password):
            return False, "Password must contain at least one special character (@$!%*?&)"
        
        return True, ""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using Werkzeug's secure hashing"""
        return generate_password_hash(password)
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify a password against its hash"""
        return check_password_hash(password_hash, password)
    
    @staticmethod
    def create_tokens(user_id: int, additional_claims: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Create access and refresh tokens for a user
        """
        if additional_claims is None:
            additional_claims = {}
        
        # Create access token (expires in 15 minutes)
        access_token = create_access_token(
            identity=user_id,
            additional_claims=additional_claims,
            expires_delta=timedelta(minutes=15)
        )
        
        # Create refresh token (expires in 7 days)
        refresh_token = create_refresh_token(
            identity=user_id,
            additional_claims=additional_claims,
            expires_delta=timedelta(days=7)
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    @staticmethod
    def validate_email_format(email: str) -> bool:
        """Validate email format using regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_username_format(username: str) -> bool:
        """Validate username format (alphanumeric and underscores only)"""
        pattern = r'^[a-zA-Z0-9_]{3,50}$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Basic input sanitization"""
        if not text:
            return ""
        # Remove potentially dangerous characters
        return text.strip()
