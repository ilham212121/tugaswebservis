import os
from tkinter import Image
from flask import Flask,jsonify,request,flash
from flask_httpauth import HTTPTokenAuth
import random
import string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash 

from werkzeug.utils import secure_filename
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
def allowed_gambar(gambarname):     
  return '.' in gambarname and gambarname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
UPLOAD_FOLDER = 'hasil_upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

database_file = "sqlite:///{}".format(os.path.join(project_dir, "ilham.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file 
db = SQLAlchemy(app)

class uploaddb(db.Model):
    image=db.Column(db.String(225),unique=False,nullable=False, primary_key=True) 

@app.route('/form/bmi', methods=['POST'])
def bmi():
    if 'gambar' not in request.files:
        flash('No gambar part')
        return jsonify({
            "pesan":"tidak ada form gambar!"
            })
    gambar = request.files['gambar']
    if gambar.filename == '':
        return jsonify({
            "pesan":"tidak ada gambar image yang dipilih"
            })
    if gambar and allowed_gambar(gambar.filename):
        gambarname = secure_filename(gambar.filename)
        gambar.save(os.path.join(app.config['UPLOAD_FOLDER'], gambarname))

        path_image = uploaddb(image=gambarname)
        db.session.add(path_image)
        db.session.commit()

        return jsonify({
            "pesan":"gambar telah terupload"
            })
    else:
        return jsonify({
        "pesan":"bukan gambar image"
        })

if __name__ == '__main__':
    app.run(debug=False, port=8888)