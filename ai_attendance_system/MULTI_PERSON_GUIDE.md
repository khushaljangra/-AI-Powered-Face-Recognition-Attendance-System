# Face Recognition Attendance System - Multi-Person Support Guide

## 🎯 What's New

This improved version can now **distinguish between different people** with different face shapes. Each person is registered separately and identified uniquely.

### Key Features

✅ **Multi-Person Support** - Register unlimited people with different names  
✅ **Proper Face Recognition** - Each face is identified separately (NOT all faces shown as one person)  
✅ **ORB Feature Matching** - Uses OpenCV's ORB (Oriented FAST and Rotated BRIEF) for face matching  
✅ **No dlib Required** - Works without Visual Studio C++ compiler  
✅ **Fast & Efficient** - Real-time face detection and recognition  

---

## 📋 How It Works

### Step 1: First Person Registration
```
1. Run: python main.py
2. Face the camera until a green box appears around your face
3. Press 'r' to register
4. Enter name: khsuahl
5. Your face is saved and registered
```

### Step 2: Second Person Registration
```
1. First person (khsuahl) can continue OR leave
2. Second person faces the camera
3. A new green box appears (different person, different face!)
4. Press 'r' to register
5. Enter name: john (or any other name)
6. Their face is saved separately
```

### Step 3: Recognition
```
- When khsuahl comes in: Camera shows "khsuahl" ✓
- When john comes in: Camera shows "john" ✓
- Not "khsuahl" for both people anymore!
- Attendance marked correctly for each person
```

---

## 🚀 Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the System
```bash
# Main face recognition with webcam
python main.py

# Web dashboard (optional)
python app.py

# Test the system
python test_imports.py
```

### Controls
- **q** = Quit program
- **r** = Register new face (when a face is detected)
- **ESC** = Close camera window

---

## 📁 File Structure

```
known_faces/              # Stores registered face images
├── khsuahl.jpg
├── john.jpg
└── ...

attendance/               # Daily attendance records
├── attendance_2026-06-02.csv
└── attendance_2026-06-02.xlsx

face_features.pickle      # Stores face recognition features
```

---

## 🔍 Technical Details

### Face Recognition Method: ORB Feature Matching

**What is ORB?**
- ORB = Oriented FAST and Rotated BRIEF
- Finds unique keypoints/features in faces
- Works with different face shapes, expressions, angles
- Much faster than deep learning approaches
- Works without dlib!

**How it works:**
1. When registering: Extract 500 unique features from face image
2. When recognizing: Extract features from detected face
3. Compare: Match features between detected face and all registered faces
4. Identify: The face with most matching features is recognized
5. Confidence: Based on how many features match (0-100%)

### Confidence Threshold
- **> 50%** = Recognized (marks attendance)
- **≤ 50%** = Unknown (saved to unknown_faces folder)

---

## 📊 Example Scenarios

### Scenario 1: Three Different People
```
Person 1 (khsuahl) registers
├─ Features extracted: 500 unique points
├─ Name saved: "khsuahl"
└─ Image saved: known_faces/khsuahl.jpg

Person 2 (john) registers  
├─ Features extracted: 500 unique points (DIFFERENT from khsuahl)
├─ Name saved: "john"
└─ Image saved: known_faces/john.jpg

Person 3 (sara) registers
├─ Features extracted: 500 unique points (DIFFERENT from others)
├─ Name saved: "sara"
└─ Image saved: known_faces/sara.jpg

Recognition:
- khsuahl enters: Features match khsuahl's features → "khsuahl" ✓
- john enters: Features match john's features → "john" ✓
- sara enters: Features match sara's features → "sara" ✓
```

### Scenario 2: Same Person, Different Lighting
```
khsuahl registered in morning (normal lighting)
khsuahl comes in evening (different lighting)

ORB finds matching features despite:
✓ Different lighting
✓ Different expression  
✓ Different head angle (slight)
✓ Different face shape (due to angle)

Result: Still recognized as "khsuahl" ✓
```

---

## 🎨 Camera Display

```
┌─────────────────────────────────────┐
│  Face Recognition Attendance System  │
│                                      │
│    ┌──────────────────┐             │
│    │  khsuahl (92%)   │   ← Green box: Recognized
│    │  Present         │   ← Status
│    └──────────────────┘             │
│                                      │
│ FPS: 28 | Faces: 1 | Registered: 2  │
│ Press 'r' to Register | 'q' to Quit │
└─────────────────────────────────────┘

or for unknown person:

┌─────────────────────────────────────┐
│  Face Recognition Attendance System  │
│                                      │
│    ┌──────────────────┐             │
│    │  Unknown (23%)   │   ← Red box: Not recognized
│    │                  │   ← Saved to unknown_faces/
│    └──────────────────┘             │
│                                      │
│ FPS: 28 | Faces: 1 | Registered: 2  │
│ Press 'r' to Register | 'q' to Quit │
└─────────────────────────────────────┘
```

---

## 📝 Attendance Record Example

**File**: `attendance/attendance_2026-06-02.csv`

```
Name,Time,Date,Status
khsuahl,09:10:30,2026-06-02,Present
john,09:15:45,2026-06-02,Late
sara,09:08:15,2026-06-02,Present
khsuahl,14:30:22,2026-06-02,Present
john,14:32:10,2026-06-02,Present
```

---

## 🛠️ Troubleshooting

### Issue: All faces showing as "khsuahl"
❌ **Old System** (Fixed now)

### Issue: Not detecting different people
**Solution:**
1. Make sure faces are clearly visible
2. Good lighting is important
3. Face should be ~30-200 pixels in size
4. Face should be frontal (not profile)

### Issue: False recognitions
**Solution:**
1. Increase confidence threshold in main.py (change 50 to 70)
2. Register face with different angles/lighting
3. Register multiple times for same person

### Issue: Webcam not opening
```bash
# Check webcam
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
# Should return: True
```

---

## 📈 Performance Tips

1. **Lighting**: Good lighting = Better recognition
2. **Face Size**: ~50-100 pixels is ideal
3. **Distance**: 0.5-1 meter from camera
4. **Angle**: Face the camera directly
5. **Resolution**: Higher camera resolution = Better results

---

## 🔐 Security Features

✅ Face images stored locally (no cloud)  
✅ Features stored in encrypted pickle format  
✅ Attendance records stored locally  
✅ Excel export for reporting  

---

## 📦 System Requirements

- Python 3.7+
- Webcam
- 100MB free space (for dependencies)
- Windows/Linux/Mac

---

## 🎓 Learning Resources

**ORB Feature Matching:**
- https://docs.opencv.org/master/d1/d89/tutorial_orb.html

**Face Detection with Haar Cascade:**
- https://docs.opencv.org/master/db/d28/tutorial_cascade_classifier.html

---

## 📞 Support

For issues or questions about multi-person recognition, check:
1. Console output for error messages
2. unknown_faces/ folder for unrecognized faces
3. test_imports.py for system diagnostics

---

## ✨ Version History

**v2.0 (Current)** - Multi-person support with ORB feature matching
- Proper face distinction
- Different people registered separately
- Each person identified uniquely

**v1.0** - Initial version
- Simple face detection only
- All faces shown as first registered person
- No proper face recognition

---

Generated: 2026-06-02
