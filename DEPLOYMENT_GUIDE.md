# KBlog - Deployment Guide for PythonAnywhere

This guide will help you deploy the KBlog application on PythonAnywhere.

## Prerequisites

- PythonAnywhere account (free or paid)
- GitHub account (recommended for easier deployment)
- Git installed locally

## Step-by-Step Deployment

### Step 1: Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com/
2. Click "Sign up now"
3. Choose a username (this will be part of your URL: username.pythonanywhere.com)
4. Select a plan (Beginner plan is free)
5. Complete registration and email verification

### Step 2: Upload Your Project

#### Option A: Using Git (Recommended)

1. Push your project to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/blog-site-django.git
git push -u origin main
```

2. In PythonAnywhere Bash Console:
```bash
    git clone https://github.com/yourusername/blog-site-django.git
cd blog-site-django
```

#### Option B: Upload ZIP File

1. Create a ZIP file of your project
2. Upload via PythonAnywhere web interface
3. Extract the files

### Step 3: Create Virtual Environment

In PythonAnywhere Bash console:

```bash
cd ~/blog-site-django
mkvirtualenv --python=/usr/bin/python3.10 KBlog
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Create requirements.txt

Add this file to your project root:

```
Django==5.2.8
Pillow==10.1.0
django-crispy-forms==2.3
crispy-bootstrap5==2024.10
django-filter==24.1
python-decouple==3.8
psycopg2-binary==2.9.9
gunicorn==21.2.0
```

Or generate automatically:
```bash
pip freeze > requirements.txt
```

### Step 5: Configure Django Settings

Edit `blog_project/settings.py` with your k4shaf username:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ IMPORTANT: Generate a new SECRET_KEY for production
# Run in shell: from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())
SECRET_KEY = 'django-insecure-change-this-to-generated-key'

# Set DEBUG to False for production
DEBUG = False

# Add your domain
ALLOWED_HOSTS = ['k4shaf.pythonanywhere.com', 'www.k4shaf.pythonanywhere.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'django_filters',
    
    # Local apps
    'blog.apps.BlogConfig',
    'accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'blog.middleware.UserActivityMiddleware',
]

ROOT_URLCONF = 'blog_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog_project.wsgi.application'

# ✅ CORRECT DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ CORRECT STATIC FILES CONFIGURATION
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = []

# ✅ CORRECT MEDIA FILES CONFIGURATION
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Login URLs
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'blog:home'
LOGOUT_REDIRECT_URL = 'blog:home'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Update this
EMAIL_HOST_PASSWORD = 'your-app-password'  # Update this
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'  # Update this

# Security Settings for Production
CSRF_COOKIE_SECURE = False  # Set to True when using HTTPS
SESSION_COOKIE_SECURE = False  # Set to True when using HTTPS
SECURE_SSL_REDIRECT = False  # Set to True when using HTTPS
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

### Step 6: Run Migrations

In PythonAnywhere Bash console:

```bash
cd ~/blog-site-django
workon KBlog
mkdir -p static media logs
python manage.py migrate
python manage.py collectstatic --noinput
```

### Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### Step 8: Configure Web App

1. Go to "Web" tab in PythonAnywhere
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10
5. Click "Create web app"

### Step 9: Configure WSGI File

1. Go to "Web" tab
2. Edit the WSGI configuration file
3. Replace content with:

```python
import os
import sys

path = '/home/k4shaf/blog-site-django'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'blog_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 10: Configure Static Files

In the "Web" tab, set up static files mapping:

**Static Files:**
- URL: `/static/`
- Directory: `/home/k4shaf/blog-site-django/static`

**Media Files:**
- URL: `/media/`
- Directory: `/home/k4shaf/blog-site-django/media`

### Step 11: Set Environment Variables

If using secrets like API keys:

1. Go to "Web" tab
2. Set WSGI environment variables in the configuration

Or create a `.env` file and load it in settings.py:

```python
import os
from pathlib import Path

env_path = Path('.env')
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            key, value = line.strip().split('=', 1)
            os.environ[key] = value
```

### Step 12: Reload Web App

1. In "Web" tab, click "Reload" button
2. Visit `k4shaf.pythonanywhere.com` 🎉

## Troubleshooting

### Static Files Not Loading

```bash
# In PythonAnywhere console
python manage.py collectstatic --noinput --clear
```

Then reload the web app.

### Database Lock Error

```bash
# If you get "database is locked" error
rm db.sqlite3
python manage.py migrate
```

### ModuleNotFoundError

1. Verify virtual environment is activated
2. Check Python version matches
3. Reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Permission Denied

```bash
# Fix file permissions
chmod -R 755 ~/blog-site-django
chmod 777 ~/blog-site-django/media
```

### ALLOWED_HOSTS Error

Update `settings.py`:
```python
ALLOWED_HOSTS = ['k4shaf.pythonanywhere.com', 'www.k4shaf.pythonanywhere.com', 'localhost', '127.0.0.1']
```

Reload the web app.

### 500 Error

Check error logs in PythonAnywhere:
1. Go to "Web" tab
2. Scroll down to "Log files"
3. Click on "Error log"

## Post-Deployment

### Create Categories and Tags

1. Go to `/admin/`
2. Log in with your superuser credentials
3. Create categories and tags for organizing posts

### Write Your First Post

1. Log in as your superuser account
2. Click "New Post"
3. Fill in post details
4. Publish

### Configure Email (Optional)

1. Enable Gmail 2FA
2. Generate app-specific password
3. Update `EMAIL_HOST_PASSWORD` in settings

### Set Up SSL/HTTPS

1. Go to "Web" tab
2. Look for "Security" section
3. Enable "Force HTTPS"

## Performance Optimization

### Enable Caching

Add to `settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

### Database Optimization

For PostgreSQL (if using paid plan):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yourusername$dbname',
        'USER': 'yourusername',
        'PASSWORD': 'your-password',
        'HOST': 'yourusername.postgres.pythonanywhere-services.com',
        'PORT': '',
    }
}
```

### Compress Static Files

1. Install whitenoise:
```bash
pip install whitenoise
```

2. Add to middleware in `settings.py`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line
    # ... rest of middleware
]
```

## Maintenance

### Backup Your Database

Regularly backup your SQLite database:

```bash
# In PythonAnywhere console
cd ~/blog-site-django
cp db.sqlite3 db.sqlite3.backup
```

Or download from Files section.

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Monitor Performance

1. Check "Web" tab for CPU usage
2. Review error logs regularly
3. Monitor disk usage

### Regular Maintenance

1. Delete old activities: Admin > User Activity > Select old entries > Delete
2. Prune old comments: Clean up rejected comments
3. Optimize database: `python manage.py dbshell` then run VACUUM

## Custom Domain

To use a custom domain:

1. Purchase a domain from a registrar
2. Go to PythonAnywhere "Account" tab
3. Add your domain
4. Follow domain configuration instructions
5. Update DNS records at your registrar

## Upgrading Plan

If you need more resources:

1. Go to "Account" tab
2. Click "Upgrade"
3. Choose a new plan
4. Follow upgrade instructions

## Support

- PythonAnywhere Help: https://www.pythonanywhere.com/help/
- Django Docs: https://docs.djangoproject.com/
- Blog Support: Open an issue on GitHub

---

**Last Updated**: 2024
**Django Version**: 5.2.8
**Python Version**: 3.10+
