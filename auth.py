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
  
    # try:
        form = RegistrationForm()
        if form.validate_on_submit():

            sampleDict = {
                 "email": f"{form.email.data}",
                 "Password": f"{form.password.data}",
                 "carPlateNumber":f"{form.PlateNumber.data}",
                 "rememberMe":True,
                 "UserName" : f"{form.username.data}",
             }

            print(sampleDict)

            if (sampleDict): #Email is not found and its unique
                response = requests.post('http://localhost:50455/Account/Register', json=sampleDict)
                
                print(response.text)
                # if(response.ok):
                #     res = make_response(render_template('auth/login.html'))
                #     return res

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

    # except Exception as e:
    #     return render_template("errors/403.html")  # Send user to an error page if something happened during login.

        return render_template('auth/register.html', form=form, title='Register')


from requests.structures import CaseInsensitiveDict

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.cookies.get('token') is not None:
          res = make_response(render_template('home/home.html'))
          return res


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
                print(token)
                if(response.ok):
                        #res = make_response(render_template('admin/mainSystem.html'))
                        #res = flask.make_response()   
                        
                        url = "http://localhost:50455/Account/IsAdmin"
                        print("aaa")
                        print(str(token))
                        payload="{\"probName\": \"Reverse Integer\"}\r\n"
                        headers = {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer '+str(token.get('token')),
                        'Cookie': '.AspNetCore.Identity.Application=CfDJ8E3aAmEvYipFulffWPbZEEG-nx5fCjmJKx2B6xwnQ4SPWV74OpBaW7uCv9Q6vzaAanWgN5Tz-v-_MhaAtMpLaZ8AyLmdUWmJKkldMrVtecYWUQzgwUzQX59RmD_qRI7BrwDnj2A7yb1bWxTZNpDGL7EKpSZED4Y8VlZF7CGJ6CunVJnGYnFp81ivTofBG2u2v0zxILG8gE1y2jklsoyUliSBA9XC5lnZhWYJjSUZI5ShQRPMdNLixUVbFBOQxbVraZ971D-XmOcNNy6VtwtBaZo9mEUmNRc60rE5Ls7DcEsu-hEtUzkLUm3fWOZepxKUUR1C3KZQUnZbejo1FvgJKqyLCQRjut8mvXWjP6lMFFdR907QE-x0Y1BSl8H3VdfRaV3oyaCNhLM8Mvrl3d9KM9F45SOqgJoMrGtDNeRKfziYPsF7hhserjndRAwfwpe9NKdp6Ccq91ryqopHCaNXEX9k0LPf4CgAZhvKrPnANJ4tbqDBmo9rr1R9g0fbLPcRokVzTQ0hblW1tQlMJTAZ9UsV-Fw1hZtJK8A17b4nJh4KgyZi_uiqWjR5YSeks__SUGiDFg6434jTcZNK_ZaFKuYcl6a4wRndd2OPpM4TqSadjWjO3QbI7g53LppZ5HdrY15Z5kDaOD6Z-iJeeQMDfzzE6gNH9I2mNSCRmyGGjm-5s1ui6cqp9yPfspjWCgyqJYK9w5NMPPIIGoz8wD1Ous8'
                        }

                        resp = requests.request("GET", url, headers=headers, data=payload)

                        print(resp.text)

        
                    
                        print(resp.text)
                        if(resp.text == "true"):
                            print("admin")
                            res = make_response(redirect(url_for('admin.home')))
                            res.set_cookie("token", token['token'] ,httponly =True)
                            return res

                        else: 
                            print("user")
                            res = make_response(redirect(url_for('home.parkingSlotes')))
                            res.set_cookie("token", token['token'] ,httponly =True)
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


###NOT YET##
@auth.route('/logout')
def logout():
    ress = make_response(redirect(url_for('home.homepage')))
    url = "http://localhost:50455/Account/Logout"

    payload="{\"probName\": \"Reverse Integer\"}\r\n"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+str(request.cookies.get('token')),
    'Cookie': '.AspNetCore.Identity.Application=CfDJ8E3aAmEvYipFulffWPbZEEG-nx5fCjmJKx2B6xwnQ4SPWV74OpBaW7uCv9Q6vzaAanWgN5Tz-v-_MhaAtMpLaZ8AyLmdUWmJKkldMrVtecYWUQzgwUzQX59RmD_qRI7BrwDnj2A7yb1bWxTZNpDGL7EKpSZED4Y8VlZF7CGJ6CunVJnGYnFp81ivTofBG2u2v0zxILG8gE1y2jklsoyUliSBA9XC5lnZhWYJjSUZI5ShQRPMdNLixUVbFBOQxbVraZ971D-XmOcNNy6VtwtBaZo9mEUmNRc60rE5Ls7DcEsu-hEtUzkLUm3fWOZepxKUUR1C3KZQUnZbejo1FvgJKqyLCQRjut8mvXWjP6lMFFdR907QE-x0Y1BSl8H3VdfRaV3oyaCNhLM8Mvrl3d9KM9F45SOqgJoMrGtDNeRKfziYPsF7hhserjndRAwfwpe9NKdp6Ccq91ryqopHCaNXEX9k0LPf4CgAZhvKrPnANJ4tbqDBmo9rr1R9g0fbLPcRokVzTQ0hblW1tQlMJTAZ9UsV-Fw1hZtJK8A17b4nJh4KgyZi_uiqWjR5YSeks__SUGiDFg6434jTcZNK_ZaFKuYcl6a4wRndd2OPpM4TqSadjWjO3QbI7g53LppZ5HdrY15Z5kDaOD6Z-iJeeQMDfzzE6gNH9I2mNSCRmyGGjm-5s1ui6cqp9yPfspjWCgyqJYK9w5NMPPIIGoz8wD1Ous8'
    }

    res = requests.request("GET", url, headers=headers, data=payload)

    print(res.text)

    ress.delete_cookie("token")
   
    return ress

###########################Pricing##########################

@auth.route('/pricing')
def pricing():

    return render_template('auth/memberPricing.html')

@auth.route('/getSessionIDMonth',methods=['POST'])
def getSessionIDMonth():

        sampleDict = {
                 "priceid": "price_1J6EhlGbd5hvE4QitsvxHzTU",
             }
        print(sampleDict)
      
        sessionID = requests.post('http://localhost:50455/Payment/create-checkout-session',json=sampleDict)

        json_dictionary = json.loads(sessionID.text)
        print(json_dictionary)
        return jsonify({'sessionID' : json_dictionary})


@auth.route('/paymentSucceded',methods=['GET'])
def paymentSucceded():

    return render_template('auth/paymentSucceded.html')

@auth.route('/myPlan')
def myPlan():
       
        sampleDict = {
                 "returnUrl": "https://www.google.com/",
             }
        print(sampleDict)
        token = request.cookies.get('token')
        hed = {'Authorization': 'Bearer ' + token}
        print(token)
        myplan = requests.post('http://localhost:50455/Payment/customer-portal',headers=hed,json=sampleDict)
        
        plan=[]
        json_dictionary = json.loads(myplan.text)
       
        print(json_dictionary['url'])

        return redirect(json_dictionary['url'], code=302)



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


