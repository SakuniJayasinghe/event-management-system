from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)  
    description = db.Column(db.Text, nullable=True)  

    def __repr__(self):
        return f'<Event {self.name}>'
