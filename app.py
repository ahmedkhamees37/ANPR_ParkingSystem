from flask import Flask , session
import json
import requests
from flask import Flask, jsonify, request
from flask import Flask, request, render_template, send_from_directory
###############################
# Initialize Flask
import json

from flask_bootstrap import  Bootstrap
from flask import Flask, request, url_for

app = Flask(__name__)

Bootstrap(app)
app.config['SECRET_KEY']="aaa"

app.config['WTF_CSRF_ENABLED'] = False

SESSION_COOKIE_SECURE = True
REMEMBER_COOKIE_SECURE = True

###################
from home import home as home_blueprint
app.register_blueprint(home_blueprint)

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)


if __name__ == '__main__':
    app.run(debug=False,threaded=True)


