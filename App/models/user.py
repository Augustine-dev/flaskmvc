from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(70), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(10), nullable=False) # Used for differeniating types of user - "student", "staff", "admin"

    __mapper_args__ = {
        'polymorphic_on': user_type,
        'polymorphic_identity': 'user'
    }

    def __init__(self, username, password, email, user_type="student"):
        self.username = username
        self.set_password(password)
        self.email = email
        self.user_type = user_type

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.username}>"

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'user_type': self.user_type
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Student(User):
    __tablename__="student"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    hours = db.Column(db.Integer, default=0)

    __mapper_args__={
        'polymorphic_identity': 'student',
    }

    def get_accolades(self):
        milestones = [10, 25, 50]
        return [m for m in milestones if self.hours >= m]
    
class Staff(User):
    __tablename__="staff"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    __mapper_args__={
        'polymorphic_identity': 'staff',
    }

class HourLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=True)
    hours = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

    def get_json(self):
        return {
            'id' : self.id,
            'student_id': self.student_id,
            'staff_id' : self.staff_id,
            'hours':self.hours,
            'confirmed' : self.confirmed
        }
