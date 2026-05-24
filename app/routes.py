from flask import render_template, request, redirect, url_for, flash, current_app as app
from app import db
from app.models import User, Subject, Topic, StudyPlan, ProgressLog 
from app.scheduler import calculate_study_plan
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import PyPDF2
from google import genai  # Use the new library

# Load the variables from .env
load_dotenv() 

# 1. Initialize the Secure Gemini Client
# This pulls your key from the .env file instead of hardcoding it
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

# 1. Dashboard - View all Subjects and Topics
@app.route('/dashboard')
@login_required
def dashboard():
    subjects = Subject.query.filter_by(user_id=current_user.id).all()
    plan_entries = StudyPlan.query.filter_by(user_id=current_user.id).order_by(StudyPlan.scheduled_date).all()
    return render_template('dashboard.html', subjects=subjects, plan_entries=plan_entries)

# 2. Add a Subject (Personalized to current_user)
@app.route('/add_subject', methods=['POST'])
@login_required
def add_subject():
    name = request.form.get('subject_name')
    if name:
        # Fixed: Changed from hardcoded user_id=1 to current_user.id
        new_subject = Subject(name=name, user_id=current_user.id) 
        db.session.add(new_subject)
        db.session.commit()
        flash(f'Subject "{name}" added!')
    return redirect(url_for('dashboard'))

# 3. Add a Topic (Personalized to current_user)
@app.route('/add_topic/<int:subject_id>', methods=['POST'])
@login_required
def add_topic(subject_id):
    title = request.form.get('topic_title')
    prio_str = request.form.get('priority')
    time_str = request.form.get('estimated_time')

    if not title or not prio_str or not time_str:
        flash("Error: Missing topic details. Please fill all fields.")
        return redirect(url_for('dashboard'))

    try:
        new_topic = Topic(
            title=title,
            priority=int(prio_str),
            estimated_time=int(time_str),
            subject_id=subject_id,
            user_id=current_user.id # Fixed: Using current_user.id
        )
        db.session.add(new_topic)
        db.session.commit()
        flash(f"Topic '{title}' added!")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}")
    return redirect(url_for('dashboard'))

# 4. Generate plan
@app.route('/generate_plan', methods=['POST'])
@login_required
def generate_plan():
    exam_date_str = request.form.get('exam_date')
    if not exam_date_str:
        flash("Please select an exam date!")
        return redirect(url_for('dashboard'))

    try:
        exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
        result = calculate_study_plan(user_id=current_user.id, exam_date=exam_date)
        if result['status'] == 'success':
            flash(result['message'])
        else:
            flash(f"Error: {result['message']}")
    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}")
    return redirect(url_for('dashboard'))

# 5. Delete subject
@app.route('/delete_subject/<int:subject_id>', methods=['POST'])
@login_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    for topic in subject.topics:
        StudyPlan.query.filter_by(topic_id=topic.id).delete()
    Topic.query.filter_by(subject_id=subject_id).delete()
    db.session.delete(subject)
    db.session.commit()
    flash('Subject, Topics, and Schedule cleared!', 'info')
    return redirect(url_for('dashboard'))

# 6. Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash("Username or email already exists!")
            return redirect(url_for('signup'))
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created! Please login.")
        return redirect(url_for('login'))
    return render_template('signup.html')

# 7. Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Syllabus Scanner Setup
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload_syllabus', methods=['POST'])
@login_required
def upload_syllabus():
    subject_id = request.form.get('subject_id')
    file = request.files.get('syllabus_file')
    if file and subject_id:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # Use new client for Syllabus Scanner too!
        prompt = "Extract study topics from this syllabus. Return ONLY topic names as a comma-separated list."
        # Note: You may need to handle file uploads differently in the new SDK if passing raw images
        # For now, keeping the content logic focused on text summary stability
        flash('AI is processing your syllabus...', 'info')
        # Placeholder for AI logic using the new client for vision if needed
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))

@app.route('/complete_task/<int:topic_id>', methods=['POST'])
@login_required
def complete_task(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    if topic.user_id != current_user.id:
        return {"error": "Unauthorized"}, 403

    topic.is_completed = True
    db.session.commit()

    subject = Subject.query.get(topic.subject_id)
    total_subject_topics = Topic.query.filter_by(subject_id=subject.id).count()
    completed_subject_topics = Topic.query.filter_by(subject_id=subject.id, is_completed=True).count()
    progress = (completed_subject_topics / total_subject_topics * 100) if total_subject_topics > 0 else 0
    
    return {
        "success": True, 
        "total_progress": round(progress, 2),
        "message": "Quest Completed! +10 XP",
        "subject_id": subject.id
    }

# AI Summary Core Functions
def get_gemini_response(prompt):
    """Updated to use the new google.genai library"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        if response and response.text:
            return response.text.replace('**', '<b>').replace('\n', '<br>')
        return "AI returned an empty response."
    except Exception as e:
        print(f"!!! GENAI API ERROR: {e}") 
        return f"Sorry, AI is acting up. Error: {str(e)[:50]}"

@app.route('/notes')
@login_required
def notes_page():
    return render_template('notes.html', notes=None)

@app.route('/summarize_pdf', methods=['POST'])
@login_required
def summarize_pdf():
    if 'pdf_file' not in request.files:
        flash("No file part", "error")
        return redirect(url_for('notes_page'))
    
    file = request.files['pdf_file']
    if file.filename == '':
        flash("No selected file", "error")
        return redirect(url_for('notes_page'))

    try:
        reader = PyPDF2.PdfReader(file)
        extracted_text = ""
        for i in range(min(10, len(reader.pages))):
            page_text = reader.pages[i].extract_text()
            if page_text:
                extracted_text += " ".join(page_text.split()) + " "

        if not extracted_text.strip():
            flash("Could not read any text from this PDF.", "warning")
            return redirect(url_for('notes_page'))

        prompt = f"Simplify the following technical text into easy-to-understand student notes with bold headings: {extracted_text[:12000]}"
        ai_notes = get_gemini_response(prompt) 
        return render_template('notes.html', notes=ai_notes)

    except Exception as e:
        print(f"System Error: {e}")
        flash("Something went wrong while processing the PDF.", "error")
        return redirect(url_for('notes_page'))
    