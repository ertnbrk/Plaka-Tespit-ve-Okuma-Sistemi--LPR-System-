from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import uvicorn
import io
import tempfile
import os
import time
from pydantic import BaseModel

# Import existing logic
from inference import LicensePlateDetector
from video_inference import VideoLicensePlatePipeline
import mock_db

# New imports
from app.api.routers import auth, complaints, admin
from app.db.database import engine, Base

# Create tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LPR Backend System")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount new routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(complaints.router, prefix="/complaints", tags=["complaints"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

# Initialize detector
# Note: Path is relative to where main.py is run. 
# Assuming running from web_app/backend, model is in ../models/best.pt
detector = LicensePlateDetector(model_path="../models/best_merged_large.pt")
video_pipeline = VideoLicensePlatePipeline(model_path="../models/best_merged_large.pt")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    
    try:
        result = detector.predict(contents)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.post("/predict_video")
async def predict_video(file: UploadFile = File(...)):
    # Save uploaded video to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Process video
        results = video_pipeline.process_video(tmp_path)
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

class VehicleQuery(BaseModel):
    plate: str
    source: str = "camera_1"
    timestamp: str = None

@app.post("/api/vehicle/query")
async def query_vehicle(query: VehicleQuery):
    # Simulate realistic service delay
    time.sleep(1.2)
    
    # Query Mock DB
    info = mock_db.get_vehicle_info(query.plate)
    
    if info:
        return info
    else:
        return {"error": "Araç bulunamadı", "status": "NOT_FOUND"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
