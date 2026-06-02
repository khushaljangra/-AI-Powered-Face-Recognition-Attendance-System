# AI-Powered Face Recognition Attendance System

A production-ready attendance system using Python, OpenCV, and Flask.

## Features
- **Real-time Recognition**: Detects and recognizes multiple faces simultaneously.
- **Attendance Logging**: Automatically marks "Present" or "Late" in CSV and Excel.
- **Cooldown Mechanism**: Prevents duplicate entries within 60 seconds.
- **Unknown Face Logging**: Saves images of unrecognized people for security.
- **Web Dashboard**: A beautiful Flask-based UI to view live attendance stats.
- **Registration**: Register new users directly via the webcam.
- **Anti-Spoofing**: Basic eye-blink detection to ensure live presence.

## Project Structure
- `main.py`: The core recognition and webcam application.
- `app.py`: The Flask web dashboard.
- `face_encoder.py`: Handles face dataset and encoding.
- `attendance.py`: Manages attendance rules and storage.
- `utils.py`: UI drawing and helper utilities.
- `known_faces/`: Put images of people here (e.g., `john_doe.jpg`).
- `unknown_faces/`: Where unrecognized faces are saved.
- `attendance/`: CSV and Excel reports.

## Setup Instructions

### 1. Requirements
Ensure you have Python 3.8+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
*Note: If you are on Windows and face issues with `dlib` (required by `face_recognition`), you may need to install Visual Studio with "Desktop development with C++" and "CMake".*

### 3. Add Known Faces
Place high-quality images of people you want to recognize in the `known_faces/` folder. Name the files as `PersonName.jpg`.

### 4. Run the System

#### Start the Recognition App (Webcam)
```bash
python main.py
```
- Press **'q'** to quit.
- Press **'r'** to register a new person on the fly.

#### Start the Web Dashboard
Open a new terminal and run:
```bash
python app.py
```
View the dashboard at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## How It Works
1. `face_encoder` loads images from `known_faces/`, generates 128-d encodings, and saves them to `encodings.pickle`.
2. `main.py` captures frames from the webcam and compares them against known encodings.
3. If a match is found (distance < 0.6), attendance is marked in a daily CSV file.
4. `app.py` reads the CSV and updates the web table every 5 seconds.

## License
MIT
