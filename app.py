# app.py
from flask import Flask, request, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from googletrans import Translator
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///translations.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

translator = Translator()

class Translation(db.Model):
    id = db.column(db.Integer, primary_key=True)
    japanese_text = db.Column(db.String(500), nullable=False)
    english_text = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Translation('{self.japanese_text}', '{self.english_text}')"
    
with app.app_context():
    db.create_all()




@app.route("/", methods=["GET", "POST"])
def index():
    translated = ""
    if request.method == "POST":
        text_ja = request.form["japanese_text"]
        translated = translator.translate(text_ja, src="ja", dest="en").text
    return render_template("index.html", translated=translated)


if __name__ == "__main__":
    app.run(debug=True)
