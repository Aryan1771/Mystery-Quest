# MYSTERY QUEST – DETECTIVE INVESTIGATION WEB APPLICATION

> **Full-Stack Web Development Laboratory Project**  
> Built with Python, Django (MVT Architecture), SQLite, Bootstrap 5, AJAX (Fetch API), and ReportLab.

---

## 🔍 1. Project Overview

**Mystery Quest** is a full-stack detective investigation web application designed for interactive criminal case solving and forensic reasoning. Users take on the role of detectives, inspect crime scenes, collect physical and forensic clues, cross-examine suspect alibis against eyewitness depositions, consult a rule-based AI hint system, and submit formal accusations before the magistrate.

The project fulfills all requirements specified in the Full Stack Web Development Laboratory curriculum synopsis, demonstrating complex relational database modeling, role-based authorization, asynchronous AJAX communication, dynamic leaderboards, and automated server-side PDF and CSV report generation.

---

## 🏛️ 2. System Architecture & Tech Stack

- **Architecture:** Model-View-Template (MVT) pattern adhering to Django best practices.
- **Backend:** Python 3.13 / Django 6.1
- **Database:** SQLite with full relational integrity (One-to-One, One-to-Many, Many-to-Many).
- **Frontend:** HTML5, CSS3, JavaScript (ES6+ Fetch API), Bootstrap 5, Bootstrap Icons.
- **Reporting Engine:** ReportLab (Server-side PDF generation) & Python `csv` module (CSV exports).
- **AJAX Communication:** JavaScript Fetch API calling Django endpoints returning JSON responses.
- **Design Aesthetic:** Detective Noir palette (Deep navy `#070b12`, midnight slate `#131b2c`, and warm gold `#f59e0b`).

---

## 🗄️ 3. Database Models & Schema Design

| Model | Relationship | Description |
|---|---|---|
| **`UserProfile`** | `OneToOneField(User)` | Stores total score, dynamic rank title (`Rookie Sleuth` up to `Master Detective`), solved cases count, and bio. |
| **`Case`** | Root Entity | Stores title, description, background lore, difficulty (`Easy`, `Medium`, `Hard`), status, solution explanation, and pointer to `correct_suspect`. |
| **`Suspect`** | `ManyToManyField(Case)` | Stores suspect name, profile, stated alibi, investigated motive, and `is_culprit` flag. |
| **`Clue`** | `ForeignKey(Case)` | Stores title, category (`Textual`, `Physical`, `Forensic`, `Location`, `Digital`), and detailed description. |
| **`Evidence`** | `ForeignKey(Case)`, `ForeignKey(Suspect)` | Forensic records linking suspects and recovered clues to the crime scene. |
| **`WitnessStatement`** | `ForeignKey(Case)` | Eyewitness depositions with credibility ratings (`High`, `Medium`, `Questionable`). |
| **`UserCaseProgress`** | `ForeignKey(User)`, `ForeignKey(Case)` | Tracks individual detective progress, collected clues (`ManyToManyField`), hints used, score, and completion status (`In Progress`, `Solved`, `Failed`). |
| **`Accusation`** | `ForeignKey(User)`, `ForeignKey(Case)` | Logs detective accusations, selected suspect, correctness, submission timestamp, and deduction notes. |

---

## 🚀 4. Core Features & Capabilities

1. **User Authentication & Role-Based Authorization:**
   - Registration, secure session-based login, and logout.
   - Built-in Django authentication with PBKDF2 password hashing and CSRF defense.
   - Automatic `UserProfile` instantiation via `post_save` signals.
   - Clear distinction between normal detectives and administrative staff.

2. **Interactive Crime Investigation Room (`investigate.html`):**
   - Multi-panel tabbed workspace:
     1. *Crime Scene Clues:* Interactive clue inspection and cataloging with dynamic progress bar updates.
     2. *Suspect Dossiers:* Detailed profiles, alibis, and motives.
     3. *Evidence Locker:* Forensic traces connecting suspects and clues.
     4. *Witness Testimonies:* Depositions with credibility ratings.
     5. *AI Clue Assistant:* Rule-based deductive guidance.
     6. *Accusation Chamber:* Formal indictment interface with deduction rationale.

3. **Asynchronous (AJAX) Interactivity:**
   - **Real-Time Live Search:** Search cases, clues, and suspects instantly as you type using `fetch()` without full-page reloads.
   - **AJAX Clue Collection:** Inspect and catalog clues with instantaneous UI and progress bar updates.
   - **AJAX AI Hint Generation:** Retrieve hints seamlessly with real-time score adjustment tracking.

4. **Rule-Based AI Hint System:**
   - Heuristic deduction engine based on pure Python conditional logic and current docket state.
   - Progressive assistance without spoiling the solution:
     - 0 clues: Directs to initial physical inspection.
     - 1 clue: Guides towards uncovering diverse evidence categories.
     - 2+ clues: Prompts cross-examination of witness timelines against suspect alibis.
     - All clues: Encourages deductive synthesis of motives and means.
   - Automatically deducts 15 efficiency points per hint consulted.

5. **Scoring Engine & Anti-Exploit Protection:**
   - **Base Points:** Easy (100 pts), Medium (150 pts), Hard (200 pts).
   - **Clue Discovery Bonus:** +10 points for each clue collected.
   - **Hint Penalties:** -15 points per hint consulted (minimum floor: 50 pts for correct solution).
   - **Anti-Cheat:** Repeat submissions on already-solved cases are prevented from artificially inflating user score.

6. **Automated Server-Side Reporting:**
   - **ReportLab PDF Dossier:** Generates official investigation reports with case overview, clues table, suspect analysis, verdict, and official stamp.
   - **CSV Downloads:** Export case archive records (`/reports/cases/csv/`) and full leaderboard statistics (`/reports/leaderboard/csv/`).

7. **Dynamic Leaderboard:**
   - Real-time ranking sorted by `total_score` and `cases_solved`.
   - Gold, Silver, and Bronze trophy medals for top 3 investigators.
   - Highlights the logged-in detective's standing.

8. **Administrative CRUD Management:**
   - Staff-protected dashboard (`/manage/`) for full Create, Read, Update, and Delete operations over Cases, Clues, and Suspects using Django ModelForms.
   - Fully customized Django Admin (`/admin/`).

---

## 📂 5. Project Directory Structure

```
mystery_quest/
├── manage.py                          # Django management script
├── requirements.txt                   # Dependency list
├── README.md                          # Documentation & guide
├── db.sqlite3                         # SQLite database
│
├── mystery_quest_project/             # Project Configuration
│   ├── settings.py                    # Settings, apps, templates, static/media paths
│   ├── urls.py                        # Root URL router
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                          # Authentication & User Profiles App
│   ├── models.py                      # UserProfile model & post_save signal
│   ├── forms.py                       # UserRegistrationForm, UserLoginForm, ProfileForm
│   ├── views.py                       # register_view, login_view, logout_view, profile_view
│   ├── urls.py                        # /accounts/ routes
│   ├── admin.py                       # UserProfileAdmin
│   └── tests.py                       # Authentication & ranking unit tests
│
├── investigation/                     # Core Game Logic & Investigation App
│   ├── models.py                      # Case, Clue, Suspect, Evidence, WitnessStatement, UserCaseProgress, Accusation
│   ├── forms.py                       # CaseForm, ClueForm, SuspectForm, AccusationForm
│   ├── hint_engine.py                 # Rule-based AI heuristic hint generator
│   ├── reports.py                     # ReportLab PDF & CSV exports
│   ├── views.py                       # Investigation views, AJAX search, CRUD operations
│   ├── urls.py                        # Investigation & RESTful routes
│   ├── admin.py                       # Customized Django Admin with Inlines
│   ├── tests.py                       # 12 automated unit & integration tests
│   └── management/commands/
│       └── seed_data.py               # Database seeder with 5 rich fictional cases
│
├── static/
│   ├── css/
│   │   └── custom.css                 # Noir dark-navy & gold theme styling
│   └── js/
│       ├── search.js                  # Asynchronous AJAX live search
│       └── investigation.js           # Asynchronous clue collection & AI hint handler
│
└── templates/
    ├── base.html                      # Root layout, detective navbar & footer
    ├── home.html                      # Landing page & Hall of Fame preview
    ├── accounts/
    │   ├── login.html                 # Login page
    │   ├── register.html              # Registration page
    │   └── profile.html               # Detective Dossier & case history
    └── investigation/
        ├── case_list.html             # Case files archive with difficulty filters
        ├── case_detail.html           # Case dossier briefing
        ├── investigate.html           # Interactive multi-panel crime room
        ├── leaderboard.html           # Dynamic leaderboard
        ├── search.html                # Live AJAX search interface
        ├── crud_dashboard.html        # Staff management dashboard
        ├── case_form.html             # Case Create/Edit form
        ├── clue_form.html             # Clue Create/Edit form
        ├── suspect_form.html          # Suspect Create/Edit form
        └── confirm_delete.html        # Deletion confirmation
```

---

## ⚙️ 6. Installation & Execution Guide

### Step 1: Open Terminal in Project Folder
Ensure you are in the project root directory:
```bash
cd "C:\Users\Lenovo\.gemini\antigravity\scratch\mystery_quest"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Apply Database Migrations
```bash
python manage.py makemigrations accounts
python manage.py makemigrations investigation
python manage.py migrate
```

### Step 4: Seed Database with Sample Cases & Detectives
Run the custom seed command to populate 5 complete fictional cases, clues, suspects, evidence, and sample detectives:
```bash
python manage.py seed_data
```

### Step 5: Run Automated Tests
Verify that all 12 unit and integration tests pass cleanly:
```bash
python manage.py test
```

### Step 6: Start the Development Server
```bash
python manage.py runserver
```
Visit your browser at: **`http://127.0.0.1:8000/`**

---

## 🔑 7. Default Credentials

| Role | Username | Password | Access Level |
|---|---|---|---|
| **Administrator / Staff** | *Create with Django's `createsuperuser` command* | *Set privately* | Full access + Django Admin + Management CRUD (`/manage/`) |
| **Detective** | *Register in UI* | *Chosen privately by the user* | Standard detective permissions |

Do not publish real or demo passwords in the repository. Django stores password hashes, not recoverable plaintext passwords.

---

## 🎓 8. College Viva / Practical Examination Talking Points

When demonstrating this project to internal/external examiners:

1. **MVT Architecture:** Explain how the Request-Response cycle flows from `urls.py` through class/function-based views in `views.py`, interacting with ORM models in `models.py`, and rendering Bootstrap 5 templates inheriting from `base.html`.
2. **Relational Database Design:** Highlight the `OneToOneField` between `User` and `UserProfile`, `ManyToManyField` between `Case` and `Suspect`, and `ForeignKey` relationships on `Clue`, `Evidence`, and `WitnessStatement`.
3. **Asynchronous Communication (AJAX):** Demonstrate that typing in the Live Search bar triggers JavaScript's `fetch()` API to `/api/search/` with debouncing, dynamically rendering results as JSON without a page refresh.
4. **Rule-Based AI Hint System:** Clarify that instead of costly external AI APIs, the application employs an intelligent rule-based expert heuristic in `hint_engine.py` that evaluates the state of collected clues and penalizes points fairly.
5. **PDF & CSV Generation:** Show server-side binary generation using `reportlab.platypus` (`SimpleDocTemplate`, `Table`, `Paragraph`) for confidential PDF dossiers, and Python's `csv` module with `HttpResponse(content_type='text/csv')` for instant downloads.
6. **Anti-Exploit Security:** Explain how the accusation engine prevents repeat submissions from artificially gaming the leaderboard score.
