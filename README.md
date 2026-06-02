 I have successfully built the AI-Powered Face Recognition Attendance System for you. The project is structured,
  modular, and ready for production use.

  📂 Project Structure

    1 ai_attendance_system/
    2 ├── main.py              # Core real-time recognition engine
    3 ├── app.py               # Flask web dashboard backend
    4 ├── face_encoder.py      # Face encoding logic
    5 ├── attendance.py        # Attendance logging & cooldown rules
    6 ├── utils.py             # Helper functions (UI overlays, unknown captures)
    7 ├── known_faces/         # Directory for user images (e.g., John_Doe.jpg)
    8 ├── unknown_faces/       # Captures of unrecognized individuals
    9 ├── attendance/          # CSV & Excel logs (auto-generated)
   10 ├── templates/           # Flask HTML dashboard
   11 └── requirements.txt     # Project dependencies

  🚀 How to Run

   1. Install Dependencies:
   1     pip install -r requirements.txt

   2. Add Known Faces:
      Place images of users inside the known_faces/ folder. Name them as Name_Surname.jpg.

   3. Generate Encodings:
      Run this script once (or whenever you add new faces) to process the images:
   1     python face_encoder.py

   4. Start Recognition:
   1     python main.py
       * Press 'Q' to quit.
       * Press 'R' to register a new user on the fly (it will ask for a name in the terminal).

   5. View Dashboard:
      Start the Flask server:
   1     python app.py
      Open http://127.0.0.1:5000 in your browser to see real-time attendance logs.

  🛡️ Features Included:
   * Smart Cooldown: Prevents double-marking the same person within 60 seconds.
   * Dual Logging: Attendance is saved in both CSV (for speed) and Excel (for reporting).
   * Unknown Tracking: Automatically captures and stores images of unrecognized faces.
   * Interactive UI: A clean, Bootstrap-powered dashboard that auto-refreshes every 5 seconds.
   * On-the-fly Registration: Register users directly via webcam while the system is running.
