from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import cv2
import numpy as np
import base64
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from ultralytics import YOLO
from fastapi.responses import JSONResponse

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

@app.post("/mask")
@app.post("/mask/")
async def mask_image(file: UploadFile = File(...)):
    # Read file directly into memory to avoid slow disk I/O
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # --- Extract Data using OCR ---
    extracted_text = pytesseract.image_to_string(img)
    
    name, dob, gender, age_str = "Not Found", "Not Found", "Not Found", "Not Calculated"
    lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]
    
    dob_match = re.search(r'(?:DOB|Year of Birth|YOB|Date of Birth|DOB:|DOB /)[^\d]*([\d/A-Za-z-]+)', extracted_text, re.IGNORECASE)
    if dob_match:
        dob = dob_match.group(1).strip()
        
        # Calculate Age
        try:
            parsed_dob = None
            # Standard DD/MM/YYYY
            exact_match = re.search(r'(\d{2})/(\d{2})/(\d{4})', dob)
            if exact_match:
                parsed_dob = datetime(int(exact_match.group(3)), int(exact_match.group(2)), int(exact_match.group(1)))
            else:
                # Year only
                year_match = re.search(r'(\d{4})', dob)
                if year_match:
                    parsed_dob = datetime(int(year_match.group(1)), 1, 1)

            if parsed_dob:
                today = datetime.now()
                age = relativedelta(today, parsed_dob)
                age_str = f"{age.years} Years, {age.months} Months, {age.days} Days"
        except Exception as e:
            age_str = "Error calculating age"
    
    gender_match = re.search(r'\b(Male|Female|MALE|FEMALE|male|female)\b', extracted_text)
    if gender_match:
        gender = gender_match.group(1).capitalize()
        
    for i, line in enumerate(lines):
        if dob_match and dob_match.group(1) in line and i > 0:
            name_candidate = lines[i-1]
            if len(name_candidate) > 2 and not any(char.isdigit() for char in name_candidate):
                name = name_candidate
                break
            elif i > 1:
                name_candidate = lines[i-2]
                if len(name_candidate) > 2 and not any(char.isdigit() for char in name_candidate):
                    name = name_candidate
                    break

    # Use imgsz=320 and turn off logging for much faster inference
    results = model.predict(img, imgsz=320, conf=0.3, verbose=False)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            # For 8 digits out of 12, the mask x2 should be ~ 65% across the box
            mask_x2 = x1 + int((x2 - x1) * 0.65)
            
            # Text parameters for the Mask
            text = "XXXX XXXX"
            
            # Find the size of the text at scale 1.0 to calculate ratio
            (base_w, base_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 1)
            
            # Calculate the exact width available for these 8 digits (with a tiny margin)
            available_width = (mask_x2 - x1) * 0.90
            
            # Scale the text so it exactly fits the exact width of the original 8 numbers
            font_scale = available_width / base_w
            thickness = max(1, int(font_scale * 2.5))
            
            # Get final text dimensions based on exact scale
            (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
            
            # --- Dynamic Background Blending ---
            # Sample the background color from just above the bounding box (offset by 5 pixels)
            # to make the mask blend perfectly into the natural paper color of the card.
            sample_y = max(0, y1 - 5)
            sample_x = x1 + int((mask_x2 - x1) / 2)
            bg_color = img[sample_y, sample_x].tolist() # Returns [B, G, R]
            
            # Draw the rectangle using the sampled background color instead of pure white
            cv2.rectangle(img, (x1, y1), (mask_x2, y2), bg_color, -1)
            
            # Fine-tune the horizontal position so it perfectly fills the left 65% width
            text_x = x1 + max(0, int(((mask_x2 - x1) - text_width) / 2))
            # Vertically center by using baseline
            text_y = y1 + int(((y2 - y1) + text_height) / 2)
            
            cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)

    output_path = os.path.join(OUTPUT_FOLDER, "masked_" + file.filename)
    cv2.imwrite(output_path, img)
    
    _, buffer = cv2.imencode('.png', img)
    img_str = base64.b64encode(buffer).decode('utf-8')

    return JSONResponse(content={
        "masked_image": img_str,
        "extracted_data": {
            "name": name,
            "dob": dob,
            "gender": gender,
            "age": age_str
        }
    })
