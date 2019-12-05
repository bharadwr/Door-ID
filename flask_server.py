# Runs on the 477 Machine, receives image uploads from the client train_faces.py
import os, subprocess
from flask import Flask, request, redirect, url_for, send_from_directory
import azure_face
import slack_rtmclient, slack_webclient
from uuid import uuid4

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], "user.jpg")
        file.save(path)
        confidence = azure_face.IdentifyPersonInImage(personImage=path)
        if confidence is None:
            print("No faces detected in image, going to sleep", confidence)
            slack_webclient.send_file(file_path=path, file_title="no user in frame")
            slack_webclient.send_message(message="No users detected in frame")
            return "No faces in frame"

        elif confidence < 0.7:
            print("Unidentified person")
            slack_webclient.send_file(file_path=path, file_title="unrecognized person")
            slack_webclient.send_message(message="Unrecognized person at door, please respond with thumbs to add to known users, and thumbs down to deny.")
            try:
                grepOut = subprocess.check_output("python3 slack_rtmclient.py", shell=True, stderr=subprocess.STDOUT)
                if "Authorized" in grepOut.decode():
                    print("Adding user to known visitor list")
                    azure_face.AddPersonToPersonGroup(personName=str(uuid4()), imgFile=path)
                    slack_webclient.send_message(message="Adding user to known visitor list")
                    return "Adding user to known visitor list"
                elif "Unauthorized" in grepOut.decode():
                    print("Ignoring user due to negatory response")
                    slack_webclient.send_message(message="Ignoring user due to negatory response")
                    return "Ignoring user due to negatory response"

            except subprocess.CalledProcessError as grepexc:
                print("error code", grepexc.returncode, grepexc.output)
                slack_webclient.send_message(message="Ignoring user due to error in server")
                return "Ignoring user due to error in server"

        elif confidence >= 0.7:
            print("Known user at door", confidence)
            slack_webclient.send_file(file_path=path, file_title="known user")
            slack_webclient.send_message(message="Known user at door with confidence: " + str(confidence))
            return "Known user at door"

    else:
        return "joe"

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=40862, debug=True)
