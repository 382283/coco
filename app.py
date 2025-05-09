from flask import Flask, render_template, request, send_from_directory
from googletrans import Translator
from gtts import gTTS
import os

app = Flask(__name__)
app.config["AUDIO_FOLDER"] = "static/audio"

os.makedirs(app.config["AUDIO_FOLDER"], exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    text_en = ""
    audio_file = None

    if request.method == "POST":
        translator = Translator()
        text_ja = request.form["input_text"]
        text_en = translator.translate(text_ja, src="ja", dest="en").text

        # 音声ファイルを作成
        tts = gTTS(text=text_en, lang="en")
        audio_file = "output.mp3"
        audio_path = os.path.join(app.config["AUDIO_FOLDER"], audio_file)
        tts.save(audio_path)

    return render_template("index.html", text_en=text_en, audio_file=audio_file)


# オーディオファイルを提供するルート（必要に応じて）
@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(app.config["AUDIO_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
