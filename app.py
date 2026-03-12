import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, PatientRecord, CancerSite

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cancer-audit-secret-123'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
@login_required
def index():
    search_query = request.args.get('search', '')
    if search_query:
        patients = PatientRecord.query.filter(
            (PatientRecord.nhs_number.contains(search_query)) |
            (PatientRecord.surname.contains(search_query))
        ).all()
    else:
        patients = PatientRecord.query.order_by(PatientRecord.surname).all()

    return render_template('index.html', patients=patients, search_query=search_query)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_patient():
    sites = CancerSite.query.all()
    if request.method == 'POST':
        new_patient = PatientRecord(
            nhs_number=request.form.get('nhs_number'),
            forename=request.form.get('forename'),
            surname=request.form.get('surname'),
            site_id=request.form.get('site_id'),
            t_stage=request.form.get('t_stage'),
            n_stage=request.form.get('n_stage'),
            m_stage=request.form.get('m_stage'),
            performance_status=request.form.get('performance_status'),
            first_treatment_type=request.form.get('treatment'),
            cns_contact='cns_contact' in request.form,
            user_id=current_user.id
        )

        db.session.add(new_patient)
        db.session.commit()
        flash(f'New record created for {new_patient.surname}')
        return redirect(url_for('index'))

    return render_template('create.html', sites=sites)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_patient(id):
    patient = PatientRecord.query.get_or_404(id)
    sites = CancerSite.query.all()

    if request.method == 'POST':
        new_t = request.form.get('t_stage')
        new_n = request.form.get('n_stage')
        new_m = request.form.get('m_stage')
        new_ps = request.form.get('performance_status')

        valid_t = ['T1', 'T2', 'T3', 'T4', 'Tx', '']
        valid_n = ['N0', 'N1', 'N2', 'Nx', '']
        valid_m = ['M0', 'M1', '']

        if new_t not in valid_t or new_n not in valid_n or new_m not in valid_m:
            flash("Error: Invalid TNM Stage selected.")
            return redirect(url_for('edit_patient', id=id))

        if new_ps and (int(new_ps) < 0 or int(new_ps) > 4):
            flash('Error: Performance Status must be 0-4.')
            return redirect(url_for('edit_patient', id=id))

        patient.t_stage = new_t
        patient.n_stage = new_n
        patient.m_stage = new_m
        patient.performance_status = new_ps
        patient.first_treatment_type = request.form.get('treatment')
        patient.cns_contact = 'cns_contact' in request.form
        patient.site_id = request.form.get('site_id')

        db.session.commit()
        flash(f'Updated record for {patient.surname}')
        return redirect(url_for('index'))

    return render_template('edit.html', patient=patient, sites=sites)


@app.route('/delete/<int:id>')
@login_required
def delete_patient(id):
    if current_user.role != 'admin':
        flash('Access Denied: Only Admins can delete records.')
        return redirect(url_for('index'))
    patient = PatientRecord.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Record deleted successfully.')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)