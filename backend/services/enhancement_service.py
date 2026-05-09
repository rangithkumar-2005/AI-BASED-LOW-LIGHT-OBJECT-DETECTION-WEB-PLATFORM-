import cv2
import numpy as np

def enhance_low_light_image(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        return False
        
    # Convert to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L-channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    
    # Merge and convert back to BGR
    limg = cv2.merge((cl,a,b))
    enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    # Slightly increase brightness and contrast
    alpha = 1.2
    beta = 10
    enhanced = cv2.convertScaleAbs(enhanced, alpha=alpha, beta=beta)
    
    cv2.imwrite(output_path, enhanced)
    return True