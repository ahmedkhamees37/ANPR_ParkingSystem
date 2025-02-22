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
    # logged = False
    # cookie = request.cookies.get('token')
    # if(cookie is not None):
    #     logged = True

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


def deleteParking():
        aa = requests.get('http://localhost:50455/Parking/RegisterParking')
        print(aa)


@home.route('/endParkingReve',methods=['GET'])
def endParkingReve():

        url = "http://localhost:50455/Parking/EndReservation"
      
        response = requests.request("GET", url)
       
        return jsonify({'mySlot' : "done"})


@home.route('/getParkingSpaces',methods=['POST'])
def getParkingSpaces():
        deleteParking()
        area = request.form['area']
        slots=[]
        if (area): #Email is not found and its unique
                numberOfSlots = requests.get('http://localhost:50455/Parking/Get_ParkingSlot',params={'LotName': area})
                
                json_dictionary = json.loads(numberOfSlots.text)
                print(json_dictionary)
                for i in range(len(json_dictionary)):
                    slots.append(int(json_dictionary[i]['slot_number']))
        print(slots)
        return jsonify({'slots' : slots})


@home.route('/myParkingSpace',methods=['GET'])
def myParkingSpace():

        url = "http://localhost:50455/Parking/Get_UserParkingSlot"
     

        payload={}
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+str(request.cookies.get('token')),
        'Cookie': '.AspNetCore.Identity.Application=CfDJ8E3aAmEvYipFulffWPbZEEG-nx5fCjmJKx2B6xwnQ4SPWV74OpBaW7uCv9Q6vzaAanWgN5Tz-v-_MhaAtMpLaZ8AyLmdUWmJKkldMrVtecYWUQzgwUzQX59RmD_qRI7BrwDnj2A7yb1bWxTZNpDGL7EKpSZED4Y8VlZF7CGJ6CunVJnGYnFp81ivTofBG2u2v0zxILG8gE1y2jklsoyUliSBA9XC5lnZhWYJjSUZI5ShQRPMdNLixUVbFBOQxbVraZ971D-XmOcNNy6VtwtBaZo9mEUmNRc60rE5Ls7DcEsu-hEtUzkLUm3fWOZepxKUUR1C3KZQUnZbejo1FvgJKqyLCQRjut8mvXWjP6lMFFdR907QE-x0Y1BSl8H3VdfRaV3oyaCNhLM8Mvrl3d9KM9F45SOqgJoMrGtDNeRKfziYPsF7hhserjndRAwfwpe9NKdp6Ccq91ryqopHCaNXEX9k0LPf4CgAZhvKrPnANJ4tbqDBmo9rr1R9g0fbLPcRokVzTQ0hblW1tQlMJTAZ9UsV-Fw1hZtJK8A17b4nJh4KgyZi_uiqWjR5YSeks__SUGiDFg6434jTcZNK_ZaFKuYcl6a4wRndd2OPpM4TqSadjWjO3QbI7g53LppZ5HdrY15Z5kDaOD6Z-iJeeQMDfzzE6gNH9I2mNSCRmyGGjm-5s1ui6cqp9yPfspjWCgyqJYK9w5NMPPIIGoz8wD1Ous8'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        slots=[]
        json_dictionary = json.loads(response.text)
        for i in range(len(json_dictionary)):
                    slot = json_dictionary[i]
        print(slot)
        return jsonify({'mySlot' : slot})



@home.route('/RegisterParkingSpaces',methods=['POST'])
def RegisterParkingSpaces():
    


        space = request.form['space']
        hours = request.form['hours']
        print(type(space))
        print("aaa"+space)
        sampleDict = {
                 "parking_slot": space,
                 "Rhour":hours,
             }
        print(sampleDict)
        token = request.cookies.get('token')
        hed = {'Authorization': 'Bearer ' + token}
      
        print(token)
        numberOfSlots = requests.post('http://localhost:50455/Parking/RegisterParking',headers=hed,json=sampleDict)
        print(numberOfSlots.text)
        print(numberOfSlots)

        return jsonify({'Nslots' : "aa"})



@home.route('/Cancel_Reservation',methods=['POST'])
def Cancel_Reservation():
    
        url = "http://localhost:50455/Parking/Cancel_Reservation"
     
        payload={}
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+str(request.cookies.get('token')),
        'Cookie': '.AspNetCore.Identity.Application=CfDJ8E3aAmEvYipFulffWPbZEEG-nx5fCjmJKx2B6xwnQ4SPWV74OpBaW7uCv9Q6vzaAanWgN5Tz-v-_MhaAtMpLaZ8AyLmdUWmJKkldMrVtecYWUQzgwUzQX59RmD_qRI7BrwDnj2A7yb1bWxTZNpDGL7EKpSZED4Y8VlZF7CGJ6CunVJnGYnFp81ivTofBG2u2v0zxILG8gE1y2jklsoyUliSBA9XC5lnZhWYJjSUZI5ShQRPMdNLixUVbFBOQxbVraZ971D-XmOcNNy6VtwtBaZo9mEUmNRc60rE5Ls7DcEsu-hEtUzkLUm3fWOZepxKUUR1C3KZQUnZbejo1FvgJKqyLCQRjut8mvXWjP6lMFFdR907QE-x0Y1BSl8H3VdfRaV3oyaCNhLM8Mvrl3d9KM9F45SOqgJoMrGtDNeRKfziYPsF7hhserjndRAwfwpe9NKdp6Ccq91ryqopHCaNXEX9k0LPf4CgAZhvKrPnANJ4tbqDBmo9rr1R9g0fbLPcRokVzTQ0hblW1tQlMJTAZ9UsV-Fw1hZtJK8A17b4nJh4KgyZi_uiqWjR5YSeks__SUGiDFg6434jTcZNK_ZaFKuYcl6a4wRndd2OPpM4TqSadjWjO3QbI7g53LppZ5HdrY15Z5kDaOD6Z-iJeeQMDfzzE6gNH9I2mNSCRmyGGjm-5s1ui6cqp9yPfspjWCgyqJYK9w5NMPPIIGoz8wD1Ous8'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code==200:
             return jsonify({'success' : '200'})

        else:
             return jsonify({'failure' : '400'})




####newww####
@home.route('/homee')
#@login_required
def homee():
    
    return render_template('home/index.html')

