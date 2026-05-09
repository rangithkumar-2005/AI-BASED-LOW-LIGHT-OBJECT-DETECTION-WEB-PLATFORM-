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
