# CampusGig - Student Freelancing Platform

A three-tier web application built with **Flask**, **MySQL**, and modern semantic **HTML/CSS/JS** inspired by the approved CampusGig design aesthetic (Abril Fatface & DM Sans typography, lime `#D4F25C`, forest `#0E3B2C`, orange `#FF6B2C`, and grape `#6B3FA0` palette, marquee tickers, and responsive cards).

The platform is designed to be **open to ANY domain** (technical, design, content, marketing, research, etc.). Domains are free text with suggested common domains.

---

## Architecture & Tech Stack

- **Frontend:** Jinja2 templates, semantic HTML5, CSS3 design system (`static/css/style.css`), intro animation script (`static/js/intro.js`).
- **Backend:** Python Flask 3.x, Flask-WTF (CSRF protection & form validation), Werkzeug (secure password hashing).
- **Database:** MySQL 8.x / MariaDB (managed via Flask-SQLAlchemy with parameterized queries; SQLite supported for zero-setup local dev).

---

## Project Structure

```
campusgig/
├── app.py                     # Main application factory, routing & business logic
├── models.py                  # SQLAlchemy models (Student, Client, Project, Proposal)
├── forms.py                   # Flask-WTF forms & common domain suggestions
├── requirements.txt           # Python dependencies
├── schema.sql                 # MySQL schema definition
├── seed.sql                   # Sample SQL seed data
├── .env.example               # Environment variables template
├── .env                       # Local environment configuration
├── static/
│   ├── css/
│   │   └── style.css          # Design system, colours, fonts & responsive components
│   └── js/
│       └── intro.js           # Intro wordmark animation
├── templates/
│   ├── base.html              # Base layout with navbar & footer
│   ├── home.html              # Landing page with hero & domain marquee
│   ├── login.html             # Dual login page (student & client)
│   ├── register_student.html  # Student registration
│   ├── register_client.html   # Client registration
│   ├── student/
│   │   ├── dashboard.html     # Browse & filter projects by domain/keyword
│   │   ├── project_detail.html# Project view & submit proposal form
│   │   ├── applications.html  # "My applications" status tracker
│   │   └── profile.html       # Edit skills, portfolio link, & bio
│   └── client/
│       ├── dashboard.html     # Posted gigs manager & applicant counters
│       ├── post_project.html  # Post a project form (free-text domain)
│       ├── proposals.html     # Review bids, hire (accept), or decline
│       ├── students.html      # Campus talent directory
│       └── profile.html       # Client profile editor
└── test_flow.py               # End-to-end integration test script
```

---

## Quickstart Instructions

### 1. Prerequisites
- Python 3.9+
- MySQL Server 8.0+ (or MariaDB)

### 2. Installation

1. **Clone/Navigate to the project root:**
   ```bash
   cd campusgig
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 3. Database Setup

#### Option A: MySQL Server (Standard Production/Local)
1. Ensure your MySQL server is running.
2. Create the database and tables using `schema.sql`:
   ```bash
   mysql -u root -p < schema.sql
   ```
3. (Optional) Load sample data:
   ```bash
   mysql -u root -p campusgig < seed.sql
   ```
4. Configure your `.env` file with your credentials:
   ```ini
   DATABASE_URL=mysql+pymysql://<user>:<password>@localhost:3306/campusgig
   SECRET_KEY=your-custom-secret-key
   ```

#### Option B: Zero-Config SQLite (Immediate Testing)
The repository includes a ready-to-use SQLite connection fallback in `.env`:
```ini
DATABASE_URL=sqlite:///campusgig.db
```
Initialize and seed the database with Flask CLI commands:
```bash
flask init-db
flask seed-db
```

---

## Running the Application

Start the Flask development server:
```bash
flask run
# or
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Seed Accounts (for testing)

All seed accounts use password: `password123`

| Role | Email | Name / Org |
| :--- | :--- | :--- |
| **Student** | `rohan@campus.edu` | Rohan Verma (Full-Stack Dev) |
| **Student** | `ananya@design.edu` | Ananya Patel (UI/UX Designer) |
| **Student** | `marcus@mit.edu` | Marcus Lee (Technical Writer) |
| **Client** | `sarah@lumina.io` | Sarah Chen (Lumina Studio) |
| **Client** | `alex@fintechpulse.com`| Alex Rodriguez (Fintech Pulse) |

---

## Workflow Testing Walkthrough

1. **Register as Student:** Go to `/register/student`, input your details, skills, and portfolio link.
2. **Explore Projects:** Filter by keyword or domain list on `/student/dashboard`.
3. **Submit Proposal:** Click on any open project and submit your proposed price and pitch.
4. **Register / Sign In as Client:** Go to `/register/client` or log in as a client.
5. **Post a Project:** Open `/client/post-project`, enter a title, custom domain, budget, and description.
6. **Review & Hire:** Go to `/client/dashboard`, click **Review Proposals**, and click **Hire Student**.
7. **Verify:** The project status automatically transitions to `hired` and the proposal updates to `accepted`.
