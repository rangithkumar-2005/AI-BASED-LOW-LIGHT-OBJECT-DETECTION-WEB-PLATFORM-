from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database.connection import get_db
from models.all_models import User, Upload, Detection
from services.enhancement_service import enhance_low_light_image
from services.yolo_service import detect_objects
from services.chatbot_service import generate_explanation
import shutil
import os
import uuid
import json

from services.pdf_service import generate_pdf_report
from fastapi.responses import FileResponse

router = APIRouter(prefix='/detect', tags=['Detection'])

os.makedirs('uploads', exist_ok=True)
os.makedirs('enhanced', exist_ok=True)
os.makedirs('results', exist_ok=True)

@router.post('/upload')
async def upload_and_detect(file: UploadFile = File(...), db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        user = User(username="guest", email="guest@example.com", password="password")
        db.add(user)
        db.commit()
        db.refresh(user)
        
    ext = file.filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    orig_path = f'uploads/{filename}'
    enh_path = f'enhanced/{filename}'
    res_path = f'results/{filename}'
    
    with open(orig_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 1. Enhance image
    enhance_low_light_image(orig_path, enh_path)
    
    # 2. Detect objects
    detected_objects = detect_objects(enh_path, res_path)
    
    # 3. Generate explanation and risk analysis
    explanation, risk_level = generate_explanation(detected_objects)
    
    # 4. Save to DB
    new_upload = Upload(user_id=user.id, original_image_path=orig_path, enhanced_image_path=enh_path, result_image_path=res_path)
    db.add(new_upload)
    db.commit()
    db.refresh(new_upload)
    
    new_detection = Detection(
        upload_id=new_upload.id,
        detected_objects=json.dumps(detected_objects),
        ai_explanation=explanation,
        risk_level=risk_level,
        status='COMPLETED'
    )
    db.add(new_detection)
    db.commit()
    
    return {
        'message': 'Detection successful',
        'upload_id': new_upload.id,
        'detected_objects': detected_objects,
        'risk_level': risk_level,
        'explanation': explanation,
        'original_image_url': f'http://127.0.0.1:8000/static/uploads/{filename}',
        'enhanced_image_url': f'http://127.0.0.1:8000/static/enhanced/{filename}',
        'result_image_url': f'http://127.0.0.1:8000/static/results/{filename}'
    }

@router.get('/report/{upload_id}')
def get_report(upload_id: int, db: Session = Depends(get_db)):
    detection = db.query(Detection).filter(Detection.upload_id == upload_id).first()
    if not detection:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report_path = generate_pdf_report(detection)
    return FileResponse(path=report_path, filename=f"NightVision_Report_{upload_id}.pdf", media_type='application/pdf')