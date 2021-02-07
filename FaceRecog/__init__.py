import os
from flask import Flask
from werkzeug import secure_filename
# Flask object initialization
# app flask object has to be created before importing views below
# because it calls "import app from app"
UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}

# app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
