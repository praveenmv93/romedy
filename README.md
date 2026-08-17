# Romedy Clinic Portal

A modern, clinical-grade medical portal featuring a slot-based patient appointment booking system, a staff check-in desk, doctor dashboards, a PDF consultation report generator, and a tabbed Medical Knowledge Hub.

The application has been styled with a stress-relieving, warm linen-cream and sage design system to reduce screen fatigue and improve user experience.

---

## Getting Started

### 1. Prerequisite Setup
Ensure Python 3.12+ is installed, then create and activate a virtual environment:
```bash
cd equipo
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
Install the required python modules listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Database & Migrations
Migrate the database to initialize the SQL + NoSQL hybrid tables in `hospital_db.sqlite3`:
```bash
python manage.py migrate
```

### 4. Start the Application
Run the Django local development server:
```bash
python manage.py runserver
```
Access the website in your browser at **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**.

---

## Test Credentials

Use these sample credentials to navigate the patient booking wizard, staff queue desks, and doctor workspaces:

### 1. Patient Account
- **Username**: `patient_john`
- **Password**: `patientpassword123`
- **Access**: Can view patient medical guides, book consultations, and schedule doctor slots.

### 2. Hospital Operations Staff Account
- **Username**: `staff_ops`
- **Password**: `staffpassword123`
- **Access**: Manages the central check-in queue, checks in arrived patients, and dynamically allocates doctors.

### 3. Physician Accounts
* **Cardiology Specialist**:
  - **Username**: `dr_sarah`
  - **Password**: `doctorpassword123`
* **Pediatric Specialist**:
  - **Username**: `dr_robert`
  - **Password**: `doctorpassword123`
- **Access**: Accesses the clinical consultation queue, reviews checked-in patients, pre-fills consultation fields, and generates WeasyPrint PDF reports.

---

## Key Features

1. **Breathing-Rings Loader**: A unique CSS + SVG medical preloader mimicking deep breathing exercises to ease clinic anxiety during page transitions.
2. **Calm Aesthetic Design**: A soft, eye-friendly cream and sage-green layout with typography tuned for reading without strain.
3. **Hybrid Database**: Django ORM structure combined with `JSONField` columns on `Appointment` and `UserProfile` models to achieve document-like NoSQL structure flexibility.
4. **Insights Hub**: Tab-based clinical resources containing Precautions, Announcements/Facilities, Physician blogs, and Disease Conditions guides.
5. **Optimized WeasyPrint PDF Speed**: Faster PDF compilation by resolving local assets through direct path mapping instead of slow DNS request resolutions.
