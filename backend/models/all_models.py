from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from database.connection import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    uploads = relationship('Upload', back_populates='owner')
    chats = relationship('ChatbotHistory', back_populates='owner')

class Upload(Base):
    __tablename__ = 'uploads'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    original_image_path = Column(String(255))
    enhanced_image_path = Column(String(255))
    result_image_path = Column(String(255))
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner = relationship('User', back_populates='uploads')
    detection = relationship('Detection', back_populates='upload', uselist=False)

class Detection(Base):
    __tablename__ = 'detections'
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(Integer, ForeignKey('uploads.id'))
    detected_objects = Column(Text) # JSON string
    confidence_scores = Column(Text) # JSON string
    ai_explanation = Column(Text)
    risk_level = Column(String(50))
    alert_message = Column(Text)
    status = Column(String(50))
    upload = relationship('Upload', back_populates='detection')

class ChatbotHistory(Base):
    __tablename__ = 'chatbot_history'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    question = Column(Text)
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner = relationship('User', back_populates='chats')