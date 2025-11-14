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
django-crispy-forms==2.1
crispy-bootstrap5==2.0.2
```

Or generate automatically:
```bash
pip freeze > requirements.txt
```

### Step 5: Configure Django Settings

Edit `blog_project/settings.py`:

```python
# Set DEBUG to False for production
DEBUG = False

# Add your domain
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'www.yourusername.pythonanywhere.com']

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/yourusername/blog-site-django/db.sqlite3',
    }
}

# Static files
STATIC_ROOT = '/home/yourusername/blog-site-django/static'
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = '/home/yourusername/blog-site-django/media'
MEDIA_URL = '/media/'

# Email Configuration (Optional)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use app-specific password for Gmail
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'

# Security Settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

### Step 6: Run Migrations

In PythonAnywhere Bash console:

```bash
cd ~/blog-site-django
workon KBlog
python manage.py makemigrations
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

path = '/home/yourusername/blog-site-django'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'blog_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 10: Configure Static Files

In the "Web" tab, set up static files mapping:

1. URL: `/static/`
2. Directory: `/home/yourusername/blog-site-django/static`

And for media files:

1. URL: `/media/`
2. Directory: `/home/yourusername/blog-site-django/media`

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
2. Visit `yourusername.pythonanywhere.com`

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
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'www.yourusername.pythonanywhere.com']
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
