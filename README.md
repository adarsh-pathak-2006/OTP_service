<p align="center">
  <img src="https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"/>
  <img src="https://img.shields.io/badge/DRF-3.18-ff1709?style=for-the-badge&logo=django&logoColor=white" alt="DRF"/>
  <img src="https://img.shields.io/badge/Celery-5.6-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery"/>
  <img src="https://img.shields.io/badge/Redis-8.1-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis"/>
  <img src="https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT"/>
</p>

# 🔐 OTP as a Service — API

> **A production-grade, plug-and-play OTP delivery microservice.**  
> Register a project, get a unique reference ID, and start sending OTPs to any email — no backend needed on your end.

---

## 💡 The Problem

Every app needs OTP verification — for signups, password resets, or transaction confirmations. But building a reliable OTP system from scratch every time means dealing with:

- Email infrastructure & SMTP configuration
- OTP generation, storage, and expiry
- Rate limiting & abuse prevention
- Async delivery so your main app doesn't block

**This service eliminates all of that.** Integrate OTP into any app with a single POST request.

---

## ⚡ How It Works

```
┌─────────────────┐         ┌──────────────────┐         ┌───────────────┐
│   Your App /    │  POST   │                  │  Celery  │               │
│   Frontend      │ ──────► │  OTP Service API  │ ──────► │  Email (SMTP) │
│                 │         │                  │         │               │
└─────────────────┘         └──────────────────┘         └───────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │   Redis Cache    │
                            │   + SQLite DB    │
                            └──────────────────┘
```

1. **Register** on the platform and create a **Project**
2. Receive a cryptographically secure **reference ID** (`secrets.token_urlsafe`)
3. Hit `POST /<reference_id>/` with an email — the OTP is generated and delivered asynchronously
4. That's it. Your app never touches email infrastructure.

---

## 🏗️ Architecture & Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Framework** | Django 6.1 + DRF 3.18 | REST API with serializers, pagination, and permissions |
| **Authentication** | SimpleJWT | Stateless token-based auth (access + refresh tokens) |
| **Task Queue** | Celery 5.6 + Redis | Async OTP email delivery — non-blocking |
| **Caching** | django-redis | Redis-backed response caching with signal-based invalidation |
| **Security** | CORS headers, password validators, IDOR protection | Production-hardened from day one |
| **Database** | SQLite (dev) / PostgreSQL-ready | Swappable via Django ORM |

---

## 📡 API Reference

### 🔑 Authentication

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/authentication/register/` | Create a new account | ❌ |
| `POST` | `/authentication/token/` | Get JWT access + refresh tokens | ❌ |
| `POST` | `/authentication/token/refresh/` | Refresh an expired access token | ❌ |

### 📂 Project Management

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/core/projects/` | List your projects (paginated, cached) | ✅ JWT |

### 📨 OTP Operations

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/core/projects/<id>/` | View OTP history for a project (paginated, cached) | ✅ JWT |
| `POST` | `/<reference_id>/` | **Send an OTP to an email** | ❌ Public |

### Example: Send an OTP

```bash
curl -X POST http://localhost:8000/your_reference_id/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

**Response:**
```json
{
  "data": {
    "id": 1,
    "email": "user@example.com",
    "otp": "482913",
    "sent_on": "2026-09-26T14:30:00Z",
    "project": { "..." }
  },
  "message": "otp sent on the entered address"
}
```

---

## 🔧 Key Engineering Decisions

### 🧠 Signal-Based Cache Invalidation
Instead of manually clearing caches in every view, Django signals (`post_save`) on `Project` and `OTP` models automatically invalidate all paginated cache keys when data changes. This guarantees fresh reads without sacrificing cache performance.

### ⚙️ Async Email with Celery
OTP emails are dispatched via Celery workers, keeping API response times under **~50ms** regardless of SMTP latency. The main Django process never blocks on I/O.

### 🔒 Security-First Design
- **IDOR Protection**: OTP history queries are scoped to the authenticated user's projects — no cross-tenant data leaks.
- **Password Validation**: Django's full validator suite (similarity, length, common passwords, numeric-only) is enforced at registration.
- **Cryptographic Reference IDs**: Project reference IDs use `secrets.token_urlsafe(16)` — not sequential integers — preventing enumeration attacks.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Redis server running on `localhost:6379`

### 1. Clone & Install

```bash
git clone https://github.com/adarsh-pathak-2006/OTP_service.git
cd OTP_service/otp

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
SECRET_KEY=your_secret_key_here
DEBUG=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

### 3. Run Migrations & Start

```bash
python manage.py migrate
python manage.py runserver
```

### 4. Start Celery Worker (separate terminal)

```bash
celery -A otp worker --loglevel=info
```

---

## 📁 Project Structure

```
otp/
├── authentication/          # User registration & JWT auth
│   ├── views.py             # RegisterAPI
│   ├── serializer.py        # User serializers
│   └── urls.py              # Auth routes
├── core/                    # OTP business logic
│   ├── models.py            # Project & OTP models
│   ├── views.py             # Dashboard, OTP list, OTP generation
│   ├── serializer.py        # Project & OTP serializers
│   ├── tasks.py             # Celery async email task
│   ├── signals.py           # Cache invalidation signals
│   └── urls.py              # Core routes
├── otp/                     # Django project config
│   ├── settings.py          # All configurations
│   ├── celery.py            # Celery app initialization
│   ├── cache_keys.py        # Centralized cache key generators
│   ├── pagination.py        # DRF pagination config
│   └── urls.py              # Root URL routing
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
└── manage.py
```

---

## 🗺️ Roadmap

- [ ] OTP expiry & verification endpoint
- [ ] Rate limiting per project / per email
- [ ] SMS OTP delivery (Twilio integration)
- [ ] Dashboard frontend (React / Next.js)
- [ ] Webhook callbacks on OTP events
- [ ] Docker & docker-compose setup

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  <b>Built with 🐍 Django & ❤️ by Adarsh Pathak</b>
</p>
