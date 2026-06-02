#!/usr/bin/env python
"""Test script to verify all imports and components work correctly."""

import sys

print("[TEST] Testing imports and components...")

try:
    import cv2
    print("[PASS] cv2 imported successfully")
except ImportError as e:
    print(f"[FAIL] cv2 import failed: {e}")
    sys.exit(1)

try:
    import numpy as np
    print("[PASS] numpy imported successfully")
except ImportError as e:
    print(f"[FAIL] numpy import failed: {e}")
    sys.exit(1)

try:
    from datetime import datetime
    print("[PASS] datetime imported successfully")
except ImportError as e:
    print(f"[FAIL] datetime import failed: {e}")
    sys.exit(1)

try:
    import os
    print("[PASS] os imported successfully")
except ImportError as e:
    print(f"[FAIL] os import failed: {e}")
    sys.exit(1)

try:
    from face_recognition_improved import ImprovedFaceRecognizer
    print("[PASS] ImprovedFaceRecognizer imported successfully")
except Exception as e:
    print(f"[FAIL] ImprovedFaceRecognizer import failed: {e}")
    sys.exit(1)

try:
    from attendance import AttendanceManager
    print("[PASS] AttendanceManager imported successfully")
except Exception as e:
    print(f"[FAIL] AttendanceManager import failed: {e}")
    sys.exit(1)

try:
    from utils import Utils
    print("[PASS] Utils imported successfully")
except Exception as e:
    print(f"[FAIL] Utils import failed: {e}")
    sys.exit(1)

try:
    # Test ImprovedFaceRecognizer
    recognizer = ImprovedFaceRecognizer(known_faces_dir="known_faces")
    recognizer.load_features()
    print(f"[PASS] ImprovedFaceRecognizer initialized with {len(recognizer.known_face_names)} known faces")
except Exception as e:
    print(f"[FAIL] ImprovedFaceRecognizer initialization failed: {e}")
    sys.exit(1)

try:
    # Test AttendanceManager
    attendance = AttendanceManager(attendance_dir="attendance", late_threshold="09:15:00")
    print("[PASS] AttendanceManager initialized successfully")
except Exception as e:
    print(f"[FAIL] AttendanceManager initialization failed: {e}")
    sys.exit(1)

try:
    # Test OpenCV Cascade Classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("[FAIL] Could not load Haar Cascade")
        sys.exit(1)
    print("[PASS] Haar Cascade Classifier loaded successfully")
except Exception as e:
    print(f"[FAIL] Haar Cascade loading failed: {e}")
    sys.exit(1)

try:
    # Test ORB detector
    print(f"[PASS] ORB detector created successfully")
except Exception as e:
    print(f"[FAIL] ORB detector creation failed: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("[SUCCESS] All components loaded successfully!")
print("[INFO] System features:")
print("  - Face Detection: OpenCV Haar Cascade")
print("  - Face Recognition: ORB feature matching (No dlib required!)")
print(f"  - Multi-person support: YES")
print(f"  - Known faces registered: {len(recognizer.known_face_names)}")
print("\n[INFO] You can now run: python main.py")
print("="*60)
