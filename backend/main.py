from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import base64
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytesseract
from ultralytics import YOLO

app = FastAPI()

# =========================
# CORS CONFIG (Production)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aadhaar-mask-detector.vercel.app"
    ],  # or use ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Load YOLO Model Once
# =========================
model = YOLO("MIXED_AADHAR_NO_DETECT.pt")


@app.get("/")
def home():
    return {"message": "Aadhar Masking API Running"}


@app.post("/mask")
async def mask_image(file: UploadFile = File(...)):

    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return JSONResponse(status_code=400, content={"error": "Invalid image file"})

        # =========================
        # OCR EXTRACTION
        # =========================
        extracted_text = pytesseract.image_to_string(img)

        name, dob, gender, age_str = "Not Found", "Not Found", "Not Found", "Not Calculated"
        lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]

        dob_match = re.search(
            r'(?:DOB|Year of Birth|YOB|Date of Birth)[^\d]*([\d/]+)',
            extracted_text,
            re.IGNORECASE
        )

        if dob_match:
            dob = dob_match.group(1)

            try:
                exact_match = re.search(r'(\d{2})/(\d{2})/(\d{4})', dob)
                if exact_match:
                    parsed_dob = datetime(
                        int(exact_match.group(3)),
                        int(exact_match.group(2)),
                        int(exact_match.group(1))
                    )
                    today = datetime.now()
                    age = relativedelta(today, parsed_dob)
                    age_str = f"{age.years} Years"
            except:
                age_str = "Error calculating age"

        gender_match = re.search(r'\b(Male|Female)\b', extracted_text, re.IGNORECASE)
        if gender_match:
            gender = gender_match.group(1).capitalize()

        for i, line in enumerate(lines):
            if dob != "Not Found" and dob in line and i > 0:
                candidate = lines[i - 1]
                if not any(char.isdigit() for char in candidate):
                    name = candidate
                    break

        # =========================
        # YOLO MASKING
        # =========================
        results = model.predict(img, imgsz=320, conf=0.3, verbose=False)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                mask_x2 = x1 + int((x2 - x1) * 0.65)

                cv2.rectangle(img, (x1, y1), (mask_x2, y2), (255, 255, 255), -1)

                cv2.putText(
                    img,
                    "XXXX XXXX",
                    (x1 + 5, y1 + int((y2 - y1) / 2)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 0),
                    2,
                    cv2.LINE_AA
                )

        # =========================
        # Convert to Base64
        # =========================
        _, buffer = cv2.imencode(".png", img)
        img_str = base64.b64encode(buffer).decode("utf-8")

        return JSONResponse(content={
            "masked_image": img_str,
            "extracted_data": {
                "name": name,
                "dob": dob,
                "gender": gender,
                "age": age_str
            }
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
