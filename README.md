# Django Blog Platform

A full-featured blog application built with **Python, Django, and PostgreSQL**, featuring article management, user authentication, profile customization, comments, search functionality, image uploads, and Jalali date support.

This project was developed to demonstrate practical Django development skills, including database integration, authentication, CRUD operations, file handling, and application configuration.

## ✨ Key Features

### 📝 Blog & Content Management
- Create, update, and delete blog posts.
- Manage post statuses: Draft, Published, and Rejected.
- Organize articles using categories.
- View detailed article pages.
- Upload and manage multiple images per article.
- Calculate and display estimated reading time.
- Display recent and popular articles.
- Paginate article listings.

### 🔍 Search
- Search articles by title.
- PostgreSQL-powered similarity search using `TrigramSimilarity`.

### 👤 Authentication & User Profiles
- User registration and login.
- User logout.
- View and update profile information.
- Upload and manage profile pictures.
- Change account passwords.

### 💬 Comments & Contact
- Submit comments on blog posts.
- Moderate comments by activating or deactivating them.
- Submit contact messages and support tickets.

### ⚙️ Additional Features
- Jalali (Persian) calendar support.
- Automatic image resizing and processing.
- Django administration panel.
- Environment-based configuration using `python-dotenv`.
- Markdown support.

## 🧰 Technology Stack

| Technology | Description |
|---|---|
| Python | Core programming language |
| Django 6 | Backend web framework |
| PostgreSQL | Relational database |
| Psycopg | PostgreSQL database adapter |
| Pillow | Image processing |
| Django Resized | Image resizing and optimization |
| Django Jalali | Persian calendar support |
| Markdown | Markdown text processing |
| Python Dotenv | Environment variable management |

## 📁 Project Structure

```text
blog/
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

## 🚀 Installation & Setup

Follow the instructions below to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/AmirHossein-1385/blog.git
cd blog
```

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
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

Create a `.env` file in the project root directory by copying the example configuration.

**Windows:**

```powershell
Copy-Item .env.example .env
```

**Linux / macOS:**

```bash
cp .env.example .env
```

Update the `.env` file with your local PostgreSQL credentials and Django configuration:

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

> **Note:** PostgreSQL must be installed and running. Create the database and database user before starting the application.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create an Administrator Account

```bash
python manage.py createsuperuser
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

## 🔧 Configuration

The main Django configuration is located in:

```text
DjangoProject1/settings.py
```

The following environment variables are used:

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Django application secret key |
| `DJANGO_DEBUG` | Enables or disables debug mode |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated list of allowed hosts |
| `POSTGRES_DB` | PostgreSQL database name |
| `POSTGRES_USER` | PostgreSQL username |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `POSTGRES_HOST` | PostgreSQL server hostname or IP |
| `POSTGRES_PORT` | PostgreSQL server port |

## 🔐 Security

- Sensitive configuration values are managed through environment variables.
- The `.env` file is excluded from version control.
- Database backup files are excluded from the repository.
- `DEBUG` should be set to `False` in production.
- Use a unique and securely generated `SECRET_KEY`.
- Configure `ALLOWED_HOSTS` for the deployment environment.

## 📌 Project Purpose

This project serves as a practical Django portfolio application, demonstrating the implementation of common backend development concepts and web application features.

It is intended for educational and portfolio purposes and can be extended with additional features in the future.
