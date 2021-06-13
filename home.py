from flask import Blueprint,session,request
from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required, current_user
import requests
from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError,SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo
####
####
from wtforms.fields.html5 import TimeField
from flask import Flask, render_template, request, jsonify
home = Blueprint('home', __name__)
from requests.structures import CaseInsensitiveDict

import json

class parkForm(FlaskForm):
    area = SelectField('Sub Category', choices = [('A1', 'A1'), ('B1', 'B1')])
    submit = SubmitField('Search Parking Spaces')

    
@home.route('/')
#@login_required
def homepage():
    
    return render_template('home/home.html')



@home.route('/adminPanel')
def adminPanel():
    
    return render_template('admin/panel.html')



@home.route('/parkingSlotes')
#@login_required
def parkingSlotes():
    
     
        form = parkForm()
        if form.validate_on_submit():

            sampleDict = {
                 "area": form.area.data,
               
             }

            print(sampleDict)

            # if (sampleDict): #Email is not found and its unique
            #     response = requests.post('http://localhost:50455/Account/Register', json=sampleDict)
            #     print(response)

        return render_template('parking/parking.html',form=form)


@home.route('/getParkingSpaces',methods=['POST'])
def getParkingSpaces():
    
        area = request.form['area']
       
        if (area): #Email is not found and its unique
                numberOfSlots = requests.get('http://localhost:50455/Parking/GetCountRegisterParking',params={'LotName': area})
                print(numberOfSlots.text)

         
        return jsonify({'Nslots' : numberOfSlots.text})




@home.route('/RegisterParkingSpaces',methods=['POST'])
def RegisterParkingSpaces():
    
        space = request.form['space']
        print(type(space))
        print("aaa"+space)
        sampleDict = {
                 "parking_slot": space
     
             }
        token = request.cookies.get('token')
        hed = {'Authorization': 'Bearer ' + token}
      
        print(token)
        numberOfSlots = requests.post('http://localhost:50455/Parking/RegisterParking',headers=hed,json=sampleDict)
        print(numberOfSlots.text)
        print(numberOfSlots)

        return jsonify({'Nslots' : "aa"})





####newww####
@home.route('/homee')
#@login_required
def homee():
    
    return render_template('home/index.html')

