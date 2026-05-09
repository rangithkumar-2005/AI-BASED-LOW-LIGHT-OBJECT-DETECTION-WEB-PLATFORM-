<<<<<<< HEAD
# NightVision Guardian AI

AI-Powered Intelligent Night Surveillance & Low-Light Object Detection Platform.

## Features
- Low-Light Image Enhancement (OpenCV)
- Object Detection (YOLOv8) - filtering Person, Cat, Dog, Car.
- AI Risk Analysis & Explanations (Gemini API)
- MySQL Database Storage
- Futuristic Dark UI (React + Tailwind + Framer Motion)

## Setup Instructions

### 1. Database Setup
Ensure MySQL is running locally. The app expects credentials: `root` / `Ranjithkumar@123` on port `3306`.
```bash
cd backend
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python database/create_db.py
```

### 2. Backend Setup
Set your `GEMINI_API_KEY` in `backend/.env`.
```bash
cd backend
venv\\Scripts\\activate
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Next Steps
The core directory structure, database models, AI service integrations (YOLO, OpenCV, Gemini), and the frontend aesthetics have been scaffolded. 
You can now build upon the FastAPI endpoints in `backend/routes/` and the React pages in `frontend/src/pages/`.
=======
# AI-BASED-LOW-LIGHT-OBJECT-DETECTION-WEB-PLATFORM-
AI-Based Low Light Object Detection Web Platform is a full-stack AI application that enhances low-light images and detects objects using YOLOv8 and OpenCV. Built with React.js, FastAPI, and MySQL, the platform provides secure authentication, real-time object detection, AI-powered monitoring, detection history, and downloadable reports.
>>>>>>> 7c74570710d5c565b69de4faf2c0a7954fb418da
