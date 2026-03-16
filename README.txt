* CANCER AUDIT DASHBOARD                                                      
* Installation & Operations Guide                                             


1. LINKS
==================

REPOS: https://github.com/chrisbailey8941-del/SEA_Assignment/tree/app
RENDER: https://sea-assignment-6lkd.onrender.com/

2. LOCAL INSTALLATION & DATABASE SEEDING
========================================
To set up a local copy with the full audit dataset:

1. Ensure Python 3.9+ is installed.
2. Open terminal in the project root directory.
3. Install dependencies:
   > pip install flask flask-sqlalchemy flask-login pytest

4. SEED THE DATABASE:
   Run the following command to create the 'database.db' file and populate
   it with clinical test records and authenticated user accounts:
   > python seed.py

5. Run the application:
   > python app.py

6. Access via browser at: http://127.0.0.1:5000

3. SYSTEM TESTING
=================
To run the automated Pytest suite (Login, CRUD, and Audit logic):
   > python -m pytest

4. RUNNING VIA RENDER (LIVE CLOUD DEPLOYMENT)
=============================================
To access the application immediately without local installation:

1. Navigate to: https://sea-assignment-6lkd.onrender.com/
2. NOTE: The first load may take up to 60 seconds.
3. IMPORTANT: If the page fails to load or shows a timeout error on the first 
   attempt, please Refresh the webpage. 

5. USER GUIDE
=============
- LOGGING IN: Use 'Admin' or 'Staff' credentials.

- DASHBOARD: High-visibility "MISSING" flags highlight gaps in mandatory 
  audit fields such as TNM Staging and Performance Status.

- SEARCHING: Use the search bar at the top of the dashboard to filter 
  the record list by NHS Number or Surname.

- CREATING RECORDS: 
  Click the "Add Patient" button. Complete the clinical form. Note that the 
  system enforces data integrity by blocking duplicate NHS Numbers.

- EDITING RECORDS: 
  Click the "Edit" button on a specific patient row. This allows for the 
  completion of previously missing data as it becomes clinically available.

- DELETING RECORDS: 
  * Click the Delete button on the right hand side of the record that you wish to delete.
  * Only users with 'Admin' privileges will see the "Delete" option. 
  * 'Staff' users are restricted from deleting records to ensure 
    clinical data governance.

