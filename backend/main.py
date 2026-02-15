from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import cv2
from ultralytics import YOLO

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "masked"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load YOLO model
model = YOLO("MIXED_AADHAR_NO_DETECT.pt")

@app.get("/")
def home():
    return {"message": "Aadhar Masking API Running"}

@app.post("/mask/")
async def mask_image(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = cv2.imread(input_path)
    results = model(img)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), -1)

    output_path = os.path.join(OUTPUT_FOLDER, "masked_" + file.filename)
    cv2.imwrite(output_path, img)

    return FileResponse(output_path, media_type="image/png", filename="masked_" + file.filename)
