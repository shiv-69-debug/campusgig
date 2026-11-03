from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

# Suggestion list of common domains for user convenience (Platform accepts ANY domain as free text)
COMMON_DOMAINS = [
    "Web Development",
    "Mobile Apps",
    "UI/UX Design",
    "Graphic Design",
    "Data Science & AI",
    "Machine Learning",
    "Content Writing",
    "Copywriting",
    "Digital Marketing",
    "Video Editing & Animation",
    "Audio & Music Production",
    "Technical Writing",
    "Cybersecurity",
    "Cloud & DevOps",
    "Product Management",
    "Translation & Transcription",
    "Research & Tutoring"
]

class StudentRegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    skills = StringField('Skills (comma-separated)', validators=[Optional(), Length(max=255)])
    portfolio_url = StringField('Portfolio or GitHub URL', validators=[Optional(), Length(max=255)])
    bio = TextAreaField('Short Bio / About You', validators=[Optional()])
    submit = SubmitField('Create Student Account')

class ClientRegisterForm(FlaskForm):
    name = StringField('Full Name or Contact Person', validators=[DataRequired(), Length(max=100)])
    email = StringField('Work Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    organization = StringField('Organization / Company / Club', validators=[Optional(), Length(max=120)])
    submit = SubmitField('Create Client Account')

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Login As', choices=[('student', 'Student Freelancer'), ('client', 'Client / Employer')], default='student')
    submit = SubmitField('Sign In')

class StudentProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    skills = StringField('Skills (comma-separated, e.g. Python, React, UI Design)', validators=[Optional()])
    portfolio_url = StringField('Portfolio / GitHub Link', validators=[Optional(), Length(max=255)])
    bio = TextAreaField('About You / Bio', validators=[Optional()])
    submit = SubmitField('Save Profile')

class ClientProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    organization = StringField('Organization / Company Name', validators=[Optional(), Length(max=120)])
    submit = SubmitField('Save Profile')

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(max=150)])
    domain = StringField('Domain / Field (e.g. Web Dev, Design, AI, Content)', validators=[DataRequired(), Length(max=80)])
    budget = StringField('Budget or Compensation (e.g. ₹5,000, ₹500/hr, ₹12,000 fixed)', validators=[Optional(), Length(max=40)])
    description = TextAreaField('Detailed Project Description & Deliverables', validators=[DataRequired()])
    submit = SubmitField('Post Project')

class ProposalForm(FlaskForm):
    price = StringField('Your Proposed Price / Rate (e.g. ₹4,500, ₹400/hr)', validators=[DataRequired(), Length(max=40)])
    message = TextAreaField('Proposal Pitch & Relevant Experience', validators=[DataRequired()])
    submit = SubmitField('Submit Proposal')
