# CampusGig: build the full Flask + MySQL version with a coding agent

Use this with Claude Code (or any coding agent). Put `campusgig-frontend-design.html` in an empty project folder, open the agent there, and paste the prompt below.

## Prompt to paste

Build "CampusGig", a freelancing platform for students, as a Flask + MySQL web app (three-tier: HTML/CSS/JS frontend, Flask backend, MySQL database).

**Design:** `campusgig-frontend-design.html` is the approved UI. Reuse its fonts (Abril Fatface, DM Sans), colours (lime #D4F25C, forest #0E3B2C, orange #FF6B2C, grape #6B3FA0), the intro wordmark animation, the hero with the profile card in front of the headline, the domain marquee, and the card styles. Split it into Flask templates (`base.html`, `home.html`, `student/*.html`, `client/*.html`) and `static/css/style.css`, `static/js/intro.js`. Ignore its `claude.use('db')` script: replace it with real Flask routes and forms.

**Rules:** the platform is open to ANY domain. Domain is free text on projects, with a suggestion list of common domains. Never hard-code a fixed domain list in the database.

**Auth:** dual login. Register and login pages for students and clients, passwords hashed with `werkzeug.security`, sessions with Flask `session`, a `role_required('student'|'client')` decorator, CSRF protection (Flask-WTF).

**Student module:** register/login, create and edit profile (skills, portfolio link, bio), search projects (keyword + domain filter), submit a proposal (message + price), see "My applications" with status.

**Client module:** register/login, client profile, post a project (title, domain, budget, description), view student profiles, review proposals per project, hire (accept) or decline. Accepting sets the project to `hired`.

**Workflow:** Student/Client -> Login -> Dashboard -> Project management -> Database.

**Database (MySQL, use SQLAlchemy or mysql-connector with parameterised queries):**

```sql
CREATE TABLE students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  skills TEXT, portfolio_url VARCHAR(255), bio TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE clients (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  organization VARCHAR(120),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE projects (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  title VARCHAR(150) NOT NULL,
  domain VARCHAR(80) NOT NULL,
  budget VARCHAR(40), description TEXT,
  status ENUM('open','hired','closed') DEFAULT 'open',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (client_id) REFERENCES clients(id)
);
CREATE TABLE proposals (
  id INT AUTO_INCREMENT PRIMARY KEY,
  project_id INT NOT NULL, student_id INT NOT NULL,
  message TEXT, price VARCHAR(40),
  status ENUM('pending','accepted','rejected') DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (project_id, student_id),
  FOREIGN KEY (project_id) REFERENCES projects(id),
  FOREIGN KEY (student_id) REFERENCES students(id)
);
```

**Deliverables:** `app.py` (or an app factory + blueprints), `schema.sql`, `seed.sql` with a few sample projects, `requirements.txt`, `.env.example` for DB credentials, and a README with run steps (`pip install -r requirements.txt`, create the database, `flask run`). Run it and test: register both roles, post a project, apply, hire.
