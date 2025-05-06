from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    japanese_text = db.Column(db.String(500), nullable=False)
    english_text = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Translation('{self.japanese_text}','{self.english_text}')"
