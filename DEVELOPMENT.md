# MiniSocial Development Guide

Complete setup and development guide for MiniSocial backend developers.

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Project Structure](#project-structure)
3. [Configuration](#configuration)
4. [Common Commands](#common-commands)
5. [Troubleshooting](#troubleshooting)
6. [Exception Handling](#exception-handling)

---

## Installation & Setup

### Prerequisites

- Python 3.14+
- PostgreSQL 12+
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd minisocial
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install django==6.0.2
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install psycopg2-binary
pip install bcrypt
```

Or install all at once:

```bash
pip install -r requirements.txt
```

### Step 4: Create `.env` File

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=django-insecure-7%exna=od@-9k&sz*$qq$(11fdo1k=&6l+)p%u0q1*i7rld9o6
DB_ENGINE=django.db.backends.postgresql
DB_NAME=minisocial_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Step 5: Configure PostgreSQL Database

1. Install PostgreSQL if not already installed
2. Create a new database:

```sql
CREATE DATABASE minisocial_db;
```

3. Update `config/settings.py` with your credentials (or use `.env` file):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'minisocial_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 6: Run Migrations

```bash
python manage.py migrate
```

### Step 7: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 8: Start Development Server

```bash
python manage.py runserver
```

Server will run at: `http://127.0.0.1:8000/`

✅ **Setup Complete!** You're ready to develop.

---

## Project Structure

```
minisocial/
├── config/
│   ├── __init__.py
│   ├── settings.py           # Django settings & configuration
│   ├── urls.py               # Main URL configuration
│   ├── asgi.py               # ASGI entry point
│   ├── wsgi.py               # WSGI entry point
│   ├── exceptions.py         # Custom exception classes
│   └── exception_handler.py  # Global exception handler
│
├── accounts/
│   ├── __init__.py
│   ├── models.py             # User model definition
│   ├── views.py              # View classes (Registration, Login)
│   ├── serializers.py        # Request/response serializers
│   ├── urls.py               # Authentication URL routes
│   ├── tests.py              # Unit tests
│   ├── apps.py               # App configuration
│   ├── admin.py              # Django admin setup
│   ├── README.md             # Detailed auth documentation
│   └── migrations/           # Database schema migrations
│
├── manage.py                 # Django management script
├── README.md                 # User-friendly project description
├── DEVELOPMENT.md            # This file
└── requirements.txt          # Python dependencies
```

---

## Configuration

### Main Settings File: `config/settings.py`

Key configurations:

#### 1. Database Setup
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'minisocial_db',
        'USER': 'postgres',
        'PASSWORD': '@Rohan333',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### 2. Installed Apps
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'accounts',
]
```

#### 3. Authentication
```python
AUTH_USER_MODEL = 'accounts.User'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
```

#### 4. REST Framework Configuration
```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'config.exception_handler.custom_exception_handler',
}
```

This uses the custom exception handler for all API errors.

#### 5. JWT Configuration (Optional)
```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}
```

---

## Exception Handling

**For complete exception handling documentation**, see [config/README.md](config/README.md)

This includes:
- All custom exception classes (BadRequest, NotFound, Unauthorized, Forbidden, InternalServerError)
- Exception handler implementation and flow
- Response format specifications
- Real-world examples
- Best practices
- Troubleshooting guide

---

## Common Commands

### Database Management

```bash
# Run all pending migrations
python manage.py migrate

# Create new migration files from model changes
python manage.py makemigrations

# Create migration for specific app
python manage.py makemigrations accounts

# Show migration status
python manage.py showmigrations

# Rollback migrations
python manage.py migrate accounts 0001
```

### Server Management

```bash
# Run development server (default: 127.0.0.1:8000)
python manage.py runserver

# Run on specific host and port
python manage.py runserver 0.0.0.0:8080

# Run with auto-reload disabled
python manage.py runserver --noreload
```

### User Management

```bash
# Create superuser
python manage.py createsuperuser

# Change user password
python manage.py changepassword <username>
```

### Django Shell

```bash
# Open interactive Python shell with Django context
python manage.py shell

# Example queries
from accounts.models import User
user = User.objects.get(email='user@example.com')
print(user.full_name)
```

### Testing

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test accounts

# Run specific test class
python manage.py test accounts.tests.RegistrationTestCase

# Run with verbose output
python manage.py test --verbosity=2

# Run and show coverage
coverage run --source='.' manage.py test
coverage report
```

### Debugging

```bash
# Drop into Python debugger (add to code)
import pdb; pdb.set_trace()

# Django shell for testing queries
python manage.py shell

# View all registered URL patterns
python manage.py show_urls
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"

**Solution:** Activate virtual environment and install dependencies
```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Issue: "PostgreSQL connection error"

**Solution:** Ensure PostgreSQL is running and credentials are correct
```bash
# Check PostgreSQL status (Windows)
pg_isready -h localhost

# Test connection
psql -U postgres -d minisocial_db -h localhost
```

### Issue: "django.db.utils.ProgrammingError: relation does not exist"

**Solution:** Run migrations
```bash
python manage.py migrate
```

### Issue: "BadRequestException not being caught"

**Solution:** Use `raise_exception=True` in views
```python
# Correct
serializer.is_valid(raise_exception=True)

# Wrong
serializer.is_valid()
```

### Issue: "Password not hashing properly"

**Solution:** Use `create_user()` method instead of `create()`
```python
# Correct - hashes password
User.objects.create_user(email='user@example.com', password='pass')

# Wrong - doesn't hash
User.objects.create(email='user@example.com', password='pass')
```

### Issue: "CSRF token missing or incorrect"

**Solution:** Add `@csrf_exempt` decorator (for API testing) or disable CSRF for API views
```python
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class MyAPIView(APIView):
    pass
```

### Issue: "Secret key is exposed"

**Solution:** Use environment variables
```python
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
```

---

## Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/new-feature
```

### 2. Make Changes
- Create models, views, serializers
- Write tests for new code
- Update documentation

### 3. Run Tests
```bash
python manage.py test
```

### 4. Check Code Quality
```bash
# Format code
black .

# Check for issues
flake8 .

# Type checking
mypy .
```

### 5. Commit Changes
```bash
git add .
git commit -m "Add new feature"
```

### 6. Create Pull Request
Push to GitHub and create a pull request for review

---

## Performance Tips

1. **Use select_related() for Foreign Keys**
   ```python
   User.objects.select_related('profile')
   ```

2. **Use prefetch_related() for Reverse Relations**
   ```python
   User.objects.prefetch_related('posts')
   ```

3. **Index frequently queried fields**
   ```python
   email = models.EmailField(unique=True, db_index=True)
   ```

4. **Cache expensive queries**
   ```python
   from django.views.decorators.cache import cache_page
   
   @cache_page(60 * 15)  # 15 minutes
   def my_view(request):
       pass
   ```

5. **Use pagination for large datasets**
   ```python
   from rest_framework.pagination import PageNumberPagination
   ```

---

## Security Best Practices

✅ **Implemented:**
- Passwords hashed with BCrypt SHA256
- JWT tokens are cryptographically signed
- Email validation prevents invalid accounts
- Unique email/username constraints
- CSRF protection enabled
- SQL injection prevention via ORM

⚠️ **TODO:**
- Add rate limiting on login/registration
- Implement email verification
- Add password reset flow
- Implement 2FA (Two-Factor Authentication)
- Add API key authentication for services

---

## Module Documentation

- **[Accounts Module](accounts/README.md)** - Complete authentication documentation with API endpoints, JWT flow, and examples

---

## Next Steps

1. Read the [Accounts README](accounts/README.md) for authentication details
2. Create a new app for your feature
3. Test your code thoroughly
4. Write documentation for other developers
5. Submit a pull request

Happy coding! 🚀
