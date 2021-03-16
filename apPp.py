from flask import Flask, render_template, request, redirect ,Response,send_file,session,jsonify
import numpy as np
import cv2
import urllib.request
import cv2
import numpy as np
from ml import alpr
app = Flask(__name__)

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


app.config['SECRET_KEY']="aaa"

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

################
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
@app.route('/alpr', methods = ['POST','GET'])

def index():
  prediction={}
  if request.method == 'POST': 
       pic = request.files['photo']
       
       if pic and allowed_file(pic.filename):
          
          #npimg = np.fromstring(pic, np.uint8)
          #img = cv2.imdecode(npimg,cv2.IMREAD_COLOR) 
          id = id_generator()
          pic.save(os.path.join('recentplates',id+'.jpg'))
          picPath='recentplates/'+id+'.jpg'
          prediction=ob1.plateRecog(picPath,model)
          

  return render_template('homepage.html',prediction=prediction)

@app.route('/')
def home():
    """Video streaming home page."""
    return render_template('homepage.html')

##############
cap1  = FileVideoStream("2.mp4")
##############
# def video_object():
#     return cv2.VideoCapture(0)

from cam import CameraStream
cap = CameraStream().start()




@app.route('/video_feed/<action>')
def video_feed(action):
    if(action=="on"):
        return Response(ob1.liveFeed(cap,model),
                        mimetype='multipart/x-mixed-replace; boundary=frame')  
    else:
      return "oo.jpg"

@app.route('/camera/<action>')
def camera(action):

    """Video streaming route. Put this in the src attribute of an img tag."""
    if(action=="on"):
          return Response(ob1.camera(cap),
                    mimetype='multipart/x-mixed-replace; boundary=frame')  
   
    else:
      return "oo.jpg"
  
import requests
@app.route('/getPlateNumber', methods=['GET'])
def getPlateNumber():
    output = ob1.getPlate(cap)
    # from datetime import datetime

    # # datetime object containing current date and time
    # now = datetime.now()
   

    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # # print("date and time =", dt_string)	
                                                                                       
    return Response(output, mimetype='text')                                                                                                                                              
                                                                                                                                                                             



# if __name__ == '__main__':
#     app.run(debug=True,threaded=True)


