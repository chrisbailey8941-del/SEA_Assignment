import pytest
from app import app, db
from models import PatientRecord

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

# 1. Test: Can both roles login?
def test_01_login_roles(client):
    res = client.post('/login', data={'username': 'admin_user', 'password': 'Admin123'}, follow_redirects=True)
    assert b"admin_user" in res.data
    res2 = client.post('/login', data={'username': 'staff_user', 'password': 'Staff456'}, follow_redirects=True)
    assert b"staff_user" in res2.data

# 2. Test: Can we create a new record?
def test_02_create_record(client):
    client.post('/login', data={'username': 'admin_user', 'password': 'Admin123'})
    client.post('/create', data={'nhs_number': '999111', 'forename': 'Test', 'surname': 'Patient', 'site_id': 1})
    assert PatientRecord.query.filter_by(nhs_number='999111').first() is not None

# 3. Test: Is data viewable on the dashboard?
def test_03_view_data(client):
    client.post('/login', data={'username': 'staff_user', 'password': 'Staff456'})
    res = client.get('/')
    assert b"Smith" in res.data

# 4. Test: Does it flag "MISSING" data?
def test_04_audit_alerts(client):
    client.post('/login', data={'username': 'staff_user', 'password': 'Staff456'})
    res = client.get('/')
    assert b"MISSING" in res.data

# 5. Test: Are staff blocked from deleting?
def test_05_staff_security(client):
    client.post('/login', data={'username': 'staff_user', 'password': 'Staff456'})
    res = client.get('/delete/1', follow_redirects=True)
    assert b"Access Denied" in res.data