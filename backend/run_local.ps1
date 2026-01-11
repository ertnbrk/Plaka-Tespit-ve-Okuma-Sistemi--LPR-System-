# Clear potentially conflicting env vars from session
$env:DATABASE_URL=""

# Ensure clean slate
docker-compose up -d

# Wait a moment for DB to be ready
Start-Sleep -Seconds 5

# Initialize DB (creates tables)
python init_db.py

# Run the app
uvicorn main:app --reload
