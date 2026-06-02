import cv2
import numpy as np
from datetime import datetime
import os

from face_recognition_improved import ImprovedFaceRecognizer
from attendance import AttendanceManager
from utils import Utils

def main():
    print("[INFO] Starting Face Recognition Attendance System...")
    print("[INFO] Using ORB-based face matching for multi-person support")
    
    # Load OpenCV Face Detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("[ERROR] Could not load Haar Cascade. Check your OpenCV installation.")
        return

    # Initialize components with improved face recognizer
    recognizer = ImprovedFaceRecognizer(known_faces_dir="known_faces", model_path="face_features.pickle")
    recognizer.load_features()
    
    attendance = AttendanceManager(attendance_dir="attendance", late_threshold="09:15:00")
    
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("[ERROR] Could not open webcam.")
        return

    prev_time = datetime.now()
    process_this_frame = True
    
    # Trackers
    face_locations = []
    face_names = []
    face_confidences = []
    attendance_statuses = []
    last_registration_time = {}  # Track registration timing

    print("[INFO] System Running.")
    print("[HOTKEYS] 'q' = Quit, 'r' = Register Face (Check terminal for name prompt)")
    print("[INFO] Looking for faces... Please face the camera.")

    while True:
        ret, frame = video_capture.read()
        if not ret or frame is None:
            continue

        if process_this_frame:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            small_gray = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)
            faces = face_cascade.detectMultiScale(small_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            face_locations = []
            for (x, y, w, h) in faces:
                # Scale back up because we used small_gray
                face_locations.append((y * 2, (x + w) * 2, (y + h) * 2, x * 2))

            face_names = []
            face_confidences = []
            attendance_statuses = []

            # Match each detected face with known faces
            for i, face_location in enumerate(face_locations):
                top, right, bottom, left = face_location
                
                # Extract features from detected face
                detected_descriptors = recognizer.extract_face_features(frame, face_location)
                
                if detected_descriptors is not None:
                    # Match against known faces (increased threshold from 30 to 50)
                    name, confidence = recognizer.match_faces(detected_descriptors, threshold=50)
                    
                    # If matched with confidence > 30%, show result
                    status = None
                    if confidence >= 30:  # Lowered threshold from 50 to 30
                        if name != "Unknown":
                            success, status = attendance.mark_attendance(name)
                            if success:
                                Utils.play_success_sound()
                    else:
                        # Very low confidence - save as unknown
                        name = "Unknown"
                        Utils.save_unknown_face(frame, face_location)
                else:
                    name = "Unknown"
                    confidence = 0
                    status = None
                
                face_names.append(name)
                face_confidences.append(confidence)
                attendance_statuses.append(status)

        process_this_frame = not process_this_frame

        # Display results
        for (top, right, bottom, left), name, conf, status in zip(face_locations, face_names, face_confidences, attendance_statuses):
            Utils.draw_face_info(frame, (top, right, bottom, left), name, conf, status)

        # FPS and Stats
        fps, prev_time = Utils.calculate_fps(prev_time)
        cv2.putText(frame, f"FPS: {int(fps)} | Faces: {len(face_locations)} | Registered: {len(recognizer.known_face_names)}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, "Press 'r' to Register | 'q' to Quit", (10, frame.shape[0] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        cv2.imshow('Face Recognition Attendance System', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("[INFO] Exiting system...")
            break
        elif key == ord('r'):
            if len(face_locations) > 0:
                print("\n" + "="*60)
                print("[REGISTRATION MODE] Face detected! Registration starting...")
                print("="*60)
                name = input("\nEnter name for registration (e.g., khsuahl): ").strip()
                
                if name and len(name) > 0:
                    print(f"\n[INFO] Registering face for: {name}")
                    # Use the first detected face for registration
                    success = recognizer.register_face(frame, name, face_location=face_locations[0])
                    if success:
                        print(f"✓ Successfully registered {name}!")
                    else:
                        print(f"✗ Failed to register {name}")
                    print("="*60 + "\n")
                else:
                    print("[WARNING] Name cannot be empty!")
            else:
                print("[WARNING] No face detected. Please stand in front of camera and press 'r' again.")

    video_capture.release()
    cv2.destroyAllWindows()
    attendance.export_to_excel()
    print("[INFO] System shutdown complete.")

if __name__ == "__main__":
    main()
