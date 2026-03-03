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
import os

# Dynamic Tesseract path handling for different environments
if os.name == 'nt':
    # 1. Local Windows Environment
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
else:
    # Check if Tesseract is installed via Docker/Global APT or Render's Native Build environment
    docker_tesseract_path = '/usr/bin/tesseract'
    
    # 2. Render Native Python Environment (using build.sh extracted locally)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    render_native_tesseract_path = os.path.join(current_dir, '.apt', 'usr', 'bin', 'tesseract')

    if os.path.exists(render_native_tesseract_path):
        os.environ['LD_LIBRARY_PATH'] = f"{os.path.join(current_dir, '.apt', 'usr', 'lib', 'x86_64-linux-gnu')}:{os.environ.get('LD_LIBRARY_PATH', '')}"
        os.environ['TESSDATA_PREFIX'] = os.path.join(current_dir, '.apt', 'usr', 'share', 'tesseract-ocr', '4.00')
        pytesseract.pytesseract.tesseract_cmd = render_native_tesseract_path
    elif os.path.exists(docker_tesseract_path):
        # 3. Render Docker Environment (from Dockerfile)
        pytesseract.pytesseract.tesseract_cmd = docker_tesseract_path
    else:
        # Prevent silent failures and 500 errors by raising a clear startup error
        raise RuntimeError(f"Tesseract OCR not found. Searched paths:\n1. {render_native_tesseract_path}\n2. {docker_tesseract_path}")
from ultralytics import YOLO

app = FastAPI()

# =========================
# CORS CONFIG (Production)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Load YOLO Model Once
# =========================
# Set YOLO to use the /tmp directory to avoid read-only filesystem errors on Render
os.environ["YOLO_CONFIG_DIR"] = "/tmp"
model = YOLO("MIXED_AADHAR_NO_DETECT.pt")


@app.get("/")
def home():
    return {"message": "Aadhar Masking API Running"}


@app.options("/mask")
@app.options("/mask/")
def mask_options():
    return JSONResponse(content="OK")

@app.post("/mask")
@app.post("/mask/")
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
                # Fine-tune the horizontal position so it perfectly fills the left 65% width
                # We need to calculate text dimensions.
                # Find the size of the text at scale 1.0 to calculate ratio
                text = "XXXX XXXX"
                (base_w, base_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 1)
                available_width = (mask_x2 - x1) * 0.90
                font_scale = available_width / base_w
                thickness = max(1, int(font_scale * 2.5))
                (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
                
                # Sample the background color from just above the bounding box (offset by 5 pixels)
                # to make the mask blend perfectly into the natural paper color of the card.
                sample_y = max(0, y1 - 5)
                sample_x = x1 + int((mask_x2 - x1) / 2)
                bg_color = img[sample_y, sample_x].tolist() # Returns [B, G, R]
                
                cv2.rectangle(img, (x1, y1), (mask_x2, y2), bg_color, -1)

                text_x = x1 + max(0, int(((mask_x2 - x1) - text_width) / 2))
                text_y = y1 + int(((y2 - y1) + text_height) / 2)

                cv2.putText(
                    img,
                    text,
                    (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    (0, 0, 0),
                    thickness,
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
