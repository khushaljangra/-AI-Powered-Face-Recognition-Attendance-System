import cv2
import face_recognition
import pickle
import os
import numpy as np
from attendance import mark_attendance
from utils import draw_overlay, save_unknown

def main():
    # Load known encodings
    if not os.path.exists("encodings.pickle"):
        print("Error: encodings.pickle not found. Run face_encoder.py first.")
        return

    with open("encodings.pickle", "rb") as f:
        data = pickle.load(f)
    
    known_encodings = data["encodings"]
    known_names = data["names"]

    video_capture = cv2.VideoCapture(0)

    print("Starting face recognition... Press 'q' to quit.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect and encode faces in current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare faces
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

            # Mark attendance if recognized
            if name != "Unknown":
                success, message = mark_attendance(name)
                color = (0, 255, 0) if success else (0, 165, 255) # Green if marked, Orange if cooldown
                status = message
            else:
                save_unknown(frame)
                status = "Unknown - Image Saved"
                color = (0, 0, 255)

            # Draw box and label
            top, right, bottom, left = [v * 4 for v in face_location]
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            draw_overlay(frame, name, status, color)

        cv2.imshow('AI Attendance System', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            name = input("Enter name for the new user: ")
            if name:
                cv2.imwrite(f"known_faces/{name}.jpg", frame)
                print(f"Captured {name}. Please run face_encoder.py to update encodings.")

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
