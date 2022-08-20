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
        new_group.adminusers.append(theuser)
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

@groups.route('/leave', methods=['GET', 'POST'])
@login_required
def leave():
    groupID = request.args.get('id')
    test_group = group.query.filter_by(id=groupID).first()
    if current_user in test_group.users:
        test_group.users.remove(current_user)
        db.session.commit()
        flash("Left Group", '')
    else:
        flash("Not in this group", 'error')
    return render_template("group/leavegroup.html", user=current_user)

@groups.route('/view')
@login_required
def view():
    groupID = request.args.get('id')
    test_group = group.query.filter_by(id=groupID).first()
    if test_group:
        flash("valid group", '')
        if current_user in test_group.adminusers:
            flash("admin", '')
    else:
        flash("Invalid group!", 'error')
    return render_template("group/viewgroup.html", user=current_user)

@groups.route('/admin')
@login_required
def admin():
    groupID = request.args.get('id')
    test_group = group.query.filter_by(id=groupID).first()
    if test_group:
        flash("valid group", '')
        if current_user in test_group.adminusers:
            flash("admin", '')
    else:
        flash("Invalid group!", 'error')
    return render_template("group/groupadmin.html", user=current_user)