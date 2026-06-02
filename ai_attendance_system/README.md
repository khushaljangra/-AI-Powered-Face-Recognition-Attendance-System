# 🎯 AI-Powered Face Recognition Attendance System

A **production-ready smart attendance system** built using **Python, OpenCV, Face Recognition, and Flask**, designed for real-time face detection, recognition, and automated attendance tracking.

---

## ✨ Key Features

🔍 **Real-time Face Recognition**
Detects and recognizes multiple faces simultaneously using webcam feed.

📊 **Automated Attendance Logging**
Marks attendance as **Present / Late** and stores it in **CSV & Excel formats**.

⏱️ **Smart Cooldown System**
Prevents duplicate entries within a configurable time window (default: 60 seconds).

🚨 **Unknown Face Detection**
Captures and stores images of unrecognized individuals for security monitoring.

🌐 **Interactive Web Dashboard**
Live attendance tracking using a clean and responsive **Flask UI**.

📸 **On-the-Fly User Registration**
Register new users directly through webcam without restarting the system.

🧠 **Basic Anti-Spoofing**
Implements eye-blink detection to reduce fake attendance attempts.

---

## 🗂️ Project Structure

```
├── main.py              # Core face recognition system
├── app.py               # Flask dashboard backend
├── face_encoder.py      # Face encoding logic
├── attendance.py        # Attendance handling & rules
├── utils.py             # Helper functions & UI overlays
│
├── known_faces/         # Known user images
├── unknown_faces/       # Unknown detected faces
├── attendance/          # CSV & Excel logs
├── encodings.pickle     # Stored face encodings
```

---

## ⚙️ Installation & Setup

### 1️⃣ Prerequisites

* Python 3.8+
* Webcam

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

⚠️ **Windows Users Note**
If `dlib` fails to install:

* Install **Visual Studio Build Tools**
* Enable:

  * Desktop Development with C++
  * CMake Tools

---

### 3️⃣ Add Known Faces

* Add images inside `known_faces/`
* Naming format:

```
John_Doe.jpg
```

---

### 4️⃣ Run the Application

#### ▶️ Start Face Recognition

```bash
python main.py
```

Controls:

* Press **Q** → Quit
* Press **R** → Register new user

---

#### 🌐 Start Web Dashboard

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## ⚙️ How It Works

1. Face images are encoded into **128-d vectors** using `face_encoder.py`.
2. Webcam feed is processed in real-time (`main.py`).
3. Faces are matched using distance threshold (< 0.6).
4. Attendance is stored in daily logs.
5. Flask dashboard auto-refreshes every 5 seconds.

---

## 📜 License

MIT License

---

## 🙌 Author

Developed by **Khushal Choyal**
