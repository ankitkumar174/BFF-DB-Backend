from flask import Flask, json, request, jsonify, send_file
import os
import urllib.request
from werkzeug.utils import secure_filename
import random

application = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/')
def main():
    return 'Homepage'


@application.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400

        return resp

    files = request.files.getlist('files[]')

    errors = {}
    success = False
    filename = ''

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(
                os.path.join(application.config['UPLOAD_FOLDER'], filename))
            success = True

        else:
            errors[file.filename] = 'File type is not allowed'

    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'

        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({
            'message': 'Files successfully uploaded',
            'url': get_json(filename)
        })
        resp.status_code = 201
        return resp

    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp


@application.route('/json')
def get_json(filename):
    intDir = '/static/uploads/'
    url = ''
    return str(url + intDir + filename)



if __name__ == '__main__':
    application.run(host='0.0.0.0',
		port=random.randint(2000, 9000))
