import cv2
import numpy as np
import sqlite3
from twilio.rest import Client
from deepface import DeepFace
import os
import random

# Disable oneDNN optimizations if needed
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Load Haar Cascade for face detection
cas_path = 'haarcascade_frontalface_default.xml'

# Check if the Haar Cascade file exists before loading
if not os.path.isfile(cas_path):
    print(f"Error: Haar Cascade file not found at {cas_path}. Please ensure the file exists.")
    exit()

# Load the Cascade Classifier
try:
    cas = cv2.CascadeClassifier(cas_path)
    if cas.empty():
        raise IOError(f"Error: Haar Cascade file not loaded. Please ensure the file is located at: {cas_path}")
except Exception as e:
    print(f"Exception occurred while loading Haar Cascade: {e}")
    exit()

# Replace with your Twilio account credentials
twilio_account_sid = 'your_account_sid'  
twilio_auth_token = 'your_auth_token'
twilio_phone_number = '+1234567890'  # Your Twilio number
twilio_client = Client(twilio_account_sid, twilio_auth_token)

# Initialize SQLite database
conn = sqlite3.connect('faces.db')
cursor = conn.cursor()

# Ensure the database setup for storing recognized faces
cursor.execute('''
    CREATE TABLE IF NOT EXISTS faces (
        name TEXT,
        encoding BLOB,
        emergency_contact TEXT
    )
''')
conn.commit()

# Load known faces from the database
def load_known_faces() -> list:
    cursor.execute("SELECT name, encoding, emergency_contact FROM faces")
    known_faces = []
    for row in cursor.fetchall():
        name, encoding, emergency_contact = row
        encoding = np.frombuffer(encoding, dtype=np.float64)  
        known_faces.append((name, encoding, emergency_contact))
    return known_faces

# Load known faces into memory
known_faces = load_known_faces()

# Function to recognize a face
def recognize_face(frame: np.ndarray) -> tuple:
    try:
        results = DeepFace.find(frame, db_path='face_database', enforce_detection=False)
        if results and len(results[0]) > 0:
            name = results[0]['identity'].iloc[0].split('/')[-1].split('.')[0]  
            emergency_contact = next((row[2] for row in known_faces if row[0] == name), None)
            return name, emergency_contact
    except Exception as e:
        print(f"Error in face recognition: {e}")
    return "Unknown", None

# Function to simulate monitoring heart rate and breathing
def monitor_vitals(frame: np.ndarray) -> tuple:
    # Simulated vital signs - Replace with actual sensor integration
    heart_rate = random.randint(60, 100)  # Simulate heart rate (60-100 BPM normal range)
    breathing_rate = random.randint(12, 20)  # Simulate breathing rate (12-20 BPM normal range)
    return heart_rate, breathing_rate

# Function to send emergency alert
def send_emergency_alert(emergency_contact: str, name: str, heart_rate: int, breathing_rate: int) -> None:
    try:
        message = twilio_client.messages.create(
            body=f"🚨 EMERGENCY ALERT 🚨\n\n{name} is in critical condition!\n\nVital Signs:\n• Heart Rate: {heart_rate} BPM\n• Breathing Rate: {breathing_rate} BPM\n\nImmediate medical attention required. Please call emergency services.",
            from_=twilio_phone_number,
            to=emergency_contact
        )
        print(f"✓ Emergency alert sent to {emergency_contact}")
    except Exception as e:
        print(f"✗ Failed to send alert: {e}")

# Main loop to capture video
cap = cv2.VideoCapture(0)  
if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

print("Starting Face Recognition and Vital Monitoring System...")
print("Press 'q' to quit")

# Alert tracking to prevent spam
last_alert_sent = {}
ALERT_COOLDOWN = 60  # seconds between alerts for same person

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = cas.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    # Process each detected face
    for (x, y, w, h) in faces:
        # Draw rectangle around detected face (Green for normal, Red for critical)
        color = (0, 255, 0)  # Default green
        
        # Extract face region for recognition
        face_roi = frame[y:y+h, x:x+w]
        
        # Recognize the face
        name, emergency_contact = recognize_face(face_roi)

        # Monitor vitals
        heart_rate, breathing_rate = monitor_vitals(frame)

        # Check for abnormal vitals
        is_critical = (heart_rate < 60 or heart_rate > 100) or (breathing_rate < 12 or breathing_rate > 20)
        
        if is_critical:
            color = (0, 0, 255)  # Red for critical condition
            
            # Send emergency alert if contact exists and cooldown period passed
            if emergency_contact and name != "Unknown":
                import time
                current_time = time.time()
                if name not in last_alert_sent or (current_time - last_alert_sent[name]) > ALERT_COOLDOWN:
                    send_emergency_alert(emergency_contact, name, heart_rate, breathing_rate)
                    last_alert_sent[name] = current_time
        
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
        
        # Display name above the face
        name_text = f"Name: {name}"
        cv2.putText(frame, name_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Add status indicator
        status = "CRITICAL" if is_critical else "NORMAL"
        status_color = (0, 0, 255) if is_critical else (0, 255, 0)
        cv2.putText(frame, f"Status: {status}", (x, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

    # Display vitals on the frame (top-left corner)
    cv2.putText(frame, f"Heart Rate: {heart_rate} BPM", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, f"Breathing Rate: {breathing_rate} BPM", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    # Add system info
    cv2.putText(frame, f"Faces Detected: {len(faces)}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Show the captured frame with overlays
    cv2.imshow('Healthcare Monitoring System - Face Recognition & Vital Signs', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Check for window close event
    if cv2.getWindowProperty('Healthcare Monitoring System - Face Recognition & Vital Signs', cv2.WND_PROP_VISIBLE) < 1:
        break

# Release resources
print("\nShutting down system...")
cap.release()
cv2.destroyAllWindows()
conn.close()
print("System closed successfully.")
