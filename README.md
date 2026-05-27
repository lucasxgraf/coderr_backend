# Coderr Backend

This project is the Django REST Framework backend for the existing frontend application **Coderr Frontend**.

> **Developer Akademie learning project** — The backend was independently developed to fully connect to the given frontend and implement all core platform features.

---

## About the Project

Coderr is a freelance service marketplace. Business users can publish service offers with multiple pricing tiers; customers can browse, order, and review those services. The backend provides a REST API that fully serves the existing frontend.

---

## Tech Stack

| Technology | Version |
|---|---|
| Python | 3.12+ |
| Django | 6.0.5 |
| Django REST Framework | 3.17.1 |
| Database | SQLite (development) |
| Authentication | Token-based (DRF TokenAuth) |

---

## Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/lucasxgraf/coderr_backend.git
cd coderr_backend
```

```bash
# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows
```

```bash
# 3. Install dependencies
pip install -r requirements.txt
```

```bash
# 4. Create migrations for any new or changed models
python manage.py makemigrations
```

```bash
# 5. Apply database migrations
python manage.py migrate
```

```bash
# 6. Start the development server
python manage.py runserver
```

The API is then available at `http://127.0.0.1:8000/api/`.  
The Django admin is available at `http://127.0.0.1:8000/admin/`.

---

## Demo Users

To explore the platform right away, create two demo accounts via the Django shell:

```bash
python manage.py shell
```

Paste the following block:

```python
from auth_app.models import CustomUser
from rest_framework.authtoken.models import Token

# Customer
andrey = CustomUser.objects.create_user(
    username='andrey',
    password='AAAAAAAA12341234',
    email='andrey@email.com',
    first_name='Andrey',
    last_name='Test',
    type='customer',
)
Token.objects.create(user=andrey)

# Business
kevin = CustomUser.objects.create_user(
    username='kevin',
    password='12341234AAAAAAAA',
    email='kevin@email.com',
    first_name='Kevin',
    last_name='Test',
    type='business',
)
Token.objects.create(user=kevin)
```

| Role | Username | Password |
|---|---|---|
| Customer | `andrey` | `AAAAAAAA12341234` |
| Business | `kevin` | `12341234AAAAAAAA` |

---

## Project Structure

```
coderr_backend/
├── config/               # Project settings, root URLs, WSGI/ASGI
├── auth_app/             # Registration & login
│   └── api/
├── profile_app/          # Business & customer profiles
│   └── api/
├── offer_app/            # Offers & pricing tiers
│   └── api/
├── order_app/            # Orders & statistics
│   └── api/
├── review_app/           # Reviews
│   └── api/
├── base_info_app/        # Platform statistics
│   └── api/
├── manage.py
└── requirements.txt
```

---

## Running Tests

```bash
python manage.py test
```
