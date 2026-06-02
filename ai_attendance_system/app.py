from flask import Flask, render_template, send_from_directory
from face_recognition_improved import ImprovedFaceRecognizer
from attendance import AttendanceManager
from datetime import datetime
import os

app = Flask(__name__)

# Initialize managers
attendance_manager = AttendanceManager(attendance_dir="attendance")
face_recognizer = ImprovedFaceRecognizer(known_faces_dir="known_faces")

@app.route('/known_faces/<path:filename>')
def serve_face(filename):
    return send_from_directory('known_faces', filename)

@app.route('/')
def index():
    # Load current face data
    face_recognizer.load_features()
    all_known_names = face_recognizer.known_face_names
    
    # Get today's stats
    present_list, absent_list = attendance_manager.get_today_stats(all_known_names)
    
    # Sort present_list by time (descending) so newest is on top
    present_list.reverse()
    
    return render_template('index.html',
                           present_list=present_list,
                           absent_list=absent_list,
                           present_count=len(present_list),
                           absent_count=len(absent_list),
                           registered_count=len(all_known_names),
                           date=datetime.now().strftime("%Y-%m-%d"),
                           time=datetime.now().strftime("%H:%M:%S"))

@app.route('/reset')
def reset():
    try:
        attendance_dir = "attendance"
        if os.path.exists(attendance_dir):
            for f in os.listdir(attendance_dir):
                os.remove(os.path.join(attendance_dir, f))
        return "All attendance records have been reset successfully! <a href='/'>Go Back</a>"
    except Exception as e:
        return f"Error resetting data: {e}"

@app.route('/export')
def export():
    path = attendance_manager.export_to_excel()
    if path:
        return f"Report exported to {path}"
    return "No records found for today."

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs("attendance", exist_ok=True)
    os.makedirs("known_faces", exist_ok=True)
    
    print("[INFO] Starting Flask Dashboard on http://127.0.0.1:5000")
    print("[INFO] Press Ctrl+C to stop")
    app.run(debug=True, port=5000)
