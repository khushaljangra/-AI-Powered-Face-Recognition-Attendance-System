import os
import pandas as pd
from datetime import datetime

ATTENDANCE_DIR = "attendance"
COOLDOWN_SECONDS = 60

# Simple in-memory cooldown tracker: {name: last_time}
last_marked = {}

def mark_attendance(name):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    # Check cooldown
    if name in last_marked:
        time_diff = (now - last_marked[name]).total_seconds()
        if time_diff < COOLDOWN_SECONDS:
            return False, "Cooldown active"

    csv_path = os.path.join(ATTENDANCE_DIR, f"attendance_{date_str}.csv")
    excel_path = os.path.join(ATTENDANCE_DIR, f"attendance_{date_str}.xlsx")

    # Entry data
    status = "Present" # Could add logic for "Late" based on a cutoff time
    new_entry = {"Name": name, "Time": time_str, "Status": status}

    # Save to CSV
    if not os.path.exists(csv_path):
        df = pd.DataFrame(columns=["Name", "Time", "Status"])
    else:
        df = pd.read_csv(csv_path)

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(csv_path, index=False)

    # Save to Excel
    df.to_excel(excel_path, index=False)

    # Update cooldown
    last_marked[name] = now
    return True, f"Attendance marked for {name}"

def get_today_attendance():
    date_str = datetime.now().strftime("%Y-%m-%d")
    csv_path = os.path.join(ATTENDANCE_DIR, f"attendance_{date_str}.csv")
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path).to_dict('records')
    return []
