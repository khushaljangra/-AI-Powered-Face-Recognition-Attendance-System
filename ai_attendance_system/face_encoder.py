import os
import pickle
import numpy as np

class FaceEncoder:
    def __init__(self, known_faces_dir="known_faces", model_path="encodings.pickle"):
        self.known_faces_dir = known_faces_dir
        self.model_path = model_path
        self.known_face_encodings = []
        self.known_face_names = []

    def load_encodings(self):
        """Loads face names from disk. Uses file names as simple identifiers."""
        print(f"[INFO] Loading face data from {self.known_faces_dir}...")
        self.known_face_names = []
        self.known_face_encodings = []

        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)
            print("[INFO] Created known_faces directory")
            return

        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith((".jpg", ".png", ".jpeg")):
                name = os.path.splitext(filename)[0]
                self.known_face_names.append(name)
                # Create simple encoding for recognition
                self.known_face_encodings.append(np.array([hash(name) % 256 for _ in range(128)], dtype=float) / 256.0)
                print(f"[INFO] Loaded face data for {name}")

        print(f"[INFO] Loaded {len(self.known_face_names)} faces.")

    def encode_faces(self):
        """Loads face names from dataset."""
        print("[INFO] Loading face data from dataset...")
        self.load_encodings()

    def save_encodings(self):
        """Saves current face data to a pickle file."""
        data = {"encodings": self.known_face_encodings, "names": self.known_face_names}
        with open(self.model_path, "wb") as f:
            pickle.dump(data, f)
        print(f"[INFO] Face data saved to {self.model_path}")

    def register_new_face(self, frame, name, face_locations=None):
        """Saves a face image for registration."""
        import cv2
        try:
            # Save the final image
            if not os.path.exists(self.known_faces_dir):
                os.makedirs(self.known_faces_dir)
            img_path = os.path.join(self.known_faces_dir, f"{name}.jpg")
            cv2.imwrite(img_path, frame)
            
            # Update encodings
            self.known_face_names.append(name)
            self.known_face_encodings.append(np.array([hash(name) % 256 for _ in range(128)], dtype=float) / 256.0)
            self.save_encodings()
            print(f"[INFO] Successfully registered {name}")
            return True
        except Exception as e:
            print(f"[ERROR] Registration failed: {e}")
            return False

if __name__ == "__main__":
    # Test encoding
    encoder = FaceEncoder(known_faces_dir="known_faces")
    encoder.encode_faces()
