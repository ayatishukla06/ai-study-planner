# 🚀 AI Study Planner 

An intelligent, full-stack study management system designed to help engineering students master complex subjects. This application integrates an automated study scheduler with advanced AI features powered by Google's latest **Gemini 2.0 Flash API** to dynamically map out syllabi and summarize heavy technical documents.

---

##  Key Features

* **🧠 AI PDF Summarizer**: Processes complex technical PDFs (up to 50 pages) and extracts structured, simplified study notes with bold headings and clean HTML formatting.
* **📸 AI Syllabus Scanner**: Automatically extracts core study topics from uploaded syllabus images and populates them directly into your dashboard.
* **📅 Automated Schedule Engine**: Generates a day-by-day study priority roadmap based on user-defined exam dates and topic priorities.
* **📊 Interactive Analytics (`charts.js`)**: Displays modern charts visualizing study completion metrics dynamically.
* **⏱️ Focus Buff (`pomodoro.js`)**: An integrated Pomodoro countdown timer designed to maximize revision efficiency.
* **🎮 Gamified Quest Tracker (`quests.js`)**: Tracks topic masteries dynamically using custom interactive progress animations.
* **🔒 Secure Architecture**: Implements production security standards by keeping sensitive keys isolated from version history.

---

##  Tech Stack

* **Backend Framework**: Python Flask
* **Database & ORM**: SQLite with SQLAlchemy ORM
* **Database Migrations**: Flask-Migrate (Alembic engine tracking state changes)
* **User Authentication**: Flask-Login (Secure session management)
* **AI Integration**: Google GenAI SDK (`google-genai` using `gemini-2.0-flash`)
* **Document Parsing**: PyPDF2
* **UI/UX Aesthetics**: Glassmorphism dark mode theme built with responsive CSS variables

---

##  Repository Directory Structure

```text
/ai-study-planner
├── app/
│   ├── static/          # Static asset pipelines
│   │   ├── css/
│   │   │   └── auth.css  # CSS for clean, centered login/signup forms
│   │   ├── charts.js     # Analytics tracking front-end logic
│   │   ├── pomodoro.js   # Focus timer automation code
│   │   ├── quests.js     # Task completion animations
│   │   └── style.css     # Global core layout theme styling
│   ├── templates/       # Glassmorphic view blocks
│   │   ├── base.html    # Core boilerplate shell
│   │   ├── dashboard.html # Study map visual terminal
│   │   ├── login.html   # Fully centered glassmorphism login system
│   │   ├── notes.html   # AI text layout engine viewer
│   │   └── signup.html  # Personalized user registration page
│   ├── __init__.py      # App factory configuration structure
│   ├── models.py        # Database entity maps (User, Subject, Topic, StudyPlan)
│   ├── routes.py        # Framework request handler & GenAI client logic
│   └── scheduler.py     # Algorithmic study plan compilation rules
├── migrations/          # Managed version tracks for schema changes
├── .env.template        # Layout instructions for local configuration keys
├── .gitignore           # Safeguard rule configurations excluding private keys
├── config.py            # Global runtime properties mapping
├── requirements.txt     # Locked production pipeline dependencies
└── run.py               # Main application initiation block
