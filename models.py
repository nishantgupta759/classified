from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    society = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    website = db.Column(db.String(255))
    offer = db.Column(db.String(255))
    visit_details = db.Column(db.Text)

    def __repr__(self):
        return f'<Advertisement {self.title}>'
