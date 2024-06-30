from flask import Flask, render_template, redirect, url_for, request, session, flash # type: ignore
# from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        profile_picture = request.files.get('profile_picture')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        address_line1 = request.form.get('address_line1')
        city = request.form.get('city')
        state = request.form.get('state')
        pincode = request.form.get('pincode')
        user_type = request.form.get('user_type')

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=hashed_password,
            address_line1=address_line1,
            city=city,
            state=state,
            pincode=pincode,
            user_type=user_type
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_type'] = user.user_type
            if user.user_type == 'patient':
                return redirect(url_for('dashboard_patient'))
            elif user.user_type == 'doctor':
                return redirect(url_for('dashboard_doctor'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard_patient')
def dashboard_patient():
    if 'user_id' in session and session['user_type'] == 'patient':
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('dashboard_patient.html', user=user)
    return redirect(url_for('login'))

@app.route('/dashboard_doctor')
def dashboard_doctor():
    if 'user_id' in session and session['user_type'] == 'doctor':
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('dashboard_doctor.html', user=user)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
