# Runs on the 477 Machine, receives image uploads from the client train_faces.py
import os, subprocess
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], "user.jpg"))
        slack_output = str(subprocess.check_output(['python3', 'slackbot.py'], stderr= subprocess.STDOUT))
        print(slack_output)
        return slack_output
    else:
        return "joe"

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=40862)
