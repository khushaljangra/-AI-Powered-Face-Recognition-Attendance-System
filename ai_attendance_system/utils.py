import cv2
import os
from datetime import datetime
import numpy as np

try:
    import winsound
except ImportError:
    winsound = None

class Utils:
    @staticmethod
    def draw_face_info(frame, face_location, name, confidence, status=None):
        """Draws bounding box, name, and confidence score."""
        top, right, bottom, left = face_location
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        
        # Draw Box
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        
        # Draw Label Background
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        
        # Draw Label Text
        label = f"{name} ({confidence:.1f}%)"
        cv2.putText(frame, label, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        # Draw Attendance Status if provided
        if status:
            cv2.putText(frame, status, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    @staticmethod
    def save_unknown_face(frame, face_location, unknown_dir="unknown_faces"):
        """Saves a cropped unknown face to disk."""
        if not os.path.exists(unknown_dir):
            os.makedirs(unknown_dir)
            
        top, right, bottom, left = face_location
        crop = frame[top:bottom, left:right]
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"unknown_{timestamp}.jpg"
        path = os.path.join(unknown_dir, filename)
        
        cv2.imwrite(path, crop)
        print(f"[WARN] Unknown face logged: {filename}")

    @staticmethod
    def play_success_sound():
        """Plays a beep sound (Windows only)."""
        if winsound:
            winsound.Beep(1000, 200)

    @staticmethod
    def calculate_fps(prev_time):
        """Calculates and displays FPS."""
        curr_time = datetime.now()
        diff = (curr_time - prev_time).total_seconds()
        fps = 1 / diff if diff > 0 else 0
        return fps, curr_time

    @staticmethod
    def get_eye_aspect_ratio(eye_landmarks):
        """Calculates EAR for anti-spoofing (blink detection)."""
        # A, B, C, D, E, F landmarks
        # EAR = (|A-E| + |B-D|) / (2 * |C-F|)
        A = np.linalg.norm(np.array(eye_landmarks[1]) - np.array(eye_landmarks[5]))
        B = np.linalg.norm(np.array(eye_landmarks[2]) - np.array(eye_landmarks[4]))
        C = np.linalg.norm(np.array(eye_landmarks[0]) - np.array(eye_landmarks[3]))
        ear = (A + B) / (2.0 * C)
        return ear

    @staticmethod
    def is_blinking(face_landmarks):
        """Checks if the person is blinking (basic anti-spoofing)."""
        if 'left_eye' not in face_landmarks or 'right_eye' not in face_landmarks:
            return False
            
        left_ear = Utils.get_eye_aspect_ratio(face_landmarks['left_eye'])
        right_ear = Utils.get_eye_aspect_ratio(face_landmarks['right_eye'])
        avg_ear = (left_ear + right_ear) / 2.0
        
        # Typically EAR < 0.2 means eyes are closed
        return avg_ear < 0.2
