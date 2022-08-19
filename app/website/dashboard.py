from flask import Blueprint, render_template, request, flash, jsonify, Flask
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from .models import user
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .res.mymail import *
import re

import random, string
dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/', methods=['GET', 'POST'])
@login_required
def dash():
    return render_template("dashboard/dashboard.html", user=current_user)


