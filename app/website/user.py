from flask import Blueprint, render_template, request, flash, jsonify, Flask
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from .models import user, group
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .res.mymail import *
import re

import random, string
userblue = Blueprint('user', __name__)

@userblue.route('/', methods=['GET', 'POST'])
@login_required
def myaccount():
    data = ""
    #thegroups = user.query.filter_by(user = current_user).first()
    for tgroup in current_user.groups:
        data = data + tgroup.group_name + " "
    return data
    #for thegroup in current_user.groups:
    #    data = data + thegroup.group_name + " "
    #thegroups = group.query.filter_by(users = current_user).first()
    #for thegroup in thegroups:
    #    data = data + thegroup.group_name + ""
    #return data

