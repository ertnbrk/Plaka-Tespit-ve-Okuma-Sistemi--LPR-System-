import cv2
import easyocr
import re
import numpy as np
from ultralytics import YOLO
import tempfile
import os

class VideoLicensePlatePipeline:
    def __init__(self, model_path="../models/best_merged_large.pt"):
        # need yolo here too
        self.model = YOLO(model_path)
        # easyocr again...
        self.reader = easyocr.Reader(['en'])
        
    def normalize_text(self, text):
        """cleaning ocr garbage"""
        text = text.upper().strip()
        # removing dots and dashes
        text = re.sub(r'[\s\.\:\-\|]+', ' ', text)
        # quick fix for ocr bugs
        # NOTE: more fixes in categorization
        return text.strip()

    def categorize_plate(self, text):
        """
        figuring out what kind of plate this is
        - TR_STANDARD
        - TR_SPECIAL
        - FOREIGN
        doing some cleaning too.
        """
        raw_text = text
        clean_text = raw_text # Keep separate if we need original
        
        # delete TR if exists
        is_tr_candidate = False
        
        if clean_text.startswith("TR"):
            clean_text = clean_text[2:].strip()
            is_tr_candidate = True
            
        matcher_text = clean_text
        
        # Try to find start of digits
        digit_match = re.search(r'^(\d{2})', clean_text)
        if digit_match:
            if 1 <= int(digit_match.group(1)) <= 81:
                is_tr_candidate = True
                
        # helper: is valid city?
        def is_valid_city_code(code_str):
            try:
                val = int(code_str)
                return 1 <= val <= 81
            except:
                return False

        if is_tr_candidate:
             # solving O/0 confusion
            if len(matcher_text) >= 2:
                first_two = list(matcher_text[:2])
                if first_two[0] == 'O': first_two[0] = '0'
                if first_two[0] == 'I': first_two[0] = '1'
                if first_two[1] == 'O': first_two[1] = '0'
                if first_two[1] == 'I': first_two[1] = '1'
                matcher_text = "".join(first_two) + matcher_text[2:]
            
            compact = matcher_text.replace(" ", "")

            # --- SPECIAL PLATES ---
            
            # diplomats (green ones maybe?)
            if re.match(r'^99\s?(CD|CC|CG|CM)\s?\d{1,4}.*$', compact):
                return "Local (TR Special - Diplomatic)"
                
            # guest cars
            if re.match(r'^\d{2}\s?(MA|MZ)\s?[A-Z0-9]{2,6}.*$', compact):
                 if is_valid_city_code(compact[:2]):
                     return "Local (TR Special - Guest)"
            
            # police cars (A series)
            police_match = re.match(r'^(\d{2})(A{1,3})(\d{1,4}).*$', compact)
            if police_match:
                city, lets, nums = police_match.groups()
                if is_valid_city_code(city):
                    return "Local (TR Special - Police)"

            # --- STANDARD PLATES ---
            # strict rule: 2nums+letters+numbers
            tr_match = re.match(r'^(\d{2})([A-Z]{1,3})(\d{3,4}).*$', compact)
            if tr_match:
                city, letters, numbers = tr_match.groups()
                if is_valid_city_code(city):
                    return "Local (TR Standard)"

            # city ok but format weird, call it 'Other'
            if len(compact) >= 2 and compact[:2].isdigit() and is_valid_city_code(compact[:2]):
                 return "Local (TR Other/Invalid)"

        # --- FOREIGN ---
        return "Foreign"

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError("Error opening video file")

        # keeping tracked cars here. saving best frame.
        tracks = {}
        
        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_idx += 1
            
            # start yolo tracking
            # persist=True keeps IDs same
            results = self.model.track(frame, persist=True, verbose=False, tracker="botsort.yaml")
            
            for r in results:
                if r.boxes.id is None:
                    continue
                    
                boxes = r.boxes.xyxy.cpu().numpy()
                track_ids = r.boxes.id.int().cpu().numpy()
                confs = r.boxes.conf.cpu().numpy()
                
                for box, track_id, conf in zip(boxes, track_ids, confs):
                    x1, y1, x2, y2 = map(int, box)
                    
                    # Calculate Score: Area * Confidence
                    # bigger plates are better for OCR
                    area = (x2 - x1) * (y2 - y1)
                    score = area * conf
                    
                    # crop plate
                    plate_img = frame[y1:y2, x1:x2]
                    if plate_img.size == 0:
                        continue
                        
                    # Update best frame for this track ID
                    if track_id not in tracks or score > tracks[track_id]['best_score']:
                        tracks[track_id] = {
                            'best_score': score,
                            'best_frame': plate_img.copy(),
                            'frame_idx': frame_idx,
                            'full_frame_snippet': frame[max(0, y1-50):min(frame.shape[0], y2+50), max(0, x1-50):min(frame.shape[1], x2+50)].copy() # Keeping context context
                        }
        
        cap.release()
        
        # done, now ocr the best frames
        final_results = []
        
        for track_id, data in tracks.items():
            img = data['best_frame']
            
            # --- OCR TIME ---
            # preprocessing stuff
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Resize 2x
            gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            # make it b&w
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            ocr_out = self.reader.readtext(thresh)
            raw_text = "".join([res[1] for res in ocr_out])
            
            normalized_text = self.normalize_text(raw_text)
            
            # basic fix logic
            parts = normalized_text.split()
            if len(parts) >= 3 and parts[0].replace('O','0').isdigit():
                 parts[0] = parts[0].replace('O','0').replace('I','1')
                 parts[-1] = parts[-1].replace('O','0').replace('I','1')
                 normalized_text = " ".join(parts)
            
            category = self.categorize_plate(normalized_text)
            
            # Base64 encode the snippet for frontend display
            _, buffer = cv2.imencode('.jpg', data['full_frame_snippet'])
            import base64
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            final_results.append({
                "track_id": int(track_id),
                "text": normalized_text,
                "category": category,
                "frame_idx": data['frame_idx'],
                "image": f"data:image/jpeg;base64,{img_base64}"
            })
            
        return final_results
