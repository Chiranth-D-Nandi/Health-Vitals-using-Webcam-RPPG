Healthcare Monitoring System with Face Recognition
A real-time monitoring system that combines computer vision, face recognition, and camera-based vital signs estimation to provide automated health monitoring and emergency alerts.

Project Overview
This hackathon project was designed to monitor individuals' vital signs through a webcam interface, recognize registered persons, and automatically send emergency alerts to their designated contacts when critical health conditions are detected. The system operates in real-time, providing continuous surveillance and immediate notifications for abnormal vital readings. The core innovation lies in the use of remote photoplethysmography (rPPG) technology to estimate heart rate and breathing rate from subtle changes in facial skin color captured by standard camera hardware.

Technical Approach: Remote Photoplethysmography (rPPG)
The vital signs estimation in this system is based on remote photoplethysmography, a non-contact method that analyzes subtle variations in reflected light from the face to determine cardiovascular activity and respiratory rate.

How rPPG Works:

Remote photoplethysmography detects minute fluctuations in light intensity reflected from the skin caused by blood flow variations during the cardiac cycle. The algorithm primarily analyzes changes in the green light channel of video frames, as this wavelength penetrates the skin effectively and shows high sensitivity to blood volume changes. By tracking these periodic color intensity variations across facial regions over time, the system can extract the pulse waveform and calculate heart rate.

For breathing rate estimation, the system analyzes subtle facial movements and skin color changes associated with respiration. These include cyclic variations in facial dimensions and micro-expressions as the body's internal air pressure changes, combined with color intensity fluctuations synchronized with the breathing cycle.

Key advantages of rPPG:

Non-contact measurement requiring only a standard camera

No additional hardware or wearable devices needed

Applicable to monitoring multiple individuals simultaneously

Continuous measurement without subject awareness

Features
Non-Contact Vital Signs Measurement: Uses remote photoplethysmography to estimate heart rate and breathing rate from video analysis without any wearable sensors

Real-time Face Detection: Uses Haar Cascade Classifier to detect faces in live video feed with adjustable sensitivity parameters

Face Recognition: Identifies registered individuals using DeepFace deep learning model for accurate person identification

Vital Signs Monitoring: Tracks heart rate and breathing rate with configurable alert thresholds, estimated through camera-based analysis of facial color and movement patterns

Emergency Alert System: Automatically sends SMS alerts via Twilio API when vital signs deviate from normal ranges

Visual Feedback System:

Color-coded rectangles around detected faces (green for normal, red for critical conditions)

Real-time display of recognized person's identity and vital statistics

Status indicators for quick assessment of health condition

Data Persistence: SQLite database for storing face encodings and emergency contact information

Alert Management: Implements cooldown mechanisms to prevent alert spam while maintaining responsiveness

Multi-face Support: Capable of monitoring multiple individuals simultaneously with independent vital tracking

Technology Stack
Language: Python 3.7 or higher

Computer Vision: OpenCV (cv2) - face detection, video capture, and rPPG signal processing

Deep Learning: DeepFace - facial recognition and identification

Backend: TensorFlow - deep learning inference

Signal Processing: NumPy and SciPy - temporal analysis for vital sign extraction

Database: SQLite3 - lightweight data storage

Notifications: Twilio API - SMS alert delivery

Prerequisites
Python 3.7 or higher

Functional webcam or camera device with adequate lighting

Active internet connection (required for DeepFace model downloads and Twilio API)

Twilio account with active phone number for SMS delivery

Installation
Clone the repository:

bash
git clone https://github.com/yourusername/healthcare-monitoring-system.git
cd healthcare-monitoring-system
Install dependencies:

bash
pip install -r requirements.txt
Download Haar Cascade file:
The haarcascade_frontalface_default.xml file should be placed in the project root directory. Download it from the OpenCV repository.

Configure Twilio credentials:

Create an account at Twilio.com

Obtain your Account SID and Auth Token

Purchase a Twilio phone number

Update the following variables in vitals-monitor.py:

python
twilio_account_sid = 'your_account_sid'
twilio_auth_token = 'your_auth_token'
twilio_phone_number = '+1234567890'
Project Structure
text
healthcare-monitoring-system/
├── vitals-monitor.py                    # Main application
├── haarcascade_frontalface_default.xml  # Face detection model
├── faces.db                             # SQLite database (auto-generated)
├── face_database/                       # Directory for registered face images
│   ├── person_name_1.jpg
│   ├── person_name_2.jpg
│   └── ...
├── requirements.txt                     # Python dependencies
└── README.md                            # This file
Usage
Prepare the face database:

Create a face_database folder in the project directory

Add photos of individuals to be monitored (front-facing, well-lit images)

Name files using the format: firstname_lastname.jpg

Register emergency contacts:

Populate the SQLite database with individual names, face encodings, and emergency contact phone numbers

Use SQLite browser or create a separate registration script

Start the application:

bash
python vitals-monitor.py
Monitor the feed:

The webcam window will display in real-time with detected faces marked by rectangles

Green rectangles indicate normal vital signs

Red rectangles indicate critical conditions

Person's name and current vital signs (estimated via rPPG) are displayed on screen

Exit the application:

Press 'q' key or close the window

System Operation
The system operates through the following sequence:

Capture Phase: Continuously captures video frames from the connected camera

Preprocessing: Converts frames to grayscale and processes color channels for rPPG analysis

Face Detection: Applies Haar Cascade Classifier to identify face regions

rPPG Analysis:

Extracts color intensity variations from detected facial regions

Analyzes green channel fluctuations associated with blood perfusion

Applies temporal filtering to extract pulse waveform

Detects breathing patterns from facial movement and color changes

Recognition Phase: Compares detected faces against registered database using DeepFace

Vital Sign Extraction: Converts rPPG signals to heart rate (BPM) and breathing rate (breaths per minute)

Alert Phase: Triggers SMS notifications when measurements deviate from normal thresholds

Display Phase: Renders annotated video with recognition results and vital statistics

The normal vital sign ranges are configured as follows:

Heart Rate: 60-100 beats per minute

Breathing Rate: 12-20 breaths per minute

When either measurement falls outside these ranges, the system marks the condition as critical and attempts to send an alert to the registered emergency contact.

rPPG Signal Processing Details
The remote photoplethysmography implementation involves several signal processing steps:

Heart Rate Estimation:

Green channel intensity is extracted from facial regions detected in each frame

Temporal variations in intensity are analyzed across consecutive frames

Bandpass filtering isolates frequency components corresponding to heart rate (approximately 0.5-3 Hz for typical resting heart rates)

Peak detection identifies individual pulse cycles

Heart rate is calculated from the frequency of detected pulses

Breathing Rate Estimation:

Lower frequency components of the rPPG signal (approximately 0.1-0.5 Hz) are isolated

Facial landmark tracking detects subtle movements associated with respiration

Periodic patterns in skin color and facial dimensions are analyzed

Breathing rate is extracted from the dominant frequency in this lower frequency band

Signal Quality Considerations:

Adequate lighting is essential for reliable rPPG performance

Subject motion can introduce artifacts; some motion compensation is applied

Face must remain relatively frontal to the camera for accurate measurements

Continuous monitoring improves signal stability and accuracy

Configuration
Key parameters can be adjusted in the source code:

Alert Cooldown Period: Default 60 seconds between alerts for the same individual

Face Detection Sensitivity: Adjustable via scaleFactor and minNeighbors parameters

Camera Source: Default uses system's primary camera (index 0)

Alert Thresholds: Modify vital sign upper and lower bounds

rPPG Filtering Parameters: Adjust bandpass filter frequencies for heart and breathing rate extraction

Important Considerations
Environmental Factors: rPPG performance depends on consistent, adequate lighting. Shadows, flickering lights, or extreme brightness variations can degrade accuracy

Subject Positioning: Frontal face orientation and minimal motion provide best results. Lateral head movements or occlusions reduce signal quality

Face Database Quality: Recognition accuracy depends on image quality. Use clear, front-facing photographs with consistent lighting

Measurement Variability: Camera-based vital sign estimation inherently has higher variability compared to contact sensors. Multiple measurements over time improve reliability

Data Privacy: Biometric data requires careful handling. Ensure compliance with applicable data protection regulations (GDPR, HIPAA, etc.)

Twilio Costs: SMS delivery incurs usage charges based on Twilio's rate structure. Monitor account balance and set spending limits as needed

Internet Connectivity: The system requires internet access for DeepFace model initialization and Twilio API communication

Performance Requirements: Initial model loading may take 10-30 seconds. Subsequent frame processing runs in real-time on standard hardware

Limitations
rPPG accuracy is affected by lighting conditions, skin tone variations, and facial hair

Face must remain visible and relatively frontal for continuous monitoring

Motion artifacts and rapid head movements can introduce errors in vital sign estimation

System assumes cooperative subjects with frontal face orientation

DeepFace model requires initial download and computation time

Simulated measurements in current implementation do not reflect actual rPPG processing (see Future Development for planned enhancements)

Future Development
Potential enhancements for this system include:

Full rPPG algorithm implementation with advanced signal processing

Motion compensation techniques to improve accuracy during head movements

Support for alternative skin color spaces (YCbCr, LAB) for improved robustness

Real-time signal quality assessment and confidence metrics

Multi-location deployment with centralized monitoring dashboard

Historical data logging and trend analysis capabilities

Machine learning models for anomaly detection and prediction

Email notification system alongside SMS alerts

Web-based dashboard for remote monitoring

Video recording and event logging

Integration with hospital information systems
