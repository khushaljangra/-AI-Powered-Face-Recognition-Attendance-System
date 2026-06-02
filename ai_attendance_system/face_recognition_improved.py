"""
Improved face recognition using OpenCV ORB (Oriented FAST and Rotated BRIEF)
This allows distinguishing between different people without dlib dependency.
"""

import cv2
import os
import pickle
import numpy as np
from pathlib import Path


class ImprovedFaceRecognizer:
    def __init__(self, known_faces_dir="known_faces", model_path="face_features.pickle"):
        self.known_faces_dir = known_faces_dir
        self.model_path = model_path
        self.known_face_names = []
        self.known_face_descriptors = []  # ORB descriptors for each face
        self.orb = cv2.ORB_create(nfeatures=500)
        self.bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)

    def extract_face_features(self, frame, face_location=None):
        """Extract ORB features from a face region."""
        if face_location:
            top, right, bottom, left = face_location
            # Ensure coordinates are valid
            top, bottom = max(0, top), min(frame.shape[0], bottom)
            left, right = max(0, left), min(frame.shape[1], right)
            face_roi = frame[top:bottom, left:right]
        else:
            face_roi = frame
        
        # Convert to grayscale if needed
        if len(face_roi.shape) == 3:
            gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        else:
            gray_face = face_roi
        
        # Extract ORB keypoints and descriptors
        keypoints, descriptors = self.orb.detectAndCompute(gray_face, None)
        
        return descriptors

    def match_faces(self, detected_descriptors, threshold=30):
        """
        Match detected face descriptors with known faces.
        Returns: (name, confidence_score) or ("Unknown", 0)
        """
        if detected_descriptors is None or len(self.known_face_descriptors) == 0:
            return "Unknown", 0
        
        best_name = "Unknown"
        best_score = 0
        best_match_count = 0
        total_possible_matches = 0
        
        for i, known_descriptors in enumerate(self.known_face_descriptors):
            if known_descriptors is None:
                continue
            
            # Match descriptors
            matches = self.bf_matcher.match(detected_descriptors, known_descriptors)
            matches = sorted(matches, key=lambda x: x.distance)
            
            # Calculate confidence based on good matches
            # Use min of detected and known descriptor counts as max possible matches
            max_possible = min(len(detected_descriptors), len(known_descriptors))
            good_matches = [m for m in matches if m.distance < threshold]
            
            # Confidence based on good matches ratio
            if max_possible > 0:
                confidence = len(good_matches) / max_possible
            else:
                confidence = 0
            
            if confidence > best_score:
                best_score = confidence
                best_name = self.known_face_names[i]
                best_match_count = len(good_matches)
                total_possible_matches = max_possible
        
        # Normalize confidence to 0-100 scale with better calculation
        if best_name != "Unknown" and best_match_count > 0:
            # For recognized faces: higher percentage
            confidence_percent = int(best_score * 100)
            # Ensure minimum 30% for any match
            confidence_percent = max(30, confidence_percent)
        else:
            # For unknown faces: show low confidence
            confidence_percent = 15 if best_score == 0 else int(best_score * 100)
        
        return best_name, confidence_percent

    def register_face(self, frame, name, face_location=None):
        """Register a new face with given name."""
        try:
            # Extract features
            descriptors = self.extract_face_features(frame, face_location)
            
            if descriptors is None or len(descriptors) == 0:
                print("[ERROR] Could not extract face features from image")
                return False
            
            # Save face image
            if not os.path.exists(self.known_faces_dir):
                os.makedirs(self.known_faces_dir)
            
            # Check if name already exists
            if name in self.known_face_names:
                print(f"[WARNING] Face for '{name}' already exists. Updating...")
                idx = self.known_face_names.index(name)
                self.known_face_descriptors[idx] = descriptors
            else:
                self.known_face_names.append(name)
                self.known_face_descriptors.append(descriptors)
            
            # Save face image
            img_path = os.path.join(self.known_faces_dir, f"{name}.jpg")
            cv2.imwrite(img_path, frame)
            
            # Save to pickle
            self.save_features()
            print(f"[SUCCESS] Registered face for '{name}' with {len(descriptors)} features")
            return True
            
        except Exception as e:
            print(f"[ERROR] Registration failed: {e}")
            return False

    def save_features(self):
        """Save face features to disk."""
        try:
            data = {
                "names": self.known_face_names,
                "descriptors": self.known_face_descriptors
            }
            with open(self.model_path, "wb") as f:
                pickle.dump(data, f)
            print(f"[INFO] Face features saved to {self.model_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Could not save features: {e}")
            return False

    def load_features(self):
        """Load face features from disk."""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, "rb") as f:
                    data = pickle.load(f)
                    self.known_face_names = data.get("names", [])
                    self.known_face_descriptors = data.get("descriptors", [])
                print(f"[INFO] Loaded features for {len(self.known_face_names)} faces")
                return True
            else:
                print("[INFO] No saved features found. Starting fresh.")
                # Also load from images in known_faces directory
                self.load_from_images()
                return True
        except Exception as e:
            print(f"[ERROR] Could not load features: {e}")
            self.load_from_images()
            return False

    def load_from_images(self):
        """Load and extract features from images in known_faces directory."""
        print("[INFO] Extracting features from face images...")
        self.known_face_names = []
        self.known_face_descriptors = []
        
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)
            return
        
        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith((".jpg", ".png", ".jpeg")):
                name = os.path.splitext(filename)[0]
                image_path = os.path.join(self.known_faces_dir, filename)
                
                try:
                    image = cv2.imread(image_path)
                    if image is None:
                        print(f"[WARNING] Could not read image: {filename}")
                        continue
                    
                    descriptors = self.extract_face_features(image)
                    if descriptors is not None and len(descriptors) > 0:
                        self.known_face_names.append(name)
                        self.known_face_descriptors.append(descriptors)
                        print(f"[INFO] Loaded features from {filename}")
                    else:
                        print(f"[WARNING] No features found in {filename}")
                except Exception as e:
                    print(f"[ERROR] Could not process {filename}: {e}")
        
        print(f"[INFO] Loaded {len(self.known_face_names)} faces from images")
        self.save_features()
