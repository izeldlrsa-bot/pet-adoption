# Pet Adoption Web Application

A Django-based pet adoption management system with user registration, pet browsing, adoption applications, and admin dashboard.

## Features

- User authentication and management
- Pet browsing and detail pages
- Adoption application system
- Admin dashboard for reviewing applications
- Responsive UI with Bootstrap 5
- Coral pink theme throughout

## Local Development Setup

### Prerequisites
- Python 3.10+
- pip and virtualenv

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd crudproject
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Collect static files:
```bash
python manage.py collectstatic
```

7. Run the development server:
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## Deployment to Render

### Steps:

1. Push to GitHub:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. Go to [render.com](https://render.com) and sign up

3. Create a new Web Service and connect your GitHub repository

4. Configure the following:
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn crudproject.wsgi`
   - **Environment Variables**:
     - `DEBUG=False`
     - `ALLOWED_HOSTS=your-app-name.render.com`
     - `SECRET_KEY` (generate a new one)
     - `DATABASE_URL` (provided by Render if using PostgreSQL)

5. Select PostgreSQL as the database (free tier available)

6. Deploy and access your app at the provided URL

## Project Structure

```
crudproject/
├── adoption/              # Admin adoption management app
├── pet_adoption/          # User pet browsing app
├── user_management/       # User management app
├── security_management/   # Authentication and authorization
├── crudproject/          # Project settings
├── static/               # Static files (CSS, JS)
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── Procfile            # Render deployment config
└── render.yaml         # Alternative Render config
```

## User Roles

- **Admin**: Can review and approve/reject adoption applications, manage users
- **Regular User**: Can browse pets and submit adoption applications

## Technologies

- Django 6.0.2
- Bootstrap 5.3.0
- PostgreSQL (production)
- SQLite (development)
- Gunicorn (production server)

## Environment Variables

For production deployment, set these variables:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed domains
- `DATABASE_URL`: Database connection string

## License

MIT License - see LICENSE file for details
