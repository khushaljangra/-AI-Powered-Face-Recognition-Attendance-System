from flask import Flask, render_template
from attendance import get_today_attendance
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    attendance_data = get_today_attendance()
    today_date = datetime.now().strftime("%Y-%m-%d")
    return render_template('index.html', attendance=attendance_data, date=today_date)

if __name__ == '__main__':
    app.run(debug=True)
