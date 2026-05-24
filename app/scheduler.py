from datetime import datetime, timedelta
from app import db
from app.models import StudyPlan, Topic, Subject

def calculate_study_plan(user_id, exam_date, daily_limit_minutes=150):
    # Convert string date from form to Python date object
    if isinstance(exam_date, str):
        exam_date = datetime.strptime(exam_date, '%Y-%m-%d').date()
    
    today = datetime.now().date()
    start_date = today + timedelta(days=1)
    
    # Validation: Exam must be in the future
    if (exam_date - start_date).days < 0:
        return {"status": "error", "message": "Exam date must be after today!"}

    # 1. Clear existing plan for this user to avoid duplicates
    StudyPlan.query.filter_by(user_id=user_id).delete()

    # 2. Fetch all uncompleted topics belonging to this user via Subject join
    topics = Topic.query.join(Subject).filter(
        Subject.user_id == user_id, 
        Topic.is_completed == False
    ).all()
    
    if not topics:
        return {"status": "error", "message": "Add some subjects and topics first!"}

    # 3. Sort by priority (1 is highest priority)
    sorted_topics = sorted(topics, key=lambda x: x.priority)

    current_date = start_date
    minutes_used_today = 0
    
    # 4. Distribution Logic
    for topic in sorted_topics:
        # If adding this topic exceeds the 2.5 hour limit, move to next day
        if minutes_used_today + topic.estimated_time > daily_limit_minutes:
            current_date += timedelta(days=1)
            minutes_used_today = 0

        # Stop scheduling if we hit the exam date
        if current_date >= exam_date:
            break

        new_entry = StudyPlan(
            user_id=user_id,
            topic_id=topic.id,
            scheduled_date=current_date
        )
        db.session.add(new_entry)
        minutes_used_today += topic.estimated_time

    db.session.commit()
    return {"status": "success", "message": "Systematic plan generated!"}