from App.models import User, Student, Staff, HourLog
from App.database import db

def create_user(username, password, user_type="student"):
    if user_type == "student":
        newuser = Student(username=username, password=password)
    elif user_type == "staff":
        newuser = Staff(username=username, password=password)
    elif user_type == "admin":
        newuser = User(username=username, password=password, user_type="admin")
    else:
        raise ValueError("Invalid role")
    db.session.add(newuser)
    db.session.commit()
    return newuser

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def log_hours(student_id, staff_id, hours):
    log = HourLog(student_id=student_id, staff_id=staff_id, hours=hours)
    db.session.add(log)
    db.session.commit()
    return log

def confirm_hours(log_id, staff_id, confirm=True):
    log = HourLog.query.get(log_id)
    if log and log.staff_id == staff_id:
        log.confirmed = confirm
        if confirm:
            student = Student.query.get(log.student_id)
            student.hours += log.hours
        db.session.commit()
        return log
    return None

def get_leaderboard():
    students = Student.query.order_by(Student.hours.desc()).all()
    return [s.get_json() | {"hours": s.hours} for s in students]

def get_student_accolades(student_id):
    student = Student.query.get(student_id)
    if student:
        return student.get_accolades()
    return []

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None

