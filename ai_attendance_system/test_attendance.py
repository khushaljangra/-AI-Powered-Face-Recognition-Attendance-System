from attendance import AttendanceManager
import os
import shutil

def test():
    if os.path.exists("test_attendance"):
        shutil.rmtree("test_attendance")
    
    manager = AttendanceManager(attendance_dir="test_attendance")
    print("Manager initialized")
    
    success, status = manager.mark_attendance("Test User")
    print(f"Marked attendance: {success}, {status}")
    
    present, absent = manager.get_today_stats(["Test User", "Absent User"])
    print(f"Present: {present}")
    print(f"Absent: {absent}")
    
    excel = manager.export_to_excel()
    print(f"Excel path: {excel}")

if __name__ == "__main__":
    test()
