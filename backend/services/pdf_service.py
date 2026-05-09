from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
import os

os.makedirs('reports', exist_ok=True)

def generate_pdf_report(detection):
    report_path = f"reports/report_{detection.upload_id}.pdf"
    
    c = canvas.Canvas(report_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "NightVision Guardian AI - Detection Report")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Upload ID: {detection.upload_id}")
    c.drawString(100, 700, f"Risk Level: {detection.risk_level}")
    
    c.drawString(100, 670, "AI Explanation:")
    
    # Wrap text for AI explanation
    from reportlab.lib.utils import simpleSplit
    lines = simpleSplit(detection.ai_explanation, "Helvetica", 12, 400)
    y = 650
    for line in lines:
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750
        c.drawString(100, y, line)
        y -= 20
        
    y -= 20
    if y < 50:
        c.showPage()
        c.setFont("Helvetica", 12)
        y = 750
        
    c.drawString(100, y, "Detected Objects:")
    y -= 20
    objects = json.loads(detection.detected_objects)
    if not objects:
        c.drawString(120, y, "No relevant objects detected.")
        y -= 20
        
    for obj in objects:
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750
        c.drawString(120, y, f"- {obj['class']} ({obj['confidence']}%)")
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 750, "Visual Evidence:")
    
    y = 700
    if os.path.exists(detection.upload.enhanced_image_path):
        try:
            c.setFont("Helvetica", 12)
            c.drawString(100, y, "Enhanced Night Vision:")
            c.drawImage(ImageReader(detection.upload.enhanced_image_path), 100, y-220, width=200, height=200, preserveAspectRatio=True)
        except Exception as e:
            c.drawString(100, y-20, f"Error loading image: {str(e)}")
            
    if os.path.exists(detection.upload.result_image_path):
        try:
            c.setFont("Helvetica", 12)
            c.drawString(320, y, "YOLOv8 Detection Result:")
            c.drawImage(ImageReader(detection.upload.result_image_path), 320, y-220, width=200, height=200, preserveAspectRatio=True)
        except:
            pass
            
    c.save()
    return report_path
