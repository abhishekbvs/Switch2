import os, csv, json, requests, datetime
from config import Config
from flask import render_template, flash, redirect, request, url_for, jsonify
from app import app, login, mail
from app.models import User
from app.forms import AddTalk, AddWorkshop, MoreData, CABegin, CAQues, test, EduData, AmrSOY
from app.mail import farer_welcome_mail, amrsoy_reg_mail, testing_mail
from app.more import get_user_ip
from app.farer import staff_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required

@login.unauthorized_handler
def unauthorized():
    return render_template('accounts/login.html', link="")

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', page="/home?m=1", uchange="")

@app.route('/home', methods=['GET'])
def home():
    mode = request.args.get('m')
    print(mode)

    if mode is not None:
        if mode == "1":
            return render_template('home.html')
    else:
        return render_template('index.html', page="/home?m=1", uchange="")

@app.route('/talks/')
def talks():
    return render_template('coming.html')

@app.route('/concerts/')
def concert():
    return render_template('coming.html')

@app.route('/exhibitions/')
def exhibitions():
    return render_template('exhibitions.html')

@app.route('/contests/')
def contests():
    return render_template('contests.html')

@app.route('/workshops/')
def workshops():
    return render_template('workshops.html')

@app.route('/sponsors/')
def sponsors():
    return render_template('sponsors.html')

# Individual pages

dept = ['CSE', 'ECE', 'ME', 'Physics', 'Chemisty', 'English', 'Biotech','BUG', 'Comm.', 'Civil', 'EEE', 'Gaming', 'Maths', 'Others']

@app.route('/workshops/<int:wid>/')
def workshop_single(wid):
    mode = request.args.get('m') 
    
    if mode is not None:
        if mode == "1":
            workshop = requests.get(Config.hub_url+'/events/workshops/'+str(wid))
            workshop = workshop.json()
            payload = {
                'vid': workshop.get('support')
            }
            support = requests.get(Config.hub_url+'/farer/user/contact', json=payload)
            support = support.json()
            if workshop is None:
                return "404"
            return render_template('individual-workshops.html', workshop = workshop, dept=dept, support=support)
    else:
        return render_template('workshops.html', open=True, wid=wid)

@app.route('/contests/<int:cid>/')
def contests_single(cid):
    mode = request.args.get('m')
    
    if mode is not None:
        if mode == "1":
            contest = requests.get(Config.hub_url+'/events/contests/'+str(cid))
            contest = contest.json()
            support = requests.get(Config.hub_url+'/farer/user/contact', json=payload)
            support = support.json()
            if contest is None:
                return "404"

            return render_template('individual-contests.html', contest=contest, dept=dept, support=support)
    else:
        return render_template('contests.html', open=True, cid=cid)

# Error handlers

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# URL services for Volunteers

@app.route('/staff/creation', methods=['GET', 'POST'])
@staff_required(5)
def staff_creation():

    # if request.method == 'POST':

    return render_template('dash/staff_creation.html')