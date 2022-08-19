from cgi import test
from flask import Blueprint, render_template, request, flash, jsonify, Flask
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from .models import user, group
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .res.mymail import *
import re
from .forms import CreateAGroupForm, JoinAGroupForm

import random, string
groups = Blueprint('groups', __name__)

@groups.route('/', methods=['GET', 'POST'])
@login_required
def grouphome():
    return "group"

@groups.route('/mygroups', methods=['GET', 'POST'])
@login_required
def mygroups():
    return "my groups"



@groups.route('/leave', methods=['GET', 'POST'])
@login_required
def leave():
    return "leave"

@groups.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    createGroupForm = CreateAGroupForm()
    theuser = current_user
    if request.method=='POST' and createGroupForm.validate_on_submit():
        group_name = createGroupForm.groupname.data
        jointoken = generateJoinToken()
        new_group = group(group_name=group_name, join_token=jointoken, is_activated=True)
        new_group.users.append(theuser)
        db.session.add(new_group)
        db.session.commit()
        flash("Group Creation Successful", '')
    return render_template("group/creategroup.html", user=current_user, form=createGroupForm)

def generateJoinToken():
    # Generates a token, which users can then use to join a group
    validToken = False
    token=''
    while not validToken:
        letters=string.ascii_lowercase
        token= ''.join(random.choice(letters) for i in range(12))
        testgroup = group.query.filter_by(join_token=token).first()
        if not testgroup:
            validToken=True
    return token

@groups.route('/join', methods=['GET', 'POST'])
@login_required
def join():
    joinGroupForm = JoinAGroupForm()
    if request.method=='POST' and joinGroupForm.validate_on_submit():
        token = joinGroupForm.jointoken.data
        test_group = group.query.filter_by(join_token=token).first()
        if not test_group:
            flash("Invalid Joining Token", 'error')
        else:
            if current_user in test_group.users:
                flash("Already in group", 'error')
            test_group.users.append(current_user)
            db.session.commit()
    return render_template("group/joingroup.html", user=current_user, form=joinGroupForm)

@groups.route('/view')
@login_required
def view():
    thegroup = group.query.filter_by(id=6).first()
    data = ""
    for theuser in thegroup.users:
        data = data + theuser.first_name + " "
    
    return data