from flask import Flask, request, jsonify
import os
import pickle
import numpy as np
import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime, timedelta
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Firebase initialization
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recog-6f4f3-default-rtdb.firebaseio.com/",
    'storageBucket': "face-recog-6f4f3.appspot.com"
})
bucket = storage.bucket()

# Load the encoding file
with open('EncodeFile.p', 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)
encodeListKnown, studentIds = encodeListKnownWithIds

@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.get_json()
    image_data = base64.b64decode(data['image'])
    np_img = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                id = studentIds[matchIndex]
                studentInfo = db.reference(f'Students/{id}').get()
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)
                _, buffer = cv2.imencode('.png', imgStudent)
                img_str = base64.b64encode(buffer).decode()

                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                if secondsElapsed > 120:  # 120 seconds = 2 minutes
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                    return jsonify({
                        'attendance_status': 'Attendance marked successfully',
                        'student_id': id,
                        'student_info': studentInfo,
                        'img_url': f'data:image/png;base64,{img_str}'
                    })
                else:
                    return jsonify({
                        'attendance_status': 'Try after some time',
                        'student_id': id,
                        'student_info': studentInfo,
                        'img_url': f'data:image/png;base64,{img_str}',
                        'timetotake': 120-secondsElapsed
                    })

    return jsonify({'attendance_status': 'No face recognized'})

if __name__ == '__main__':
    app.run(debug=True)
