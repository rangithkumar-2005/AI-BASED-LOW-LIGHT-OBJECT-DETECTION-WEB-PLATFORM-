from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.all_models import User, Upload, Detection
from middleware.auth import get_current_user

router = APIRouter(prefix='/history', tags=['History'])

@router.get('/')
def get_detection_history(db: Session = Depends(get_db), current_user_email: str = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
        
    uploads = db.query(Upload).filter(Upload.user_id == user.id).order_by(Upload.uploaded_at.desc()).all()
    
    history_data = []
    for up in uploads:
        det = db.query(Detection).filter(Detection.upload_id == up.id).first()
        history_data.append({
            'upload_id': up.id,
            'original_image': up.original_image_path,
            'enhanced_image': up.enhanced_image_path,
            'result_image': up.result_image_path,
            'uploaded_at': up.uploaded_at,
            'detection': det.detected_objects if det else None,
            'risk_level': det.risk_level if det else None,
            'explanation': det.ai_explanation if det else None
        })
        
    return history_data