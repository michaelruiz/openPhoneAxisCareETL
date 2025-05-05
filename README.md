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
git clone https://github.com/michael-ruiz/openphone-axiscare-sync.git
cd openphone-axiscare-sync
