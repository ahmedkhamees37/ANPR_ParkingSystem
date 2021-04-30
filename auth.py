from flask import Blueprint, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
import json
import requests
from flask import Flask, jsonify, request
from flask import Flask, request, render_template, send_from_directory
from flask_wtf.file import FileField
from flask import request,make_response

auth = Blueprint('auth', __name__)

####USE COMMON FUNCTIONS###
###########################

##
##
class RegistrationForm(FlaskForm):
    email = StringField('Academic Email Address', validators=[Email(), DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    #first_name = StringField('First Name', validators=[DataRequired()])
    #last_name = StringField('Last Name', validators=[DataRequired()])

    PlateNumber = StringField('Car Plate Number ', validators=[DataRequired()])
    
    password = PasswordField('Password', validators=[
        EqualTo('confirm_password'), DataRequired()])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename



@auth.route('/register', methods=['GET', 'POST'])
def register():
  
    try:
        form = RegistrationForm()
        if form.validate_on_submit():

            sampleDict = {
                 "email": form.email.data,
                 "Password": form.password.data,
                 "rememberMe":True,
                 "UserName" : f"{form.username.data}",
             }

            print(sampleDict)

            if (sampleDict): #Email is not found and its unique
                response = requests.post('http://localhost:50455/Account/Register', json=sampleDict)
                print(response)
            #     if response.text !=0:
            # ##################### Send Pic ######################
            #         filepath=upload_file(form.pic.data)
            #         if filepath!=0:
            #             user = selectUserr(form.email.data)
            #             userID = user[0]['ID']
            #             sendPic(1,filepath,userID)
            #             print("calling token")
            #             email=form.email.data
            #             return redirect(url_for('auth.Sendtoken',email=email))
            #         else:
            #             user = selectUserr(form.email.data)
            #             userID = user[0]['ID']
            #             sendPic(1,"1.jpg",userID)
            #             return redirect(url_for('auth.login'))
            #     else:
            #       flash('Error Try Again later or call support')

            else:
                  flash('Check Email')
                  return render_template('auth/register.html', form=form, title='Register')

    except Exception as e:
        return render_template("errors/403.html")  # Send user to an error page if something happened during login.

    return render_template('auth/register.html', form=form, title='Register')



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        ##Sends email to webservices , to get full details of that person
        sampleDict = {"email": f"{form.email.data}", 
                      "passowrd": f"{form.password.data}",
                        "rememberMe":True}     

        if (sampleDict): #Email is not found and its unique
                print(sampleDict)
                response = requests.post('http://localhost:50455/Account/Login', json=sampleDict)
                 # todo with response
                token = json.loads(response.text)
                
        if(response.ok):
                res = make_response(render_template('admin/mainSystem.html'))
                res.set_cookie("token", token['token'] ,httponly =True)
                print(token)
                return res

        #cookie = request.cookies.get('token')

        else:
             flash('Invalid email or password.')

#            if details is not None and details[0]['passwordField']==form.password.data:

        #         session['email'] = details[0]['email']
        #         session['Name_EN'] = details[0]['Name_EN']
        #         serv = selectUserPic(details[0]['ID'])
        #         if serv!=0:
        #             session['picUser']=serv[0]['photoFilePath']
        #         else: session['picUser']="1.jpg"
        #         # #Check if he is admin
        #         if details[0]['Nzha_UserGroups_ID']!=-1:
        #             return redirect(url_for('admin.list_courses'))
        #         else:
        # #             return redirect(url_for('home.homee'))
        #     else:
        #         flash('Invalid email or password.')

    return render_template('auth/login.html', form=form, title='Login')


# ###NOT YET##
# @auth.route('/logout')
# def logout():
#     session.pop('email',None)
#     session.pop('picUser', None)
#     session.pop('Name_EN', None)

#     flash('You have successfully been logged out.')
#     return redirect(url_for('auth.login'))


# ###################################################################################################
# ############TOKEN################
# from flask import Flask, request, url_for
# from flask_mail import Mail, Message
# from itsdangerous import URLSafeTimedSerializer, SignatureExpired
# s = URLSafeTimedSerializer('Thisisasecret!')

# @auth.route('/Sendtoken/<email>', methods=['GET', 'POST'])
# def Sendtoken(email):
#     mail = create_mail()
#     token = s.dumps(email, salt='email-confirm')
#     print(email)
#     print("TOKEEEEEEN")

#     msg = Message('Confirm Email', sender='mohamednaser9851@gmail.com', recipients=[email])

#     link = url_for('auth.confirm_email', token=token, _external=True)

#     msg.body = 'Please click on link to verify your account on Suez Trainning Cource {}'.format(link)
#     mail.send(msg)
#     return render_template('errors/verify.html')

# @auth.route('/confirm_email/<token>')
# def confirm_email(token):
#     try:
#         email = s.loads(token, salt='email-confirm', max_age=8000)
#         verifyAccount(email)
#         print(email)
#     except SignatureExpired:
#         return '<h1>The token is expired!</h1>'
#     return redirect(url_for('auth.login'))


