# app.py
from flask import Flask, request, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from googletrans import Translator
import os

from models import db, Translation

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///translations.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.urandom(24)

db.init_app(app)
migrate = Migrate(app, db)

translator = Translator()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        japanese = request.form.get("japanese_text")
        if japanese:
            english = translator.translate(japanese, src="ja", dest="en").text

            new_translation = Translation(japanese_text=japanese, english_text=english)
            db.session.add(new_translation)
            db.session.commit()
            return redirect(url_for("index"))
    history = Translation.query.all()
    return render_template("index.html", history=history)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
