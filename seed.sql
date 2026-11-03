-- Sample Seed Data for CampusGig
USE campusgig;

-- Clean existing data
DELETE FROM proposals;
DELETE FROM projects;
DELETE FROM students;
DELETE FROM clients;

-- Default password is 'password123' for all seeded users
-- Werkzeug pbkdf2:sha256 hash
-- Generated via generate_password_hash('password123')
INSERT INTO clients (id, name, email, password_hash, organization) VALUES
(1, 'Sarah Chen', 'sarah@lumina.io', 'scrypt:32768:8:1$uH3dZ8x4B12uI3k9$a89f92e34bd7a58a9e70191bce9853965b75ba4927f8841a2e7960fc5d4ca8c7fb97b481de3f4f1ff81c7e2b6aa60ba52bf33eaad85a5a6cf4ecfa58d1dae75c', 'Lumina Studio'),
(2, 'Alex Rodriguez', 'alex@fintechpulse.com', 'scrypt:32768:8:1$uH3dZ8x4B12uI3k9$a89f92e34bd7a58a9e70191bce9853965b75ba4927f8841a2e7960fc5d4ca8c7fb97b481de3f4f1ff81c7e2b6aa60ba52bf33eaad85a5a6cf4ecfa58d1dae75c', 'Fintech Pulse Media'),
(3, 'Emily Watson', 'emily@ecotrack.org', 'scrypt:32768:8:1$uH3dZ8x4B12uI3k9$a89f92e34bd7a58a9e70191bce9853965b75ba4927f8841a2e7960fc5d4ca8c7fb97b481de3f4f1ff81c7e2b6aa60ba52bf33eaad85a5a6cf4ecfa58d1dae75c', 'EcoTrack NGO');

INSERT INTO students (id, name, email, password_hash, skills, portfolio_url, bio) VALUES
(1, 'Rohan Verma', 'rohan@campus.edu', 'scrypt:32768:8:1$uH3dZ8x4B12uI3k9$a89f92e34bd7a58a9e70191bce9853965b75ba4927f8841a2e7960fc5d4ca8c7fb97b481de3f4f1ff81c7e2b6aa60ba52bf33eaad85a5a6cf4ecfa58d1dae75c', 'Python, Flask, React, SQL, Tailwind', 'https://rohanv.dev', 'Computer Science senior passionate about full-stack web development and responsive UI designs.'),
(2, 'Ananya Patel', 'ananya@design.edu', 'scrypt:32768:8:1$uH3dZ8x4B12uI3k9$a89f92e34bd7a58a9e70191bce9853965b75ba4927f8841a2e7960fc5d4ca8c7fb97b481de3f4f1ff81c7e2b6aa60ba52bf33eaad85a5a6cf4ecfa58d1dae75c', 'Figma, UI/UX, Brand Identity, Illustrator', 'https://dribbble.com/ananya-design', 'Design student focused on delightful micro-interactions, clean typography, and mobile-first product experiences.'),
(3, 'Marcus Lee', 'marcus@mit.edu', 'scrypt:32768:8:1$uH3dZ8x4B12uI3k9$a89f92e34bd7a58a9e70191bce9853965b75ba4927f8841a2e7960fc5d4ca8c7fb97b481de3f4f1ff81c7e2b6aa60ba52bf33eaad85a5a6cf4ecfa58d1dae75c', 'Technical Writing, SEO, Content Strategy, Copywriting', 'https://marcuswrites.medium.com', 'Journalism & Tech student crafting punchy product documentation and landing page copy.');

INSERT INTO projects (id, client_id, title, domain, budget, description, status) VALUES
(1, 1, 'Brand Identity & Design System for Campus Social App', 'UI/UX Design', '₹35,000', 'We need an energetic, student-centric design system with logo guidelines, color palette, and Figma components for our upcoming launch.', 'open'),
(2, 1, 'Python Web Scraper & Price Tracking Bot', 'Data Science', '₹25,000', 'Build an automated pipeline to scrape price trends across 5 retail domains and output structured JSON into a MySQL database daily.', 'open'),
(3, 2, 'Interactive Financial Dashboard in Flask & Chart.js', 'Web Development', '₹45,000', 'Looking for a skilled student developer to create a responsive analytics portal displaying user investment portfolios with dark/light mode.', 'open'),
(4, 3, 'SEO Content Series for Climate Awareness Newsletter', 'Content Writing', '₹18,000', 'Need four 1,200-word deep dive articles on campus sustainability initiatives and renewable energy incentives.', 'open'),
(5, 2, 'Mobile-First Pitch Deck & Presentation Templates', 'Graphic Design', '₹15,000', 'Create a 15-slide master deck template in Figma and Canva with custom infographics tailored for prospective angel investors.', 'hired');

INSERT INTO proposals (id, project_id, student_id, message, price, status) VALUES
(1, 3, 1, 'Hi Alex! I have extensive experience building dashboards with Flask, SQLAlchemy, and Chart.js. I can deliver a clean, tested implementation within 4 days.', '₹40,000', 'pending'),
(2, 1, 2, 'Hey Sarah! Loved your product concept. I specialize in campus-oriented visual identities and have prepared a moodboard already. Check my portfolio for previous work.', '₹35,000', 'pending'),
(3, 5, 2, 'Excited to help craft your pitch deck. I have worked with multiple student startups in their funding rounds.', '₹15,000', 'accepted');
