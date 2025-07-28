# 💸 Cross-Border Payments API

This project simulates a USD → local currency payment flow with a fee engine, onramp/offramp integration, idempotency protection, and webhook-based async updates.

## ✅ Features

- Accepts USD via a mock onramp (e.g., Stripe)
- Calculates flat + percentage fees
- Converts payout amount to destination currency using mock FX rates
- Simulates payout via mock offramp (e.g., Flutterwave, local wallet)
- Supports idempotency to prevent duplicate transactions
- Webhook endpoint to simulate async status updates
- PostgreSQL + FastAPI + SQLAlchemy

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/your-username/payments-api.git
cd payments-api
```


### 2. Create `.env` (used for local dev) sample file

```bash
cp .env_example .env
```

### 3. Set up your local environment

```env
POSTGRES_DB=payment_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 4. Start using Docker Compose

```bash
docker-compose up --build
```

> This launches both FastAPI and PostgreSQL. Alembic migrations are run automatically.

### Swagger UI

Navigate to `http://localhost:8000/docs` to view the API documentation.

---

## 📬 API Endpoints

### `POST /api/payments`

Create a new transaction.

```json
{
  "user_id": "uuid",
  "amount_usd": 100.00,
  "destination_currency": "INR"
}
```

**Header:**
```
idempotency-key: <unique-string>
```

---

### `POST /api/webhooks`

Simulate async update from an offramp:

```json
{
  "transaction_id": "uuid",
  "event_type": "payment_completed"
}
```

---

### `GET /api/payments/{transaction_id}`

Check status of a transaction.

---

## 🧠 Production Scaling Notes

### ✅ Idempotency
- Implemented via header
- Uses DB uniqueness on `idempotency_key`
- Prevents double-spending in retry scenarios

### ✅ Async Processing
- Onramp/offramp are mocked now
- Real system would:
  - Queue payouts (Celery, Sidekiq, or Kafka)
  - Use webhook handlers with secure verification
  - Add retries + dead letter queue

### ✅ Webhooks
- Can receive multiple events
- Should be idempotent themselves
- Should verify provider signatures (omitted here)

### ✅ Security
- `.env` loaded with `python-dotenv`
- In production: use Vault / AWS Secrets Manager or parameter store
- Add OAuth2 token headers or API key for protected routes

### ✅ FX Engine
- Currently mocked with hardcoded rates
- In production: integrate with a real FX provider (e.g., OpenExchange, CurrencyLayer)
- Add audit trail for rate used

### ✅ Scaling
- Run in Docker container with Uvicorn workers (gunicorn)
- Use managed DB (e.g., AWS RDS)
- Add caching for exchange rates
- Monitor: log webhook failures + queue delays

---

## 👨‍💻 Tech Stack

- **Python** + **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Pydantic**
- **Alembic** (migrations)
- **Docker Compose**

---

## 🧪 if building further

- Add user auth (OAuth2 or JWT)
- Store and track real onramp/offramp providers
- Dashboard for transaction monitoring
- Admin controls for rate override / force payout
- Alerting on failed payouts or stuck webhooks