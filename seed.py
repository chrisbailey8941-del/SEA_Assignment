from app import app, db
from models import User, CancerSite, PatientRecord

def seed_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        lung = CancerSite(site_name="Lung")
        bowel = CancerSite(site_name="Colorectal")
        breast = CancerSite(site_name="Breast")
        uro = CancerSite(site_name="Urology")
        skin = CancerSite(site_name="Skin")
        upper_gi = CancerSite(site_name="Upper GI")
        db.session.add_all([lung, bowel, breast, uro, skin, upper_gi])

        admin = User(username="admin_user", password="Admin123", role="admin")
        staff = User(username="staff_user", password="Staff456", role="regular")
        db.session.add_all([admin, staff])
        db.session.commit()

        patients = [

            PatientRecord(nhs_number="1112223334", forename="Alice", surname="Smith", t_stage="T1", n_stage="N0",
                          m_stage="M0",
                          performance_status=0, first_treatment_type="Surgery", cns_contact=True, site_id=lung.id,
                          user_id=staff.id),


            PatientRecord(nhs_number="2223334445", forename="Bob", surname="Jones", t_stage="T4", n_stage="N2",
                          m_stage="M1",
                          performance_status=3, first_treatment_type="Palliative Care", cns_contact=True,
                          site_id=bowel.id, user_id=staff.id),


            PatientRecord(nhs_number="3334445556", forename="Charlie", surname="Brown", t_stage=None, n_stage=None,
                          m_stage=None,
                          performance_status=None, first_treatment_type=None, cns_contact=False, site_id=breast.id,
                          user_id=staff.id),


            PatientRecord(nhs_number="4445556667", forename="Diana", surname="Prince", t_stage="T2", n_stage="N0",
                          m_stage=None,
                          performance_status=1, first_treatment_type=None, cns_contact=True, site_id=uro.id,
                          user_id=staff.id),


            PatientRecord(nhs_number="5556667778", forename="Edward", surname="Norton", t_stage="T1", n_stage="N0",
                          m_stage="M0",
                          performance_status=0, first_treatment_type="Surgery", cns_contact=True, site_id=skin.id,
                          user_id=staff.id),


            PatientRecord(nhs_number="6667778889", forename="Fiona", surname="Gallagher", t_stage="T3", n_stage="N1",
                          m_stage="M0",
                          performance_status=2, first_treatment_type="Chemotherapy", cns_contact=False,
                          site_id=upper_gi.id, user_id=staff.id),


            PatientRecord(nhs_number="7778889990", forename="George", surname="Miller", t_stage=None, n_stage=None,
                          m_stage=None,
                          performance_status=None, first_treatment_type=None, cns_contact=False, site_id=lung.id,
                          user_id=staff.id),


            PatientRecord(nhs_number="8889990001", forename="Hannah", surname="Abbott", t_stage="T2", n_stage="N0",
                          m_stage="M0",
                          performance_status=1, first_treatment_type="Surgery", cns_contact=True, site_id=uro.id,
                          user_id=staff.id),


            PatientRecord(nhs_number="9990001112", forename="Ian", surname="Wright", t_stage=None, n_stage=None,
                          m_stage=None,
                          performance_status=4, first_treatment_type="Supportive Care", cns_contact=True,
                          site_id=skin.id, user_id=staff.id),

            PatientRecord(nhs_number="0001112223", forename="Jenny", surname="Slate", t_stage="T3", n_stage="N0",
                          m_stage="M0",
                          performance_status=1, first_treatment_type="Radiotherapy", cns_contact=True,
                          site_id=upper_gi.id, user_id=staff.id)
        ]

        db.session.add_all(patients)
        db.session.commit()
        print(f"Database seeded with {len(patients)} patients across 6 specialties!")


if __name__ == "__main__":
    seed_database()