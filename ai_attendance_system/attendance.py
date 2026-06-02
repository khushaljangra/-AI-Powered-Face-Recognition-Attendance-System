import pandas as pd
from datetime import datetime
import os

class AttendanceManager:
    def __init__(self, attendance_dir="attendance", late_threshold="09:15:00"):
        self.attendance_dir = attendance_dir
        self.late_threshold = late_threshold
        self.cooldown_dict = {}  # {name: last_marked_time}
        self.cooldown_seconds = 60
        
        if not os.path.exists(self.attendance_dir):
            os.makedirs(self.attendance_dir)

    def get_csv_path(self):
        date_str = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.attendance_dir, f"attendance_{date_str}.csv")

    def mark_attendance(self, name):
        """Marks attendance for a person if they are not in cooldown."""
        now = datetime.now()
        current_time_str = now.strftime("%H:%M:%S")
        
        # Check cooldown
        if name in self.cooldown_dict:
            time_diff = (now - self.cooldown_dict[name]).total_seconds()
            if time_diff < self.cooldown_seconds:
                return False, f"Cooldown: {int(self.cooldown_seconds - time_diff)}s"

        # Determine status
        status = "Present"
        if current_time_str > self.late_threshold:
            status = "Late"

        # Save to CSV
        csv_path = self.get_csv_path()
        data = {
            "Name": [name],
            "Time": [current_time_str],
            "Date": [now.strftime("%Y-%m-%d")],
            "Status": [status]
        }
        df = pd.DataFrame(data)

        if not os.path.isfile(csv_path):
            df.to_csv(csv_path, index=False)
        else:
            df.to_csv(csv_path, mode='a', header=False, index=False)

        # Update cooldown
        self.cooldown_dict[name] = now
        print(f"[LOG] Attendance marked for {name} at {current_time_str} ({status})")
        return True, status

    def get_today_stats(self, all_known_names):
        """Returns present and absent lists for today."""
        csv_path = self.get_csv_path()
        if not os.path.exists(csv_path):
            return [], all_known_names

        df = pd.read_csv(csv_path)
        present_names = df["Name"].unique().tolist()
        absent_names = [name for name in all_known_names if name not in present_names]
        
        # Format present data for display
        present_data = df.to_dict('records')
        return present_data, absent_names

    def export_to_excel(self):
        """Converts the daily CSV to Excel."""
        csv_path = self.get_csv_path()
        if not os.path.exists(csv_path):
            return None
        
        excel_path = csv_path.replace(".csv", ".xlsx")
        df = pd.read_csv(csv_path)
        df.to_excel(excel_path, index=False)
        return excel_path
