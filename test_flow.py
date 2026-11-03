"""
Comprehensive end-to-end integration test for CampusGig:
- Register student and client
- Client posts a project
- Student searches and applies with a proposal
- Client reviews proposal and hires student
- Verifies project status moves to 'hired'
"""
import os
import unittest
from app import app, db
from models import Student, Client, Project, Proposal

class CampusGigIntegrationTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_full_user_and_hiring_flow(self):
        # 1. Register Client
        resp = self.client.post('/register/client', data={
            'name': 'Dr. Alan Grant',
            'email': 'alan@paleo.org',
            'organization': 'Isla Nublar Labs',
            'password': 'jurassicpassword'
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Client Dashboard', resp.data)

        # 2. Client posts a project
        resp = self.client.post('/client/post-project', data={
            'title': 'DNA Sequence Visualizer in WebGL',
            'domain': 'Bioinformatics & WebGL',
            'budget': '₹65,000',
            'description': 'We need an interactive 3D double helix renderer in Three.js and Flask backend.'
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'DNA Sequence Visualizer in WebGL', resp.data)

        with app.app_context():
            project = Project.query.filter_by(title='DNA Sequence Visualizer in WebGL').first()
            self.assertIsNotNone(project)
            project_id = project.id
            self.assertEqual(project.status, 'open')

        # 3. Log out client
        self.client.get('/logout', follow_redirects=True)

        # 4. Register Student
        resp = self.client.post('/register/student', data={
            'name': 'Ellie Sattler',
            'email': 'ellie@botany.edu',
            'password': 'studentpassword',
            'skills': 'WebGL, Three.js, Python, Biology',
            'portfolio_url': 'https://ellie-dev.io',
            'bio': 'Undergrad bio-engineer crafting scientific web tools.'
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Explore Open Projects', resp.data)

        # 5. Student submits proposal
        resp = self.client.post(f'/projects/{project_id}', data={
            'price': '₹60,000',
            'message': 'I have built multiple WebGL visualizations for molecular biology labs. Excited to help!'
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'My Applications', resp.data)

        with app.app_context():
            proposal = Proposal.query.filter_by(project_id=project_id).first()
            self.assertIsNotNone(proposal)
            self.assertEqual(proposal.status, 'pending')
            proposal_id = proposal.id

        # 6. Log out student and log in client
        self.client.get('/logout', follow_redirects=True)
        resp = self.client.post('/login', data={
            'email': 'alan@paleo.org',
            'password': 'jurassicpassword',
            'role': 'client'
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Client Dashboard', resp.data)

        # 7. Client reviews proposals
        resp = self.client.get(f'/client/projects/{project_id}/proposals')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Ellie Sattler', resp.data)
        self.assertIn('₹60,000'.encode('utf-8'), resp.data)

        # 8. Client hires student
        resp = self.client.post(f'/client/proposals/{proposal_id}/hire', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

        # 9. Verify project and proposal statuses
        with app.app_context():
            updated_project = Project.query.get(project_id)
            updated_proposal = Proposal.query.get(proposal_id)
            self.assertEqual(updated_project.status, 'hired')
            self.assertEqual(updated_proposal.status, 'accepted')

        print("\n--> Full workflow integration test PASSED successfully!")

if __name__ == '__main__':
    unittest.main()
