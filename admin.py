from datetime import datetime
from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
import json
import requests
from flask_wtf.file import FileField ###TO upload file
from collections import defaultdict
admin = Blueprint('admin', __name__)

from flask import Flask, render_template, request, redirect ,Response,send_file,session,jsonify
import numpy as np
import cv2
import urllib.request
import cv2
import numpy as np
from ml import alpr

ALLOWED_EXTENSIONS = {'jpg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ob1 = alpr()


MODEL=None

from tensorflow.keras.models import load_model

model = load_model('model.h5', compile = False)
import os 
import random
import string
from getFrames import FileVideoStream



# def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))

# ################
# @admin.after_request
# def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r
# @admin.route('/alpr', methods = ['POST','GET'])

# def index():
#   prediction={}
#   if request.method == 'POST': 
#        pic = request.files['photo']
       
#        if pic and allowed_file(pic.filename):
          
#           #npimg = np.fromstring(pic, np.uint8)
#           #img = cv2.imdecode(npimg,cv2.IMREAD_COLOR) 
#         #   id = id_generator()
#           pic.save(os.path.join('recentplates',2+'.jpg'))
#           picPath='recentplates/'+id+'.jpg'
#           prediction=ob1.plateRecog(picPath,model)
          

#   return render_template('admin/mainSystem.html',prediction=prediction)

@admin.route('/system')
def home():
    """Video streaming home page."""
    return render_template('admin/mainSystem.html')

##############
#cap1  = FileVideoStream("2.mp4")
##############
# def video_object():
#     return cv2.VideoCapture(0)

from cam import CameraStream






@admin.route('/video_feed/<action>')
def video_feed(action):
    if(action=="on"):

        return Response(ob1.liveFeed(CameraStream().start(),model),
                        mimetype='multipart/x-mixed-replace; boundary=frame')  
    else:
     return "oo.jpg"

@admin.route('/camera/<action>')
def camera(action):

     """Video streaming route. Put this in the src attribute of an img tag."""
     if(action=="on"):
        return Response(ob1.camera( CameraStream().start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')  
     else:
      return "oo.jpg"
  

@admin.route('/getPlateNumber', methods=['GET'])
def getPlateNumber():
                    output = ob1.getPlate( CameraStream())      
     
                    # sampleDict = {"number_Plate": f"{output}",
                    # "GateId":1,
                    # "Acess_DateTime":"2019-01-06T17:16:40"
                    # }     
                    # print(sampleDict) 
                    # print("ssssssssss")
                    # response = requests.post('http://localhost:50455/Account/Access', json=sampleDict)
                    # print(response.text)
                                                                                                                                                                                 
                    return Response(output, mimetype='text')                                                                                                                                              
                                                                                                                                                                             



