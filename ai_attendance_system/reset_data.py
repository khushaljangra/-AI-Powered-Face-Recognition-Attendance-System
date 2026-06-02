import os
import shutil

def reset_all_data():
    base_dir = r"C:\Users\choya\.gemini\tmp\system32\ai_attendance_system"
    attendance_dir = os.path.join(base_dir, "attendance")
    unknown_faces_dir = os.path.join(base_dir, "unknown_faces")
    known_faces_dir = os.path.join(base_dir, "known_faces")
    
    # 1. Clear Attendance records
    if os.path.exists(attendance_dir):
        for f in os.listdir(attendance_dir):
            os.remove(os.path.join(attendance_dir, f))
        print("[INFO] Attendance records cleared.")

    # 2. Clear Unknown faces
    if os.path.exists(unknown_faces_dir):
        for f in os.listdir(unknown_faces_dir):
            os.remove(os.path.join(unknown_faces_dir, f))
        print("[INFO] Unknown faces cleared.")

    # 3. Clean Known faces (keep only khushal, mamta, mahi, khushi)
    allowed_names = ["khushal", "mamta", "mahi", "khushi", "khushal jangid"]
    if os.path.exists(known_faces_dir):
        for f in os.listdir(known_faces_dir):
            name = os.path.splitext(f)[0].lower()
            if name not in [n.lower() for n in allowed_names]:
                os.remove(os.path.join(known_faces_dir, f))
                print(f"[INFO] Removed unwanted face: {f}")
    
    # 4. Optional: Reset the model features file to force re-encoding
    features_file = os.path.join(base_dir, "face_features.pickle")
    if os.path.exists(features_file):
        os.remove(features_file)
        print("[INFO] Model features reset (will re-encode on next run).")

if __name__ == "__main__":
    reset_all_data()
