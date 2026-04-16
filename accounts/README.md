# Authentication Module (Accounts)

This module handles all user authentication, registration, and JWT token management for the MiniSocial API.

## Overview

The accounts module provides:
- **User Registration** - Create new user accounts with email, username, and password
- **User Login** - Authenticate users and receive JWT tokens
- **Token Refresh** - Refresh expired JWT tokens
- **Custom Exception Handling** - Consistent error responses for validation failures

## File Structure

```
accounts/
├── models.py           # User model definition
├── views.py            # API view classes (Registration, Login)
├── serializers.py      # Request/response serializers with validation
├── urls.py             # URL routes for auth endpoints
├── tests.py            # Unit tests
└── migrations/         # Database schema migrations
```

## User Model

**File:** `models.py`

The User model extends Django's `AbstractUser` with additional fields:

```python
class User(AbstractUser):
    email = models.EmailField(unique=True)  # Primary authentication field
    full_name = models.CharField(max_length=50)  # User's full name
    username = models.CharField(max_length=150)  # Unique username
    password = models.CharField(max_length=128)  # Hashed password (BCrypt)
```

**Key Features:**
- Email-based authentication (not username)
- All emails are unique across the system
- Passwords are hashed using BCrypt SHA256
- Legacy username field required by Django but not used for auth

## API Endpoints

### Base URL
`http://localhost:8000/api/v1/auth/`

### 1. User Registration

**Endpoint:** `POST /register`

**URL:** `http://localhost:8000/api/v1/auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "password": "SecurePassword123!"
}
```

**Success Response (201 Created):**
```json
{
  "message": "User registered successfully."
}
```

**Error Response (400 Bad Request):**

Duplicate Email:
```json
{
  "isSuccess": false,
  "responseMsg": "User with this email already exists.",
  "status_code": 400
}
```

Duplicate Username:
```json
{
  "isSuccess": false,
  "responseMsg": "User with this username already exists.",
  "status_code": 400
}
```

Missing Fields:
```json
{
  "isSuccess": false,
  "responseMsg": "This field is required.",
  "status_code": 400
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "john_doe",
    "full_name": "John Doe",
    "password": "SecurePassword123!"
  }'
```

---

### 2. User Login

**Endpoint:** `POST /login`

**URL:** `http://localhost:8000/api/v1/auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Success Response (200 OK):**
```json
{
  "isSuccess": true,
  "message": "Login successful.",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "username": "john_doe",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

**Error Response (400 Bad Request):**

Invalid Credentials:
```json
{
  "isSuccess": false,
  "responseMsg": "Invalid email or password.",
  "status_code": 400
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

---

### 3. Refresh Access Token

**Endpoint:** `POST /refresh`

**URL:** `http://localhost:8000/api/v1/auth/refresh`

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Error Response (401 Unauthorized):**
```json
{
  "isSuccess": false,
  "responseMsg": "Token is invalid or expired.",
  "status_code": 401
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

---

## JWT Authentication Flow

### Flow Diagram

```
1. User Registration
   └─> POST /register with (email, username, full_name, password)
       └─> RegistrationSerializer validates input
       └─> User created in database (password hashed)
       └─> Response: 201 Created

2. User Login
   └─> POST /login with (email, password)
       └─> LoginSerializer authenticates user
       └─> EmailBackend verifies email + password match
       └─> JWT tokens generated (access + refresh)
       └─> Response: 200 OK with tokens

3. API Requests (Protected)
   └─> Include token in Authorization header
       └─> "Authorization: Bearer <access_token>"
       └─> Server validates token
       └─> Request proceeds if valid
       └─> Request rejected if invalid/expired

4. Token Expiration & Refresh
   └─> Access token expires (default: 5 minutes)
       └─> Use refresh token to get new access token
       └─> POST /refresh with refresh token
       └─> New access token issued
       └─> Continue making authenticated requests
```

### Using JWT Tokens

**Step 1: Register a New User**
```bash
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "password": "SecurePassword123!"
}
```

**Step 2: Login to Get Tokens**
```bash
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}

Response:
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Step 3: Use Access Token in Requests**
```bash
GET /api/v1/protected-endpoint
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Step 4: Refresh Token When Expired**
```bash
POST /api/v1/auth/refresh
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## Serializers

### RegistrationSerializer

**File:** `serializers.py`

Handles user registration validation:

```python
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'username', 'password']

    def validate_email(self, value):
        # Ensures email is unique
        if User.objects.filter(email=value).exists():
            raise BadRequestException("User with this email already exists.")
        return value

    def validate_username(self, value):
        # Ensures username is unique
        if User.objects.filter(username=value).exists():
            raise BadRequestException("User with this username already exists.")
        return value

    def create(self, validated_data):
        # Creates user with hashed password
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
```

**Validation Rules:**
- Email must be unique
- Username must be unique
- Password is write-only (not returned in responses)
- All fields are required

---

### LoginSerializer

**File:** `serializers.py`

Handles user login validation and authentication:

```python
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Authenticates user using email + password
        user = authenticate(email=data['email'], password=data['password'])

        if not user:
            raise BadRequestException("Invalid email or password.")

        return user
```

**Authentication Method:**
- Uses Django's `authenticate()` function
- Requires email (not username) for authentication
- Password is verified against stored hash (BCrypt)
- Raises exception if credentials invalid

---

## Custom Exceptions

**File:** `config/exceptions.py`

All custom exceptions inherit from `ApiException` which extends `APIException`:

### Exception Classes

1. **BadRequestException** (HTTP 400)
   - Used for validation errors, duplicate entries, invalid input
   - Example: Duplicate email, invalid password format

   ```python
   raise BadRequestException("User with this email already exists.")
   ```

2. **NotFoundException** (HTTP 404)
   - Used when requested resource doesn't exist

   ```python
   raise NotFoundException("User not found.")
   ```

3. **UnauthorizedException** (HTTP 401)
   - Used for authentication failures

   ```python
   raise UnauthorizedException("Invalid credentials.")
   ```

4. **ForbiddenException** (HTTP 403)
   - Used when user lacks permission

   ```python
   raise ForbiddenException("You don't have permission to access this resource.")
   ```

5. **InternalServerErrorException** (HTTP 500)
   - Used for unexpected server errors

   ```python
   raise InternalServerErrorException("Database error occurred.")
   ```

---

## Exception Handling

**File:** `config/exception_handler.py`

The custom exception handler ensures all exceptions return consistent JSON responses:

```python
def custom_exception_handler(exc, context):
    if isinstance(exc, ApiException):
        return Response({
            "isSuccess": False,
            "responseMsg": str(exc.detail),
            "status_code": exc.status_code
        }, status=exc.status_code)
    # ... additional error handling
```

**How It Works:**
1. Check if exception is a custom `ApiException`
2. If yes, return formatted error response with `isSuccess`, `responseMsg`, and `status_code`
3. If no, fall back to DRF's default exception handler
4. Ensures all errors follow the same JSON structure

---

## Views

**File:** `views.py`

### RegistrationView

Handles user registration:

```python
class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED
            )
```

**Important:** Uses `raise_exception=True` so `BadRequestException` from serializers is caught by custom exception handler.

---

### LoginView

Handles user login and token generation:

```python
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
                    "full_name": user.full_name,
                    "username": user.username,
                    "refresh": str(RefreshToken.for_user(user)),
                    "access": str(RefreshToken.for_user(user).access_token)
                }
            }, status=status.HTTP_200_OK)
```

**Token Generation:**
- `RefreshToken.for_user(user)` - Generates refresh token
- `.access_token` - Generates access token from refresh token
- Both tokens are JWT-encoded strings

---

## Database Schema

### User Table

```sql
CREATE TABLE accounts_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP,
    is_superuser BOOLEAN DEFAULT FALSE,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(254) UNIQUE NOT NULL,
    is_staff BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    date_joined TIMESTAMP DEFAULT NOW(),
    full_name VARCHAR(50) NOT NULL
);
```

**Key Constraints:**
- `email` - UNIQUE (no two users can have same email)
- `username` - UNIQUE (legacy field, not used for auth)
- `password` - Hashed with BCrypt SHA256
- `date_joined` - Auto-set on creation

---

## Testing

**File:** `tests.py`

Example test for registration endpoint:

```python
from django.test import TestCase
from rest_framework.test import APIClient

class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/v1/auth/register'

    def test_user_registration_success(self):
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'full_name': 'Test User',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 201)

    def test_duplicate_email_validation(self):
        # First registration
        data1 = {
            'email': 'test@example.com',
            'username': 'user1',
            'full_name': 'User One',
            'password': 'Pass123!'
        }
        self.client.post(self.register_url, data1)
        
        # Second registration with same email
        data2 = {
            'email': 'test@example.com',
            'username': 'user2',
            'full_name': 'User Two',
            'password': 'Pass123!'
        }
        response = self.client.post(self.register_url, data2)
        self.assertEqual(response.status_code, 400)
```

**Run Tests:**
```bash
python manage.py test accounts
```

---

## Common Issues & Solutions

### Issue: "BadRequestException not working"
**Solution:** Ensure `raise_exception=True` is used in views:
```python
serializer.is_valid(raise_exception=True)  # Correct
# NOT: serializer.is_valid()
```

### Issue: "Invalid email authentication error"
**Solution:** Ensure `AUTH_USER_MODEL` is set in `settings.py`:
```python
AUTH_USER_MODEL = 'accounts.User'
```

### Issue: "Password not hashed"
**Solution:** Always use `create_user()` method, not `create()`:
```python
User.objects.create_user(...)  # Correct (hashes password)
# NOT: User.objects.create(...)
```

### Issue: "JWT token invalid"
**Solution:** Check token format in Authorization header:
```
Authorization: Bearer <token>  # Correct
# NOT: Authorization: <token>
```

---

## Performance Tips

1. **Use select_related() for queries** - Reduces database hits
2. **Cache JWT validation** - Use middleware to store validated tokens
3. **Implement rate limiting** - Prevent brute force login attempts
4. **Index email field** - Speeds up authentication queries

---

## Security Best Practices

1. ✅ Passwords hashed with BCrypt SHA256
2. ✅ JWT tokens are cryptographically signed
3. ✅ Email validation prevents invalid accounts
4. ✅ Unique email/username prevents duplicates
5. ⚠️ TODO: Add rate limiting on login attempts
6. ⚠️ TODO: Add email verification before account activation
7. ⚠️ TODO: Implement password reset flow

---

## Dependencies

- Django 6.0.2
- Django REST Framework 3.14+
- djangorestframework-simplejwt 5.2+
- psycopg2-binary (PostgreSQL adapter)
- bcrypt (Password hashing)

---

## Next Steps

Developers working on this module should:
1. Read this entire document
2. Review `models.py` to understand User schema
3. Check `serializers.py` for validation logic
4. Study `views.py` for request handling
5. Review `config/exceptions.py` for error handling
6. Run tests to ensure your changes work
7. Check `config/exception_handler.py` for response formatting

For questions about authentication flow, refer to the "JWT Authentication Flow" section above.
