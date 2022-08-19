from flask import Blueprint, render_template, request, flash, jsonify, Flask
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from .models import user, group
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .res.mymail import *
import re

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

@groups.route('/join', methods=['GET', 'POST'])
@login_required
def join():
    return "join"

@groups.route('/leave', methods=['GET', 'POST'])
@login_required
def leave():
    return "leave"

@groups.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    theuser = current_user
    new_group = group(group_name="booby", is_activated=True)
    new_group.users.append(theuser)
    db.session.add(new_group)
    db.session.commit()
    return "fuck flask"

@groups.route('/view')
@login_required
def view():
    thegroup = group.query.filter_by(id=6).first()
    data = ""
    for theuser in thegroup.users:
        data = data + theuser.first_name + " "
    
    return data