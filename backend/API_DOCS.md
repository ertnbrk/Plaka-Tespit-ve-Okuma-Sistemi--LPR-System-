# Backend API Documentation & Test Commands

This document contains `curl` commands to test all available endpoints in the system. You can import these into Postman or run them directly in your terminal (Git Bash or similar).

Base URL: `http://localhost:8000`

---

## 1. Authentication

### **Register a New User**
Creates a new user account.
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@test.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### **Login**
Returns a JWT access token. **Copy this token for subsequent requests.**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@test.com",
    "password": "password123"
  }'
```
**Response Example:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5...",
  "token_type": "bearer"
}
```

### **Get Current User Profile**
Requires Bearer Token.
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

---

## 2. License Plate Recognition (AI)

### **Predict from Image**
Upload an image containing a license plate.
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@/path/to/your/image.jpg"
```

### **Predict from Video**
Upload a video file for processing.
```bash
curl -X POST "http://localhost:8000/predict_video" \
  -F "file=@/path/to/your/video.mp4"
```

---

## 3. Vehicle Information

### **Query Vehicle Info (Mock)**
Simulates a query to a government/insurance database using a license plate.
```bash
curl -X POST "http://localhost:8000/api/vehicle/query" \
  -H "Content-Type: application/json" \
  -d '{
    "plate": "34ABC123",
    "source": "manual_query"
  }'
```

---

## 4. Complaints (Authenticated)

### **Create a Complaint**
Report a vehicle. Sends an email notification automatically.
**Requires Auth Token.**
```bash
curl -X POST "http://localhost:8000/complaints/" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "plate": "34ABC123",
    "incident_datetime": "2026-01-11T14:30:00",
    "description": "Reckless driving, crossed red light."
  }'
```

### **List My Complaints**
See reports submitted by the logged-in user.
**Requires Auth Token.**
```bash
curl -X GET "http://localhost:8000/complaints/my?skip=0&limit=10" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

---

## 5. Admin Dashboard (Admin Only)

To test these, you must first create an admin user using the script:
`python create_admin.py`
Then login with that admin user to get an admin token.

### **List All Users**
**Requires Admin Token.**
```bash
curl -X GET "http://localhost:8000/admin/users" \
  -H "Authorization: Bearer <ADMIN_TOKEN>"
```

### **List/Filter Complaints**
Search all complaints system-wide.
**Requires Admin Token.**
```bash
curl -X GET "http://localhost:8000/admin/complaints?plate=34" \
  -H "Authorization: Bearer <ADMIN_TOKEN>"
```

### **Advanced Complaint Search**
```bash
curl -X GET "http://localhost:8000/admin/complaints?status=open&user_email=test" \
  -H "Authorization: Bearer <ADMIN_TOKEN>"
```
