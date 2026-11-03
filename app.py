import os
from functools import wraps
from dotenv import load_dotenv
from flask import (
    Flask, render_template, redirect, url_for, flash, request, session, abort
)
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import or_

# Load environment configuration
load_dotenv()

from models import db, Student, Client, Project, Proposal
from forms import (
    COMMON_DOMAINS,
    StudentRegisterForm, ClientRegisterForm, LoginForm,
    StudentProfileForm, ClientProfileForm, ProjectForm, ProposalForm
)

def create_app():
    app = Flask(__name__)

    # Secret Key for CSRF & Sessions
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'campusgig-default-dev-secret-key-39182')

    # Database Configuration (MySQL / fallback support)
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        db_user = os.getenv('DB_USER', 'root')
        db_pass = os.getenv('DB_PASSWORD', '')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '3306')
        db_name = os.getenv('DB_NAME', 'campusgig')
        database_url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    csrf = CSRFProtect(app)
    db.init_app(app)

    return app, csrf

app, csrf = create_app()

# ==========================================
# Authentication & Role Decorators
# ==========================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or 'role' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session or 'role' not in session:
                flash('Please log in to continue.', 'warning')
                return redirect(url_for('login', next=request.url))
            if session.get('role') != role_name:
                flash(f'Unauthorized: This action requires {role_name} access.', 'danger')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ==========================================
# General & Auth Routes
# ==========================================
@app.route('/')
def home():
    # Show fresh open projects on landing page
    open_projects = Project.query.filter_by(status='open').order_by(Project.created_at.desc()).limit(6).all()
    return render_template('home.html', projects=open_projects)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session and 'role' in session:
        if session['role'] == 'student':
            return redirect(url_for('student_dashboard'))
        return redirect(url_for('client_dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data
        role = form.role.data

        if role == 'student':
            user = Student.query.filter_by(email=email).first()
        else:
            user = Client.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session.clear()
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['role'] = role
            session.permanent = True

            flash(f'Welcome back, {user.name}!', 'success')
            next_page = request.args.get('next')
            if next_page and not next_page.startswith('//'):
                return redirect(next_page)

            if role == 'student':
                return redirect(url_for('student_dashboard'))
            return redirect(url_for('client_dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html', form=form)

@app.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if 'user_id' in session:
        return redirect(url_for('home'))

    form = StudentRegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if Student.query.filter_by(email=email).first() or Client.query.filter_by(email=email).first():
            flash('An account with this email already exists.', 'danger')
            return render_template('register_student.html', form=form)

        new_student = Student(
            name=form.name.data.strip(),
            email=email,
            skills=form.skills.data.strip() if form.skills.data else None,
            portfolio_url=form.portfolio_url.data.strip() if form.portfolio_url.data else None,
            bio=form.bio.data.strip() if form.bio.data else None
        )
        new_student.set_password(form.password.data)

        db.session.add(new_student)
        db.session.commit()

        # Automatically log in the registered student
        session.clear()
        session['user_id'] = new_student.id
        session['user_name'] = new_student.name
        session['role'] = 'student'

        flash('Your student account was created successfully! Welcome to CampusGig.', 'success')
        return redirect(url_for('student_dashboard'))

    return render_template('register_student.html', form=form)

@app.route('/register/client', methods=['GET', 'POST'])
def register_client():
    if 'user_id' in session:
        return redirect(url_for('home'))

    form = ClientRegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if Student.query.filter_by(email=email).first() or Client.query.filter_by(email=email).first():
            flash('An account with this email already exists.', 'danger')
            return render_template('register_client.html', form=form)

        new_client = Client(
            name=form.name.data.strip(),
            email=email,
            organization=form.organization.data.strip() if form.organization.data else None
        )
        new_client.set_password(form.password.data)

        db.session.add(new_client)
        db.session.commit()

        # Automatically log in the registered client
        session.clear()
        session['user_id'] = new_client.id
        session['user_name'] = new_client.name
        session['role'] = 'client'

        flash('Client account created successfully! Start posting gigs.', 'success')
        return redirect(url_for('client_dashboard'))

    return render_template('register_client.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('home'))


# ==========================================
# Student Module
# ==========================================
@app.route('/student/dashboard')
def student_dashboard():
    query = request.args.get('q', '').strip()
    selected_domain = request.args.get('domain', '').strip()

    project_query = Project.query.filter_by(status='open')

    if query:
        project_query = project_query.filter(
            or_(
                Project.title.ilike(f'%{query}%'),
                Project.description.ilike(f'%{query}%')
            )
        )

    if selected_domain:
        project_query = project_query.filter(Project.domain.ilike(f'%{selected_domain}%'))

    projects = project_query.order_by(Project.created_at.desc()).all()

    # Track which projects current student has already applied for
    applied_project_ids = set()
    if session.get('role') == 'student':
        student_id = session.get('user_id')
        proposals = Proposal.query.filter_by(student_id=student_id).all()
        applied_project_ids = {p.project_id for p in proposals}

    return render_template(
        'student/dashboard.html',
        projects=projects,
        applied_project_ids=applied_project_ids,
        query=query,
        selected_domain=selected_domain,
        domains_list=COMMON_DOMAINS
    )

@app.route('/projects/<int:project_id>', methods=['GET', 'POST'])
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProposalForm()
    existing_proposal = None

    if session.get('role') == 'student':
        student_id = session['user_id']
        existing_proposal = Proposal.query.filter_by(project_id=project.id, student_id=student_id).first()

    if form.validate_on_submit():
        if session.get('role') != 'student':
            flash('Only registered students can submit proposals.', 'warning')
            return redirect(url_for('login'))

        if project.status != 'open':
            flash('This project is no longer accepting new proposals.', 'warning')
            return redirect(url_for('project_detail', project_id=project.id))

        if existing_proposal:
            flash('You have already applied for this project.', 'info')
            return redirect(url_for('project_detail', project_id=project.id))

        proposal = Proposal(
            project_id=project.id,
            student_id=session['user_id'],
            price=form.price.data.strip(),
            message=form.message.data.strip(),
            status='pending'
        )
        db.session.add(proposal)
        db.session.commit()

        flash('Your proposal was submitted successfully!', 'success')
        return redirect(url_for('student_applications'))

    return render_template(
        'student/project_detail.html',
        project=project,
        form=form,
        existing_proposal=existing_proposal
    )

@app.route('/student/applications')
@role_required('student')
def student_applications():
    student_id = session['user_id']
    proposals = Proposal.query.filter_by(student_id=student_id).order_by(Proposal.created_at.desc()).all()
    return render_template('student/applications.html', proposals=proposals)

@app.route('/student/profile', methods=['GET', 'POST'])
@role_required('student')
def student_profile():
    student = Student.query.get_or_404(session['user_id'])
    form = StudentProfileForm(obj=student)

    if form.validate_on_submit():
        student.name = form.name.data.strip()
        student.skills = form.skills.data.strip() if form.skills.data else None
        student.portfolio_url = form.portfolio_url.data.strip() if form.portfolio_url.data else None
        student.bio = form.bio.data.strip() if form.bio.data else None
        db.session.commit()

        session['user_name'] = student.name
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('student_profile'))

    return render_template('student/profile.html', form=form, student=student)


# ==========================================
# Client Module
# ==========================================
@app.route('/client/dashboard')
@role_required('client')
def client_dashboard():
    client_id = session['user_id']
    projects = Project.query.filter_by(client_id=client_id).order_by(Project.created_at.desc()).all()
    return render_template('client/dashboard.html', projects=projects)

@app.route('/client/post-project', methods=['GET', 'POST'])
@role_required('client')
def client_post_project():
    form = ProjectForm()
    if form.validate_on_submit():
        # Any domain is allowed as free text
        new_project = Project(
            client_id=session['user_id'],
            title=form.title.data.strip(),
            domain=form.domain.data.strip(),
            budget=form.budget.data.strip() if form.budget.data else None,
            description=form.description.data.strip(),
            status='open'
        )
        db.session.add(new_project)
        db.session.commit()

        flash('Project posted successfully! Students can now submit proposals.', 'success')
        return redirect(url_for('client_dashboard'))

    return render_template('client/post_project.html', form=form, domains_list=COMMON_DOMAINS)

@app.route('/client/projects/<int:project_id>/proposals')
@role_required('client')
def client_project_proposals(project_id):
    project = Project.query.filter_by(id=project_id, client_id=session['user_id']).first_or_404()
    proposals = Proposal.query.filter_by(project_id=project.id).order_by(Proposal.created_at.desc()).all()
    return render_template('client/proposals.html', project=project, proposals=proposals)

@app.route('/client/proposals/<int:proposal_id>/<string:action_type>', methods=['POST'])
@role_required('client')
def client_action_proposal(proposal_id, action_type):
    proposal = Proposal.query.get_or_404(proposal_id)
    project = proposal.project

    # Ensure current client owns this project
    if project.client_id != session['user_id']:
        abort(403)

    if action_type == 'hire':
        proposal.status = 'accepted'
        project.status = 'hired'
        flash(f'Congratulations! You have hired {proposal.student.name} for "{project.title}".', 'success')
    elif action_type == 'decline':
        proposal.status = 'rejected'
        flash(f'Proposal from {proposal.student.name} was declined.', 'info')
    else:
        abort(400)

    db.session.commit()
    return redirect(url_for('client_project_proposals', project_id=project.id))

@app.route('/client/students')
@role_required('client')
def client_students():
    students = Student.query.order_by(Student.created_at.desc()).all()
    return render_template('client/students.html', students=students)

@app.route('/client/profile', methods=['GET', 'POST'])
@role_required('client')
def client_profile():
    client = Client.query.get_or_404(session['user_id'])
    form = ClientProfileForm(obj=client)

    if form.validate_on_submit():
        client.name = form.name.data.strip()
        client.organization = form.organization.data.strip() if form.organization.data else None
        db.session.commit()

        session['user_name'] = client.name
        flash('Client profile updated.', 'success')
        return redirect(url_for('client_profile'))

    return render_template('client/profile.html', form=form, client=client)


# ==========================================
# CLI Helper: Initialize & Seed Database
# ==========================================
@app.cli.command('init-db')
def init_db_command():
    """Create all database tables."""
    db.create_all()
    print("Database tables created successfully!")

@app.cli.command('seed-db')
def seed_db_command():
    """Populate database with sample students, clients, and projects."""
    db.create_all()

    # Create Clients
    c1 = Client(name='Sarah Chen', email='sarah@lumina.io', organization='Lumina Studio')
    c1.set_password('password123')
    c2 = Client(name='Alex Rodriguez', email='alex@fintechpulse.com', organization='Fintech Pulse Media')
    c2.set_password('password123')
    c3 = Client(name='Emily Watson', email='emily@ecotrack.org', organization='EcoTrack NGO')
    c3.set_password('password123')

    # Create Students
    s1 = Student(
        name='Rohan Verma',
        email='rohan@campus.edu',
        skills='Python, Flask, React, SQL, Tailwind',
        portfolio_url='https://rohanv.dev',
        bio='Computer Science senior passionate about full-stack web development and responsive UI designs.'
    )
    s1.set_password('password123')

    s2 = Student(
        name='Ananya Patel',
        email='ananya@design.edu',
        skills='Figma, UI/UX, Brand Identity, Illustrator',
        portfolio_url='https://dribbble.com/ananya-design',
        bio='Design student focused on delightful micro-interactions, clean typography, and mobile-first product experiences.'
    )
    s2.set_password('password123')

    s3 = Student(
        name='Marcus Lee',
        email='marcus@mit.edu',
        skills='Technical Writing, SEO, Content Strategy, Copywriting',
        portfolio_url='https://marcuswrites.medium.com',
        bio='Journalism & Tech student crafting punchy product documentation and landing page copy.'
    )
    s3.set_password('password123')

    db.session.add_all([c1, c2, c3, s1, s2, s3])
    db.session.flush()

    # Create Projects
    p1 = Project(
        client_id=c1.id,
        title='Brand Identity & Design System for Campus Social App',
        domain='UI/UX Design',
        budget='₹35,000',
        description='We need an energetic, student-centric design system with logo guidelines, color palette, and Figma components for our upcoming launch.',
        status='open'
    )
    p2 = Project(
        client_id=c1.id,
        title='Python Web Scraper & Price Tracking Bot',
        domain='Data Science',
        budget='₹25,000',
        description='Build an automated pipeline to scrape price trends across 5 retail domains and output structured JSON into a MySQL database daily.',
        status='open'
    )
    p3 = Project(
        client_id=c2.id,
        title='Interactive Financial Dashboard in Flask & Chart.js',
        domain='Web Development',
        budget='₹45,000',
        description='Looking for a skilled student developer to create a responsive analytics portal displaying user investment portfolios with dark/light mode.',
        status='open'
    )
    p4 = Project(
        client_id=c3.id,
        title='SEO Content Series for Climate Awareness Newsletter',
        domain='Content Writing',
        budget='₹18,000',
        description='Need four 1,200-word deep dive articles on campus sustainability initiatives and renewable energy incentives.',
        status='open'
    )
    p5 = Project(
        client_id=c2.id,
        title='Mobile-First Pitch Deck & Presentation Templates',
        domain='Graphic Design',
        budget='₹15,000',
        description='Create a 15-slide master deck template in Figma and Canva with custom infographics tailored for prospective angel investors.',
        status='hired'
    )

    db.session.add_all([p1, p2, p3, p4, p5])
    db.session.flush()

    # Create Proposals
    pr1 = Proposal(
        project_id=p3.id,
        student_id=s1.id,
        message='Hi Alex! I have extensive experience building dashboards with Flask, SQLAlchemy, and Chart.js. I can deliver a clean, tested implementation within 4 days.',
        price='₹40,000',
        status='pending'
    )
    pr2 = Proposal(
        project_id=p1.id,
        student_id=s2.id,
        message='Hey Sarah! Loved your product concept. I specialize in campus-oriented visual identities and have prepared a moodboard already. Check my portfolio for previous work.',
        price='₹35,000',
        status='pending'
    )
    pr3 = Proposal(
        project_id=p5.id,
        student_id=s2.id,
        message='Excited to help craft your pitch deck. I have worked with multiple student startups in their funding rounds.',
        price='₹15,000',
        status='accepted'
    )

    db.session.add_all([pr1, pr2, pr3])
    db.session.commit()
    print("Database seeded with sample students, clients, projects, and proposals! (Default password: password123)")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
