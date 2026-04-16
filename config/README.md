# Config Module - Exception Handling & Configuration

This module contains the core configuration and global exception handling for the MiniSocial API.

## Overview

The `config` module handles:
- **Project Settings** - Database, apps, middleware configuration
- **URL Routing** - Main URL configuration for the project
- **Exception Handling** - Custom exceptions and global error handler
- **WSGI/ASGI** - Application entry points

## File Structure

```
config/
├── __init__.py
├── settings.py           # Django settings & installed apps
├── urls.py               # Main URL configuration
├── asgi.py               # ASGI entry point
├── wsgi.py               # WSGI entry point
├── exceptions.py         # Custom exception classes
├── exception_handler.py  # Global exception handler
└── README.md             # This file
```

---

## Exception Handling System

The exception handling system ensures all API responses follow a consistent JSON format with proper HTTP status codes.

### Architecture

```
┌─────────────────────────────────────────┐
│   View / Serializer raises exception    │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  custom_exception_handler() is called   │
│  (from config/exception_handler.py)     │
└────────────────┬────────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │ Is it a custom │
        │   exception?   │
        └────┬───────┬───┘
             │       │
          YES│       │NO
             │       │
    ┌────────▼──┐  ┌─▼──────────────────┐
    │ Format as │  │ Use default DRF    │
    │ custom    │  │ exception handler  │
    │ response  │  │ then format        │
    └────────┬──┘  └─┬──────────────────┘
             │       │
             └───┬───┘
                 │
                 ▼
    ┌─────────────────────────────────────┐
    │ Return Response with JSON format    │
    │ + HTTP status code                  │
    └─────────────────────────────────────┘
```

### How It Works

1. **Exception Raised** - Code raises a custom exception
2. **Handler Intercepts** - `custom_exception_handler()` catches it
3. **Format Response** - Converts to standard JSON format
4. **Return to Client** - Sends HTTP response with correct status code

---

## Custom Exceptions

**File:** `config/exceptions.py`

All custom exceptions inherit from Django REST Framework's `APIException` and are designed to be automatically handled by our global exception handler.

### Base Exception Class

```python
class ApiException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Something went wrong."
    initializer = False

    def __init__(self, message=None, status_code=None):
        if message is not None:
            self.detail = message
        if status_code is not None:
            self.status_code = status_code
```

**Key Features:**
- Inherits from `APIException` (DRF class)
- Default status code is 400 (Bad Request)
- Accepts custom message and status code
- Automatically caught by exception handler

---

## Exception Classes Reference

### 1. BadRequestException (HTTP 400)

Use when user provides invalid input, validation fails, or resource already exists.

**Location:** `config/exceptions.py`

**Syntax:**
```python
from config.exceptions import BadRequestException

raise BadRequestException("Error message here")
```

**Example Uses:**
```python
# Validation error
if not email_is_valid(email):
    raise BadRequestException("Invalid email format")

# Duplicate entry
if User.objects.filter(email=email).exists():
    raise BadRequestException("User with this email already exists.")

# Missing required field
if not request.data.get('username'):
    raise BadRequestException("Username is required")
```

**Response (400 Bad Request):**
```json
{
  "isSuccess": false,
  "responseMsg": "Error message here",
  "status_code": 400
}
```

**HTTP Status:** `400 Bad Request`

---

### 2. NotFoundException (HTTP 404)

Use when a requested resource cannot be found.

**Location:** `config/exceptions.py`

**Syntax:**
```python
from config.exceptions import NotFoundException

raise NotFoundException("Resource not found message")
```

**Example Uses:**
```python
# User not found
user = User.objects.filter(id=user_id).first()
if not user:
    raise NotFoundException("User not found")

# Post not found
post = Post.objects.filter(id=post_id).first()
if not post:
    raise NotFoundException("Post not found")

# Comment not found
comment = Comment.objects.filter(id=comment_id).first()
if not comment:
    raise NotFoundException("Comment not found")
```

**Response (404 Not Found):**
```json
{
  "isSuccess": false,
  "responseMsg": "User not found",
  "status_code": 404
}
```

**HTTP Status:** `404 Not Found`

---

### 3. UnauthorizedException (HTTP 401)

Use when authentication fails or user is not logged in.

**Location:** `config/exceptions.py`

**Syntax:**
```python
from config.exceptions import UnauthorizedException

raise UnauthorizedException("Authentication error message")
```

**Example Uses:**
```python
# Invalid credentials
user = authenticate(email=email, password=password)
if not user:
    raise UnauthorizedException("Invalid email or password")

# Token invalid
if not token:
    raise UnauthorizedException("Token is missing or invalid")

# Session expired
if session_expired:
    raise UnauthorizedException("Session has expired. Please login again.")
```

**Response (401 Unauthorized):**
```json
{
  "isSuccess": false,
  "responseMsg": "Invalid email or password",
  "status_code": 401
}
```

**HTTP Status:** `401 Unauthorized`

---

### 4. ForbiddenException (HTTP 403)

Use when user is authenticated but lacks permission to access a resource.

**Location:** `config/exceptions.py`

**Syntax:**
```python
from config.exceptions import ForbiddenException

raise ForbiddenException("Permission denied message")
```

**Example Uses:**
```python
# User trying to delete another user's post
if post.user_id != current_user.id:
    raise ForbiddenException("You don't have permission to delete this post")

# Non-admin trying to access admin endpoints
if not user.is_admin:
    raise ForbiddenException("Only administrators can access this resource")

# User trying to edit another user's profile
if profile.user_id != current_user.id:
    raise ForbiddenException("You can only edit your own profile")
```

**Response (403 Forbidden):**
```json
{
  "isSuccess": false,
  "responseMsg": "You don't have permission to delete this post",
  "status_code": 403
}
```

**HTTP Status:** `403 Forbidden`

---

### 5. InternalServerErrorException (HTTP 500)

Use for unexpected server errors and system failures.

**Location:** `config/exceptions.py`

**Syntax:**
```python
from config.exceptions import InternalServerErrorException

raise InternalServerErrorException("Server error message")
```

**Example Uses:**
```python
# Database connection error
try:
    user = User.objects.get(id=user_id)
except Exception as e:
    raise InternalServerErrorException("Error fetching user data")

# File upload error
try:
    process_image(file)
except Exception as e:
    raise InternalServerErrorException("Error processing image")

# External service error
try:
    send_email(user_email)
except Exception as e:
    raise InternalServerErrorException("Error sending email")
```

**Response (500 Internal Server Error):**
```json
{
  "isSuccess": false,
  "responseMsg": "Error processing image",
  "status_code": 500
}
```

**HTTP Status:** `500 Internal Server Error`

---

## Exception Handler

**File:** `config/exception_handler.py`

The global exception handler intercepts all exceptions and formats them into consistent JSON responses.

### Code Overview

```python
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from .exceptions import ApiException

def custom_exception_handler(exc, context):
    """
    Global exception handler for all API exceptions.
    
    Args:
        exc: The exception that was raised
        context: Additional context about the request
        
    Returns:
        Response object with formatted error data and HTTP status code
    """

    # Check if it's a custom exception
    if isinstance(exc, ApiException):
        return Response({
            "isSuccess": False,
            "responseMsg": str(exc.detail),
            "status_code": exc.status_code
        }, status=exc.status_code)
    
    # Fall back to DRF's default exception handler
    response = exception_handler(exc, context)

    # Custom formatting for DRF exceptions
    if response is not None:
        message = None

        # Extract error message from response
        if isinstance(response.data, dict):
            message = list(response.data.values())[0]
            if isinstance(message, list):
                message = message[0]
        else:
            message = str(response.data)

        # Format response
        return Response({
            "isSuccess": False,
            "responseMsg": message,
            "status_code": response.status_code
        }, status=response.status_code)
    
    # Fallback for completely unhandled exceptions
    return Response({
        "isSuccess": False,
        "responseMsg": "An unexpected error occurred.",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

### Handler Logic

1. **Check Custom Exception**
   ```
   Is the exception an ApiException?
   YES → Format with our standard response
   NO  → Continue
   ```

2. **Check DRF Exception**
   ```
   Did DRF handle the exception?
   YES → Extract message and format
   NO  → Continue
   ```

3. **Unhandled Exception**
   ```
   Return generic error response with 500 status
   ```

### How to Enable the Handler

The handler is enabled in `config/settings.py`:

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'config.exception_handler.custom_exception_handler',
}
```

This tells Django REST Framework to use our custom handler for all exceptions.

---

## Response Format

All API responses follow a consistent format:

### Success Response

```json
{
  "isSuccess": true,
  "message": "Success message",
  "data": {}  // Optional, depends on endpoint
}
```

**Status Codes:**
- `200 OK` - Successful GET, PUT, PATCH, DELETE
- `201 Created` - Successful POST

### Error Response

```json
{
  "isSuccess": false,
  "responseMsg": "Error description",
  "status_code": 400
}
```

**Status Codes:**
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication failed
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Real-World Examples

### Example 1: User Registration with Validation

**File:** `accounts/serializers.py`

```python
from config.exceptions import BadRequestException

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'username', 'password']

    def validate_email(self, value):
        # Check for duplicate email
        if User.objects.filter(email=value).exists():
            raise BadRequestException("User with this email already exists.")
        return value

    def validate_username(self, value):
        # Check for duplicate username
        if User.objects.filter(username=value).exists():
            raise BadRequestException("User with this username already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
```

**Client Request:**
```bash
POST /api/v1/auth/register
{
  "email": "john@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "password": "SecurePass123!"
}
```

**Success Response (201):**
```json
{
  "message": "User registered successfully."
}
```

**Error Response - Duplicate Email (400):**
```json
{
  "isSuccess": false,
  "responseMsg": "User with this email already exists.",
  "status_code": 400
}
```

---

### Example 2: Login with Authentication

**File:** `accounts/views.py`

```python
from config.exceptions import BadRequestException

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            return Response({
                "isSuccess": True,
                "message": "Login successful.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "refresh": str(RefreshToken.for_user(user)),
                    "access": str(RefreshToken.for_user(user).access_token)
                }
            }, status=status.HTTP_200_OK)
```

**Login Serializer:**
```python
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        
        if not user:
            raise BadRequestException("Invalid email or password.")
        
        return user
```

**Client Request:**
```bash
POST /api/v1/auth/login
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Success Response (200):**
```json
{
  "isSuccess": true,
  "message": "Login successful.",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

**Error Response - Invalid Credentials (400):**
```json
{
  "isSuccess": false,
  "responseMsg": "Invalid email or password.",
  "status_code": 400
}
```

---

### Example 3: Resource Not Found

**Hypothetical View:**
```python
from config.exceptions import NotFoundException

class GetUserView(APIView):
    def get(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        
        if not user:
            raise NotFoundException("User not found")
        
        return Response({
            "isSuccess": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        })
```

**Client Request:**
```bash
GET /api/v1/users/9999/
```

**Error Response (404):**
```json
{
  "isSuccess": false,
  "responseMsg": "User not found",
  "status_code": 404
}
```

---

### Example 4: Permission Denied

**Hypothetical View:**
```python
from config.exceptions import ForbiddenException

class DeletePostView(APIView):
    def delete(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()
        
        if not post:
            raise NotFoundException("Post not found")
        
        # Check if user owns the post
        if post.user_id != request.user.id:
            raise ForbiddenException(
                "You don't have permission to delete this post"
            )
        
        post.delete()
        return Response({"message": "Post deleted successfully"})
```

**Error Response - Wrong User (403):**
```json
{
  "isSuccess": false,
  "responseMsg": "You don't have permission to delete this post",
  "status_code": 403
}
```

---

## Best Practices

### ✅ DO

1. **Use appropriate exception for the situation**
   ```python
   # Good - specific exception for missing resource
   if not user:
       raise NotFoundException("User not found")
   ```

2. **Provide descriptive error messages**
   ```python
   # Good - clear message about what went wrong
   raise BadRequestException("Email must be unique and valid")
   
   # Bad - vague message
   raise BadRequestException("Invalid")
   ```

3. **Use `raise_exception=True` in serializers**
   ```python
   # Good - exceptions are caught by handler
   if serializer.is_valid(raise_exception=True):
       pass
   
   # Bad - exceptions are swallowed
   if serializer.is_valid():
       pass
   ```

4. **Validate input at serializer level**
   ```python
   # Good - validation in serializer
   class UserSerializer(serializers.ModelSerializer):
       def validate_email(self, value):
           if User.objects.filter(email=value).exists():
               raise BadRequestException("Email already exists")
           return value
   ```

5. **Return correct HTTP status codes**
   ```python
   # Good - appropriate status code
   return Response(data, status=status.HTTP_201_CREATED)
   
   # Bad - generic 200
   return Response(data)
   ```

### ❌ DON'T

1. **Don't mix exception types**
   ```python
   # Bad - NotFoundException for validation error
   if not email_valid:
       raise NotFoundException("Invalid email")
   
   # Good - BadRequestException for validation
   if not email_valid:
       raise BadRequestException("Invalid email format")
   ```

2. **Don't expose internal error details to users**
   ```python
   # Bad - exposes database error
   except Exception as e:
       raise InternalServerErrorException(str(e))
   
   # Good - generic user-friendly message
   except Exception as e:
       raise InternalServerErrorException("Error processing your request")
   ```

3. **Don't forget to validate in views**
   ```python
   # Bad - no validation
   def post(self, request):
       user = User.objects.create(**request.data)
   
   # Good - serializer validation
   def post(self, request):
       serializer = UserSerializer(data=request.data)
       serializer.is_valid(raise_exception=True)
       serializer.save()
   ```

4. **Don't use generic exceptions**
   ```python
   # Bad - generic Exception
   try:
       process_user_data()
   except Exception:
       raise Exception("Error")
   
   # Good - specific custom exception
   try:
       process_user_data()
   except Exception:
       raise InternalServerErrorException("Error processing user data")
   ```

---

## Troubleshooting

### Issue: Exception not being caught by handler

**Symptom:** Getting default Django error page instead of JSON response

**Cause:** Exception is not inheriting from `ApiException` or not raised properly

**Solution:**
1. Ensure exception inherits from `ApiException`
2. Use `raise_exception=True` in serializers
3. Import from `config.exceptions`

```python
from config.exceptions import BadRequestException  # ✓ Correct
# NOT: from django.core.exceptions import ValidationError  # ✗ Wrong

raise BadRequestException("Error message")  # ✓ Correct
```

---

### Issue: Status code not matching error type

**Symptom:** Getting 400 for not found error

**Cause:** Using wrong exception class or instantiating with wrong status code

**Solution:** Use the correct exception class
```python
raise NotFoundException("Not found")  # Returns 404
raise BadRequestException("Bad input")  # Returns 400
```

---

### Issue: Response format doesn't match client expectations

**Symptom:** Client can't parse error response

**Cause:** Raising non-ApiException or exception handler not used

**Solution:**
1. Check settings.py has correct exception handler
2. Always raise custom exceptions
3. Test with sample requests

---

## Testing Exceptions

**File:** `config/tests.py`

Example test for exception handling:

```python
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class ExceptionHandlingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_bad_request_exception(self):
        """Test BadRequestException formatting"""
        response = self.client.post('/api/v1/auth/register', {
            'email': 'invalid-email',
            'username': '',
            'password': ''
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['isSuccess'])
        self.assertIn('responseMsg', response.data)

    def test_not_found_exception(self):
        """Test NotFoundException formatting"""
        response = self.client.get('/api/v1/users/9999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['isSuccess'])

    def test_forbidden_exception(self):
        """Test ForbiddenException formatting"""
        response = self.client.delete('/api/v1/posts/1/', HTTP_AUTHORIZATION='Bearer token')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data['isSuccess'])
```

**Run Tests:**
```bash
python manage.py test config
```

---

## Summary

The exception handling system provides:

✅ **Consistency** - All errors follow same JSON format
✅ **Clarity** - Specific exceptions for different error types  
✅ **Maintainability** - Centralized exception handling
✅ **Developer Friendly** - Easy to use and understand
✅ **User Friendly** - Clear error messages

### Quick Reference

| Exception | HTTP Status | Use Case |
|-----------|-------------|----------|
| `BadRequestException` | 400 | Validation errors, invalid input |
| `UnauthorizedException` | 401 | Authentication failed |
| `ForbiddenException` | 403 | Permission denied |
| `NotFoundException` | 404 | Resource not found |
| `InternalServerErrorException` | 500 | Server error |

### Quick Start

```python
# 1. Import exception
from config.exceptions import BadRequestException

# 2. Raise when needed
if some_error_condition:
    raise BadRequestException("Error message")

# 3. Exception handler automatically formats response
# No additional code needed!
```

---

## Related Documentation

- [DEVELOPMENT.md](../DEVELOPMENT.md) - Development guide with commands
- [accounts/README.md](../accounts/README.md) - Authentication module docs
- [README.md](../README.md) - User-friendly project overview
