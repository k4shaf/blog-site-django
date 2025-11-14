# KBlog - Advanced Django Blog Platform

A robust, feature-rich blog platform built with Django that demonstrates advanced concepts including user authentication, role-based permissions, comments, categories, tags, and search functionality.

## Features

### 🔐 User Authentication & Authorization
- User registration with email validation
- Secure login/logout functionality
- Role-based access control (Reader, Author, Admin)
- User profiles with avatars and bios
- Activity tracking system

### 📝 Post Management
- Create, read, update, delete posts (CRUD)
- Draft and published status support
- Automatic slug generation for SEO
- Featured images for posts
- Rich text content with line breaks support
- View count tracking

### 🏷️ Content Organization
- Multiple categories for organizing posts
- Tag-based content classification
- Category and tag filtering
- Related posts suggestions

### 💬 Comment System
- User comments on posts
- Comment approval workflow (pending, approved, rejected)
- Moderator controls for comment management
- Nested comment support ready

### 🔍 Search & Discovery
- Full-text search by title and content
- Filter by category and tags
- Pagination for large result sets
- Popular posts section
- Popular tags cloud

### 👥 Author Dashboard
- Personalized author dashboard
- Post statistics and analytics
- Easy post management interface
- Publishing history

### 📊 Admin Interface
- Customized Django admin panel
- Bulk comment moderation
- User management
- Activity monitoring

### 🛡️ Security & Performance
- CSRF protection
- SQL injection prevention
- Database indexes for optimized queries
- Permission-based view access

## Project Structure

```
blog-site-django/
├── blog/                    # Blog app
│   ├── migrations/
│   ├── admin.py             # Admin customization
│   ├── apps.py              # App configuration
│   ├── forms.py             # Django forms
│   ├── middleware.py        # Custom middleware
│   ├── models.py            # Database models
│   ├── signals.py           # Django signals
│   ├── urls.py              # URL routing
│   └── views.py             # View logic
├── accounts/                # User management app
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── blog_project/            # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL config
│   ├── asgi.py
│   └── wsgi.py
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── accounts/            # Auth templates
│   ├── blog/                # Blog templates
│   └── blog/emails/         # Email templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
├── manage.py
└── README.md
```

## Database Models

### Post Model
- `title` - Blog post title (CharField, max 200 chars)
- `slug` - URL-friendly identifier (SlugField, unique, auto-generated)
- `content` - Main post content (TextField)
- `excerpt` - Brief summary (CharField)
- `author` - Foreign key to User
- `category` - Foreign key to Category
- `tags` - Many-to-many relationship with Tags
- `featured_image` - Optional post image (ImageField)
- `status` - Draft or Published
- `views_count` - Number of views (PositiveIntegerField)
- `created_at`, `updated_at`, `published_at` - Timestamps

### Category Model
- `name` - Category name (CharField, unique)
- `slug` - URL-friendly identifier
- `description` - Category description
- `created_at` - Creation timestamp

### Tag Model
- `name` - Tag name (CharField, unique)
- `slug` - URL-friendly identifier
- `created_at` - Creation timestamp

### Comment Model
- `post` - Foreign key to Post
- `user` - Foreign key to User
- `content` - Comment text
- `status` - Pending, Approved, or Rejected
- `created_at`, `updated_at` - Timestamps

### UserProfile Model
- `user` - One-to-one relationship with User
- `role` - Reader, Author, or Admin
- `bio` - User biography
- `avatar` - Profile picture (ImageField)
- `website` - Personal website URL
- `is_email_verified` - Email verification status
- `created_at`, `updated_at` - Timestamps

### UserActivity Model
- `user` - Foreign key to User
- `activity_type` - Type of activity (view, create, edit, comment, etc.)
- `post` - Optional foreign key to Post
- `ip_address` - User's IP address
- `user_agent` - Browser/client information
- `created_at` - Activity timestamp

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd blog-site-django
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install django pillow django-crispy-forms crispy-bootstrap5
```

4. **Create migrations**
```bash
python manage.py makemigrations
```

5. **Apply migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## Usage

### Accessing the Blog
- **Home**: `http://localhost:8000/`
- **Search**: `http://localhost:8000/search/`
- **Post Detail**: `http://localhost:8000/post/<slug>/`
- **Admin**: `http://localhost:8000/admin/`

### User Actions

#### Registration
1. Click "Register" in the navigation menu
2. Fill in your details
3. Set a strong password
4. Account will be created with "Reader" role by default

#### Creating a Post (Authors only)
1. Log in to your account
2. Click "New Post" in the navigation
3. Fill in post details:
   - Title (auto-generates slug)
   - Content (main post text)
   - Excerpt (summary)
   - Category and Tags
   - Featured image (optional)
   - Status (Draft or Published)
4. Click "Save Post"

#### Commenting on Posts
1. Log in to your account
2. Go to any published post
3. Scroll to comments section
4. Enter your comment and click "Post Comment"
5. Your comment will be pending moderation

#### Publishing Posts
- **Draft Status**: Post is not visible to public
- **Published Status**: Post becomes visible to all readers
- Authors can switch status and edit published posts

### Admin Panel Features

#### Post Management
- Filter posts by status, category, author
- Bulk publish/unpublish operations
- View post statistics

#### Comment Moderation
- Approve pending comments
- Reject inappropriate comments
- Delete comments
- Filter by status and post

#### User Management
- Manage user roles
- View user activity
- Edit user profiles

## Configuration

### Settings.py Key Configuration

```python
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Login URLs
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'blog:home'
LOGOUT_REDIRECT_URL = 'blog:home'
```

### Email Configuration (Optional)

To enable email notifications:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-host'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'your-email@example.com'
```

## API Endpoints

### Public Endpoints
- `GET /` - Home page with all published posts
- `GET /post/<slug>/` - View single post
- `GET /search/` - Search posts
- `GET /category/<slug>/` - View posts by category
- `GET /tag/<slug>/` - View posts by tag

### Authentication Endpoints
- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login
- `GET /accounts/logout/` - User logout
- `GET /accounts/profile/` - View user profile
- `GET /accounts/profile/edit/` - Edit profile
- `GET /accounts/dashboard/` - Author dashboard

### Post Management Endpoints
- `GET /post/new/` - Create post form
- `POST /post/new/` - Submit new post
- `GET /post/<slug>/edit/` - Edit post form
- `POST /post/<slug>/edit/` - Submit post edits
- `GET /post/<slug>/delete/` - Delete post
- `POST /post/<slug>/delete/` - Confirm deletion

### Comment Endpoints
- `POST /post/<slug>/comment/` - Add comment
- `GET /comment/<id>/approve/` - Approve comment
- `GET /comment/<id>/reject/` - Reject comment
- `GET /comment/<id>/delete/` - Delete comment

## Deployment on PythonAnywhere

### Steps to Deploy

1. **Create PythonAnywhere Account**
   - Visit https://www.pythonanywhere.com/
   - Sign up for free account

2. **Upload Project**
   - Use PythonAnywhere web interface to upload files
   - Or use Git to clone your repository

3. **Configure Virtual Environment**
   - Create virtual environment on PythonAnywhere
   - Install dependencies

4. **Configure Django Settings**
   - Set `DEBUG = False`
   - Add your domain to `ALLOWED_HOSTS`
   - Configure database (PostgreSQL recommended)
   - Set secret key from environment variable

5. **Collect Static Files**
```bash
python manage.py collectstatic
```

6. **Configure Web App**
   - Create new web app in PythonAnywhere
   - Configure WSGI file
   - Set static files path

7. **Set Environment Variables**
   - Database credentials
   - Secret key
   - Email configuration

8. **Restart Web App**
   - Reload web app to apply changes

## Performance Optimization

### Database Optimization
- Database indexes on frequently queried fields
- Selective field retrieval using `only()` and `defer()`
- Query prefetching with `select_related()` and `prefetch_related()`

### Caching
- Browser caching headers
- Optional Redis caching support

### Content Delivery
- Static file compression
- Image optimization recommendations

## Security Best Practices

✅ Implemented
- CSRF protection on all forms
- SQL injection prevention (ORM usage)
- XSS protection (template escaping)
- Secure password storage (Django hasher)
- Permission-based access control
- User activity logging

⚠️ Recommendations for Production
- Enable HTTPS only
- Set secure cookies
- Use environment variables for secrets
- Regular security updates
- Rate limiting on API endpoints
- WAF (Web Application Firewall)

## Troubleshooting

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Database Migration Issues
```bash
python manage.py migrate --fake-initial
```

### Permission Denied Errors
Ensure user has appropriate role for the action

### Image Upload Not Working
Check `MEDIA_URL` and `MEDIA_ROOT` settings

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is open source and available under the MIT License.

## Support

For support, email support@KBlog.com or open an issue in the repository.

## Future Enhancements

- [ ] Email notifications for new comments
- [ ] Social media sharing
- [ ] Post scheduling
- [ ] Advanced analytics
- [ ] User followers system
- [ ] Post recommendations
- [ ] API (REST Framework)
- [ ] Dark mode
- [ ] Internationalization (i18n)
- [ ] Mobile app

---

**Created with ❤️ using Django**
