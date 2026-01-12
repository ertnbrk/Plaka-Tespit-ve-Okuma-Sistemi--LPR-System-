import cv2
import easyocr
import re
import numpy as np
from ultralytics import YOLO
import os
import base64
from cities import TURKISH_CITIES

class LicensePlateDetector:
    def __init__(self, model_path="../models/best_merged_large.pt"):
        # loading the best model ever (hopefully)
        self.model = YOLO(model_path)
        # easyocr is kinda slow but it works
        self.reader = easyocr.Reader(['en'])

    def process_plate_text(self, text):
        """
        Cleaning up the text mess.
        1. Remove weird chars at start.
        2. fix O and 0 mixup.
        3. check city code.
        4. Lookup City.
        """
        raw_text = text.upper().strip()
        # no garbage allowed
        clean_text = re.sub(r'[^A-Z0-9\s]', '', raw_text)
        
        # is this turkish?
        is_tr_candidate = False
        
        # sometimes it says TR at the start
        if clean_text.startswith("TR"):
            clean_text = clean_text[2:].strip() # Remove TR
            is_tr_candidate = True
        
        # cleaning start of string
        # user said only apply rules if 01-81
        
        matcher_text = clean_text
        
        # find numbers
        digit_match = re.search(r'^(\d{2})', clean_text)
        if digit_match:
            # check city code
            if 1 <= int(digit_match.group(1)) <= 81:
                is_tr_candidate = True
        
        city_name = "Unknown"
        category = "Foreign/Unknown"
        formatted = clean_text # Default to raw
        
        if is_tr_candidate:
            # fixing O/0 I/1 again...
            if len(matcher_text) >= 2:
                first_two = list(matcher_text[:2])
                if first_two[0] == 'O': first_two[0] = '0'
                if first_two[0] == 'I': first_two[0] = '1'
                if first_two[1] == 'O': first_two[1] = '0'
                if first_two[1] == 'I': first_two[1] = '1'
                matcher_text = "".join(first_two) + matcher_text[2:]

            # --- SUPER STRICT CHECK ---
            # structure: 2 digits + letters + numbers.
            # whatever is left is trash.
            
            # regex magic:
            # ^(\d{2}) -> City
            # \s*([A-Z]{1,3}) -> Letters
            # \s*(\d{3,4}) -> Numbers
            # .*$ -> Ignore rest
            
            # removing spaces just in case
            compact = matcher_text.replace(" ", "")
            tr_match = re.match(r'^(\d{2})([A-Z]{1,3})(\d{3,4}).*$', compact)
            
            if tr_match:
                city_code, lets, nums = tr_match.groups()
                
                # checking city again
                if 1 <= int(city_code) <= 81:
                    city_name = TURKISH_CITIES.get(city_code, "Unknown")
                    category = "TR Standard"
                    formatted = f"{city_code} {lets} {nums}"
                    return formatted, city_name, category
            
            # special plates (police etc)
            police_match = re.match(r'^(\d{2})(A{1,3})(\d{3,4}).*$', compact)
            if police_match:
                 city_code, lets, nums = police_match.groups()
                 if 1 <= int(city_code) <= 81:
                    city_name = TURKISH_CITIES.get(city_code, "Unknown")
                    category = "TR Special (Police)"
                    formatted = f"{city_code} {lets} {nums}"
                    return formatted, city_name, category

            # looks like a city code but weird format
            if len(compact) >= 2 and compact[:2].isdigit() and 1 <= int(compact[:2]) <= 81:
                  city_name = TURKISH_CITIES.get(compact[:2], "Unknown")
                  category = "TR (Other/Invalid Format)"
        
        # probably foreign
        return formatted, city_name, category

    def predict(self, image_bytes):
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Could not decode image")

        results = self.model(img)
        detections = []
        
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                
                plate_img = img[y1:y2, x1:x2]
                if plate_img.size == 0: continue

                # reading text
                gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
                gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                ocr_result = self.reader.readtext(thresh)
                text = "".join([res[1] for res in ocr_result])

                # filtering mess
                proc_text, city, cat = self.process_plate_text(text)
                
                if proc_text: # If valid text found
                    detections.append({
                        "box": [x1, y1, x2, y2],
                        "text": proc_text,
                        "city": city,
                        "category": cat,
                        "conf": conf
                    })
                    
                    # green box looking good
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # adding label
                    label = f"{proc_text} ({city})" if city != "Unknown" else proc_text
                    cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        _, encoded_img = cv2.imencode('.jpg', img)
        img_base64 = base64.b64encode(encoded_img).decode('utf-8')
        
        return {
            "image": f"data:image/jpeg;base64,{img_base64}",
            "detections": detections
        }
