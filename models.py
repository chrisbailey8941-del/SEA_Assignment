from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# User table creation, to define the different roles
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='regular')

# Cancer Site table creation
class CancerSite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(50), unique=True, nullable=False)
    patients = db.relationship('PatientRecord', backref='specialty', lazy=True)

# Patient Record table creation
class PatientRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nhs_number = db.Column(db.String(10), unique=True, nullable=False)
    forename = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    t_stage = db.Column(db.String(5))
    n_stage = db.Column(db.String(5))
    m_stage = db.Column(db.String(5))
    performance_status = db.Column(db.Integer)
    first_treatment_type = db.Column(db.String(50))
    cns_contact = db.Column(db.Boolean, default=False)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('cancer_site.id'))