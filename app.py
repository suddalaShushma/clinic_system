from flask import Flask, render_template, request, redirect, url_for
from models import db, Patient, Visit
import qrcode
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables within application context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    contact = request.form['contact']
    address = request.form['address']

    patient = Patient(name=name, age=age, gender=gender, contact=contact, address=address)
    db.session.add(patient)
    db.session.commit()

    visit = Visit(patient_id=patient.id)
    db.session.add(visit)
    db.session.commit()

    # Generate QR code
    token = f'{patient.id}-{visit.id}'
    visit.token = token
    db.session.commit()

    img = qrcode.make(token)
    os.makedirs('static/qrcodes', exist_ok=True)
    img.save(f'static/qrcodes/{token}.png')

    return render_template('token.html', token=token)

@app.route('/doctor')
def doctor():
    patients = Patient.query.all()
    return render_template('doctor.html', patients=patients)

@app.route('/patient/<int:id>')
def patient_details(id):
    patient = Patient.query.get(id)
    visits = Visit.query.filter_by(patient_id=id).all()
    return render_template('patient_details.html', patient=patient, visits=visits)

if __name__ == '__main__':
    app.run(debug=True)
