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

## API Endpoints

### Auth

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/registration/` | Register a new user |
| `POST` | `/api/login/` | Login — returns token |

### Profiles

| Method | Endpoint | Description |
|---|---|---|
| `GET` / `PATCH` | `/api/profile/<id>/` | Get or update profile by ID |
| `GET` | `/api/profiles/business/` | List all business profiles |
| `GET` | `/api/profiles/customer/` | List all customer profiles |

### Offers

| Method | Endpoint | Description |
|---|---|---|
| `GET` / `POST` | `/api/offers/` | List all offers / create offer |
| `GET` / `PATCH` / `DELETE` | `/api/offers/<id>/` | Offer by ID |
| `GET` | `/api/offerdetails/<id>/` | Single offer package by ID |

### Orders

| Method | Endpoint | Description |
|---|---|---|
| `GET` / `POST` | `/api/orders/` | List orders / place order |
| `GET` / `PATCH` / `DELETE` | `/api/orders/<id>/` | Order by ID |
| `GET` | `/api/order-count/<business_user_id>/` | Open orders of a business user |
| `GET` | `/api/completed-order-count/<business_user_id>/` | Completed orders of a business user |

### Reviews

| Method | Endpoint | Description |
|---|---|---|
| `GET` / `POST` | `/api/reviews/` | List all reviews / submit review |
| `GET` / `PATCH` / `DELETE` | `/api/reviews/<id>/` | Review by ID |

### Base Info

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/base-info/` | Platform-wide statistics |

---

## Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/croser93/Coderr_BackEnd.git
cd coderr_backend

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Start the development server
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
