from flask import Blueprint,session
from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required, current_user
import requests
from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo
####
####
home = Blueprint('home', __name__)

import json

@home.route('/adminPanel')
def adminPanel():
    
    return render_template('admin/panel.html')


@home.route('/parkingSlotes')
#@login_required
def parkingSlotes():
    
    return render_template('parking/parking.html')


####newww####
@home.route('/homee')
#@login_required
def homee():
    
    return render_template('home/index.html')

