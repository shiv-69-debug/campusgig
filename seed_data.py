from models import db, Student, Client, Project, Proposal

def populate_seed_data():
    """Populates initial clients, students, and sample gigs in rupees."""
    try:
        if Client.query.first():
            return

        c1 = Client(name='Sarah Chen', email='sarah@lumina.io', organization='Lumina Studio')
        c1.set_password('password123')
        c2 = Client(name='Alex Rodriguez', email='alex@fintechpulse.com', organization='Fintech Pulse Media')
        c2.set_password('password123')
        c3 = Client(name='Emily Watson', email='emily@ecotrack.org', organization='EcoTrack NGO')
        c3.set_password('password123')

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

        db.session.add_all([c1, c2, c3, s1, s2])
        db.session.flush()

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
            description='Build an automated pipeline to scrape price trends across 5 retail domains and output structured JSON daily.',
            status='open'
        )
        p3 = Project(
            client_id=c2.id,
            title='Interactive Financial Dashboard in Flask & Chart.js',
            domain='Web Development',
            budget='₹45,000',
            description='Looking for a skilled student developer to create a responsive analytics portal displaying user investment portfolios.',
            status='open'
        )

        db.session.add_all([p1, p2, p3])
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Seed data note: {e}")
