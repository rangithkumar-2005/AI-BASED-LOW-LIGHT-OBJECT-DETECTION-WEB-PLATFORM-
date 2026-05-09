from ultralytics import YOLO
import cv2
import os

# Ensure the model directory exists
os.makedirs('trained_model', exist_ok=True)
MODEL_PATH = 'trained_model/yolov8n.pt'

# Load or download model
model = YOLO('yolov8n.pt') 

ALLOWED_CLASSES = [0, 15, 16, 2] # 0: person, 15: cat, 16: dog, 2: car in COCO

def detect_objects(image_path, result_path):
    results = model(image_path, classes=ALLOWED_CLASSES)
    
    # Save the result image
    res = results[0]
    res.save(filename=result_path)
    
    detected = []
    for box in res.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        name = model.names[cls_id]
        detected.append({'class': name, 'confidence': round(conf * 100, 2)})
        
    return detected