# OpenPhone → AxisCare Sync App

This full-stack application receives OpenPhone call summary webhooks and updates corresponding caregiver profiles in AxisCare. It includes:

- **FastAPI backend** to receive and process OpenPhone events
- **Sanity checks** and validation logging
- **React + Vite frontend** to view validation logs and simulate data correction
- **Dockerized** setup for easy deployment

---

## 🚀 Features

- Receives OpenPhone webhook events (`/webhook`)
- Validates summary length (must be 10–500 characters)
- Formats and matches caregiver phone numbers
- Updates caregiver notes in AxisCare
- Logs validation failures to `validation_failures.log`
- React frontend to display logs and mock corrections

---

## 🧱 Tech Stack

- FastAPI (Python)
- React (Vite + TailwindCSS)
- Axios (HTTP requests)
- Docker + Docker Compose

---

## 📦 Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-org/openphone-axiscare-sync.git
cd openphone-axiscare-sync
```

### 2. Backend Configuration

Create a `.env` file in `backend/`:

```env
AXISCARE_API_TOKEN=your_token
AXISCARE_SITE_ID=your_site_id
OPENPHONE_API_KEY=your_openphone_key
```

### 3. Start with Docker

```bash
docker-compose up --build
```

- Backend: [http://localhost:8000](http://localhost:8000)
- Frontend: [http://localhost:5173](http://localhost:5173)

---

## 📬 API Endpoints (Backend)

| Method | Endpoint                        | Description                              |
|--------|----------------------------------|------------------------------------------|
| POST   | `/webhook`                      | Receives OpenPhone webhook events        |
| GET    | `/logs/validation-failures`     | Returns log of invalid summaries         |
| GET    | `/mock/caregiver`               | Returns fake caregiver record            |
| POST   | `/mock/correct`                 | Simulates correcting a bad record        |

---

## 🧪 Sanity Check Logic

After updating a caregiver:
- Confirms that the phone number matches
- Confirms that the new summary appears in the notes

---

## 💽 Frontend (Vite React App)

### Pages

- **/logs** – Displays validation failure logs
- **/mock** – Shows mock caregiver and triggers simulated correction

### Development

```bash
cd frontend
npm install
npm run dev
```

---

## 📁 Logs

- Invalid summaries (under 10 or over 500 characters) are saved to:
  ```
  backend/validation_failures.log
  ```

---

## 🐳 Docker Notes

The app is containerized via Docker Compose:
- `backend/Dockerfile`: FastAPI + Uvicorn
- `frontend/Dockerfile`: Vite dev server

To rebuild:
```bash
docker-compose build
```

---

## 📞 Example Webhook Payload

```json
{
  "callId": "abc123",
  "summary": "Client asked to reschedule their shift.",
  "from_number": "+15125551234",
  "to_number": "+18325556789",
  "timestamp": "2025-05-05T15:32:00Z"
}
```

---

## 📄 License

MIT or specify another license if needed.
