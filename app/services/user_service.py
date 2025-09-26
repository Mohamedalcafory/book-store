from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.security import SecurityUtils
from app.utils.exceptions import ValidationError, AuthenticationError, UserNotFoundError


class UserService:
    """Service class for user-related operations"""
    
    def __init__(self):
        self.user_repository = UserRepository()
        self.security_utils = SecurityUtils()
    
    def register_user(self, username: str, email: str, password: str) -> Tuple[User, Dict[str, str]]:
        """
        Register a new user with secure validation
        
        Args:
            username: User's username
            email: User's email
            password: User's password
            
        Returns:
            Tuple of (User object, tokens dict)
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate input data
        self._validate_registration_data(username, email, password)
        
        # Check if user already exists
        if self.user_repository.get_by_username(username):
            raise ValidationError("Username already exists")
        
        if self.user_repository.get_by_email(email):
            raise ValidationError("Email already exists")
        
        # Create new user
        user = User(
            username=username,
            email=email,
            is_active=True,
            is_admin=False
        )
        
        # Set password (this will hash it)
        user.set_password(password)
        
        # Save user to database
        try:
            saved_user = self.user_repository.add(user)
        except Exception as e:
            raise ValidationError(f"Failed to create user: {str(e)}")
        
        # Generate tokens
        tokens = self.security_utils.create_tokens(
            user_id=saved_user.id,
            additional_claims={
                'username': saved_user.username,
                'is_admin': saved_user.is_admin
            }
        )
        
        return saved_user, tokens
    
    def login_user(self, username: str, password: str) -> Tuple[User, Dict[str, str]]:
        """
        Authenticate user login
        
        Args:
            username: User's username or email
            password: User's password
            
        Returns:
            Tuple of (User object, tokens dict)
            
        Raises:
            AuthenticationError: If authentication fails
        """
        if not username or not password:
            raise AuthenticationError("Username and password are required")
        
        # Find user by username or email
        user = self.user_repository.get_by_username(username)
        if not user:
            user = self.user_repository.get_by_email(username)
        
        if not user:
            raise AuthenticationError("Invalid credentials")
        
        # Check if user is active
        if not user.is_active:
            raise AuthenticationError("Account is deactivated")
        
        # Verify password
        if not user.check_password(password):
            raise AuthenticationError("Invalid credentials")
        
        # Generate tokens
        tokens = self.security_utils.create_tokens(
            user_id=user.id,
            additional_claims={
                'username': user.username,
                'is_admin': user.is_admin
            }
        )
        
        # Update last login time (if you add this field to the model)
        user.updated_at = datetime.now()
        self.user_repository.update(user)
        
        return user, tokens
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.user_repository.get_by_id(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.user_repository.get_by_username(username)
    
    def update_user_profile(self, user_id: int, username: Optional[str] = None, 
                          email: Optional[str] = None) -> User:
        """
        Update user profile
        
        Args:
            user_id: ID of user to update
            username: New username (optional)
            email: New email (optional)
            
        Returns:
            Updated User object
            
        Raises:
            UserNotFoundError: If user not found
            ValidationError: If validation fails
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        
        if username:
            # Validate username
            if not self.security_utils.validate_username_format(username):
                raise ValidationError("Invalid username format")
            
            # Check if username is already taken
            existing_user = self.user_repository.get_by_username(username)
            if existing_user and existing_user.id != user_id:
                raise ValidationError("Username already exists")
            
            user.username = username
        
        if email:
            # Validate email
            if not self.security_utils.validate_email_format(email):
                raise ValidationError("Invalid email format")
            
            # Check if email is already taken
            existing_user = self.user_repository.get_by_email(email)
            if existing_user and existing_user.id != user_id:
                raise ValidationError("Email already exists")
            
            user.email = email
        
        # Update timestamp
        user.updated_at = datetime.now()
        
        return self.user_repository.update(user)
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """
        Change user password
        
        Args:
            user_id: ID of user
            current_password: Current password
            new_password: New password
            
        Returns:
            True if successful
            
        Raises:
            UserNotFoundError: If user not found
            AuthenticationError: If current password is wrong
            ValidationError: If new password is invalid
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        
        # Verify current password
        if not user.check_password(current_password):
            raise AuthenticationError("Current password is incorrect")
        
        # Validate new password
        is_valid, error_msg = self.security_utils.validate_password_strength(new_password)
        if not is_valid:
            raise ValidationError(error_msg)
        
        # Update password
        user.set_password(new_password)
        user.updated_at = datetime.now()
        
        self.user_repository.update(user)
        return True
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user account"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        
        user.is_active = False
        user.updated_at = datetime.now()
        
        self.user_repository.update(user)
        return True
    
    def activate_user(self, user_id: int) -> bool:
        """Activate a user account"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        
        user.is_active = True
        user.updated_at = datetime.now()
        
        self.user_repository.update(user)
        return True
    
    def _validate_registration_data(self, username: str, email: str, password: str) -> None:
        """Validate registration data"""
        # Validate username
        if not username or len(username.strip()) == 0:
            raise ValidationError("Username is required")
        
        if not self.security_utils.validate_username_format(username):
            raise ValidationError("Username must be 3-50 characters and contain only letters, numbers, and underscores")
        
        # Validate email
        if not email or len(email.strip()) == 0:
            raise ValidationError("Email is required")
        
        if not self.security_utils.validate_email_format(email):
            raise ValidationError("Invalid email format")
        
        # Validate password
        if not password or len(password.strip()) == 0:
            raise ValidationError("Password is required")
        
        is_valid, error_msg = self.security_utils.validate_password_strength(password)
        if not is_valid:
            raise ValidationError(error_msg)
