# Django Blog Platform

A feature-rich blog application built with **Python, Django, and PostgreSQL**. This project provides a complete blogging experience with article management, user authentication, profile management, comments, search functionality, image uploads, and Jalali date support.

Designed as a Django portfolio project, it demonstrates practical implementation of common web application features using Django's built-in tools and third-party packages.

## ✨ Features

### Article Management
- Create, edit, and delete blog posts.
- Manage post publication status (Draft, Published, and Rejected).
- Organize articles using categories.
- View individual article details.
- Upload and manage multiple images for each post.
- Display estimated reading time.
- Browse recent and popular articles.
- Navigate articles using pagination.

### Search
- Search articles by title.
- PostgreSQL-powered fuzzy text search using `TrigramSimilarity`.

### User Authentication & Profiles
- User registration and login.
- Secure logout functionality.
- User profile management.
- Profile image uploads.
- Password change functionality.

### Comments & Contact
- Submit comments on blog posts.
- Moderate comments through activation and deactivation.
- Submit contact messages and support tickets.

### Additional Features
- Jalali (Persian) date support.
- Automatic image resizing and processing.
- Django administration panel.
- Environment-based configuration using `python-dotenv`.
- Markdown support.

## 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Django 6 | Web framework |
| PostgreSQL | Relational database |
| Psycopg | PostgreSQL database adapter |
| Pillow | Image processing |
| Django Resized | Image resizing |
| Django Jalali | Jalali date support |
| Markdown | Markdown text processing |
| Python Dotenv | Environment variable management |

## 📂 Project Structure

```text
blog/
│
├── DjangoProject1/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── blog/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── templatetags/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── ...
│
├── images/
├── templates/
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/AmirHossein-1385/blog.git
cd blog
```

### 2. Create a Virtual Environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory by copying `.env.example`.

**Windows:**

```powershell
Copy-Item .env.example .env
```

**Linux / macOS:**

```bash
cp .env.example .env
```

Update the `.env` file with your local configuration:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_DB=blog
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

Make sure PostgreSQL is installed and running, and that the specified database and database user have been created.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

## ⚙️ Configuration

The main Django settings are located in:

```text
DjangoProject1/settings.py
```

The application uses environment variables for sensitive and environment-specific configuration.

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DJANGO_DEBUG` | Enables or disables debug mode |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated list of allowed hosts |
| `POSTGRES_DB` | PostgreSQL database name |
| `POSTGRES_USER` | PostgreSQL username |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `POSTGRES_HOST` | Database server address |
| `POSTGRES_PORT` | Database server port |

## 🔐 Security Considerations

- Sensitive configuration values are stored in environment variables.
- The `.env` file is excluded from version control.
- Database backup files are excluded from the repository.
- Debug mode should be disabled in production.
- A unique and secure secret key should be generated for each deployment.
- Configure `ALLOWED_HOSTS` appropriately before production deployment.


## 📌 Project Status

This project was developed as a portfolio project to demonstrate practical Django development skills, including database integration, authentication, CRUD operations, file uploads, and application configuration.

