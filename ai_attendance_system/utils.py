import cv2
import numpy as np
import os
from datetime import datetime
from scipy.spatial import distance as dist

def calculate_ear(eye):
    # Compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    # Compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])
    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear

def draw_overlay(frame, name, status, color=(0, 255, 0)):
    cv2.putText(frame, f"Name: {name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(frame, f"Status: {status}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

def save_unknown(frame):
    if not os.path.exists("unknown_faces"):
        os.makedirs("unknown_faces")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cv2.imwrite(f"unknown_faces/unknown_{timestamp}.jpg", frame)
