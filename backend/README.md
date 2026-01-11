# Backend - License Plate Recognition & Complaint System

This directory contains the backend API for the LPR application. It detects license plates from images/videos and manages user complaints.

## Tech Stack
- **FastAPI**: Web framework
- **SQLAlchemy + SQLite**: Database
- **YOLOv8 + EasyOCR**: Inference Pipeline
- **JWT**: Authentication
- **SMTP**: Email notifications

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Copy `.env.example` to `.env` (or set these variables in your environment):
   ```bash
   # Windows (Powershell)
   $env:JWT_SECRET="mysecret"
   $env:SMTP_USER="myemail@gmail.com"
   ...
   ```
   Or simply create a defined `.env` file if you use a loader (not strictly enforced by code, but recommended).
   
   **Note**: To use email sending with Gmail, getting an **App Password** from Google Account settings is required.

3. **Database**:
   The application uses SQLite (`app.db`) by default. The database file and tables are created automatically on the first run.

## Running the Server

```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.
Swagger UI documentation: `http://localhost:8000/docs`.

## New Features (Auth & Complaints)

### Authentication
- `POST /auth/register`: Create a new user.
- `POST /auth/login`: Get a JWT access token.
- `GET /auth/me`: user profile (Requires Bearer token).

### Complaints
- `POST /complaints`: Submit a complaint (Requires Auth). Auto-sends email.
- `GET /complaints/my`: List your complaints.

### Admin
- `GET /admin/users`: List all system users.
- `GET /admin/complaints`: Filter and search all complaints.

## Creating an Admin User

To access `/admin` endpoints, you need a user with `is_admin=True`.
Run the helper script:

```bash
python create_admin.py
```
Follow the prompts to create a new admin or promote an existing user.
