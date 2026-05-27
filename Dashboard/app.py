from flask import Flask, jsonify, render_template
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LogHound.failed_logins import detect_failed_logins
from LogHound.new_ip import new_ip_login
from LogHound.new_location import new_location_login

app = Flask(__name__, template_folder='templates')

@app.route('/alerts')
def get_alerts():
    alerts = []
    alerts += detect_failed_logins()
    alerts += new_ip_login()
    alerts += new_location_login()
    return jsonify(alerts)

@app.route('/')
def home():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)