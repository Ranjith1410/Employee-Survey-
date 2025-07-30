from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Survey
from audit import log_audit, save_survey_to_csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    survey = user.survey

    if request.method == 'POST':
        department = request.form['department']
        age = request.form['age']
        gender = request.form['gender']
        rating = request.form['rating']
        job_satisfaction = request.form['job_satisfaction']
        work_life_balance = request.form['work_life_balance']
        comments = request.form['comments']
        suggestions = request.form['suggestions']

        if user.survey:
            return "Survey already submitted"

        new_survey = Survey(
            user_id=user.id,
            department=department,
            age=age,
            gender=gender,
            rating=rating,
            job_satisfaction=job_satisfaction,
            work_life_balance=work_life_balance,
            comments=comments,
            suggestions=suggestions
        )
        db.session.add(new_survey)
        db.session.commit()
        save_survey_to_csv(new_survey, user.username)
        log_audit(user.username, 'Submitted survey')
        return render_template('thankyou.html')

    return render_template('index.html', user=user, survey=survey)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return "Username already exists"
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/edit/<int:survey_id>', methods=['GET', 'POST'])
def edit_survey(survey_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    survey = Survey.query.get_or_404(survey_id)
    user = User.query.get(session['user_id'])
    if survey.user_id != user.id:
        return "Unauthorized access"

    if request.method == 'POST':
        survey.department = request.form['department']
        survey.age = request.form['age']
        survey.gender = request.form['gender']
        survey.rating = request.form['rating']
        survey.job_satisfaction = request.form['job_satisfaction']
        survey.work_life_balance = request.form['work_life_balance']
        survey.comments = request.form['comments']
        survey.suggestions = request.form['suggestions']
        db.session.commit()
        log_audit(user.username, 'Edited survey')
        save_survey_to_csv(survey, user.username)
        return redirect(url_for('index'))

    return render_template('edit.html', survey=survey)

@app.route('/delete/<int:survey_id>', methods=['POST', 'GET'])
def delete_survey(survey_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    survey = Survey.query.get_or_404(survey_id)
    user = User.query.get(session['user_id'])
    if survey.user_id != user.id:
        return "Unauthorized access"

    db.session.delete(survey)
    db.session.commit()
    log_audit(user.username, 'Deleted survey')
    return redirect(url_for('index'))

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        # process and save survey
        department = request.form['department']
        age = request.form['age']
        gender = request.form['gender']
        rating = request.form['rating']
        job_satisfaction = request.form['job_satisfaction']
        work_life_balance = request.form['work_life_balance']
        comments = request.form['comments']
        suggestions = request.form['suggestions']

        new_survey = Survey(
            user_id=user.id,
            department=department,
            age=age,
            gender=gender,
            rating=rating,
            job_satisfaction=job_satisfaction,
            work_life_balance=work_life_balance,
            comments=comments,
            suggestions=suggestions
        )
        db.session.add(new_survey)
        db.session.commit()
        save_survey_to_csv(new_survey, user.username)
        log_audit(user.username, 'Submitted survey')
        return render_template('thankyou.html')
    return render_template('survey.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
