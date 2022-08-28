from cgi import test
from flask import Blueprint, render_template, request, flash, jsonify, Flask, abort
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from .models import user, group, assets
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .res.mymail import *
import re
from .forms import CreateAGroupForm, JoinAGroupForm, CreateAssetForm

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
        new_group = group(group_name=group_name, token=jointoken, is_activated=True)
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
        testgroup = group.query.filter_by(token=token).first()
        if not testgroup:
            validToken=True
    return token

@groups.route('/join', methods=['GET', 'POST'])
@login_required
def join():
    joinGroupForm = JoinAGroupForm()
    if request.method=='POST' and joinGroupForm.validate_on_submit():
        token = joinGroupForm.jointoken.data
        test_group = group.query.filter_by(token=token).first()
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

# @groups.route('/admin')
# @login_required
# def admin():
#     groupID = request.args.get('id')
#     test_group = group.query.filter_by(id=groupID).first()
#     if test_group:
#         flash("valid group", '')
#         if current_user in test_group.adminusers:
#             flash("admin", '')
#     else:
#         flash("Invalid group!", 'error')
#     return render_template("group/admin/groupadmin.html", user=current_user)

@groups.route('<group_token>/admin')
@login_required
def manage(group_token):
    thegroup = checkInGroupByTokenAndAdmin(group_token)
    return render_template("group/admin/groupadmin.html", user=current_user, group = thegroup)

@groups.route('<group_token>/admin//assets/create', methods=['GET', 'POST'])
@login_required
def create_asset(group_token):
    thegroup = checkInGroupByTokenAndAdmin(group_token)
    createAssetForm = CreateAssetForm()

    if request.method=='POST' and createAssetForm.validate_on_submit():
        #print(createAssetForm.type.data, flush=True)
        name = createAssetForm.assetname.data
        thetype = createAssetForm.type.data
        asset = assets(asset_name = name, is_activated = True, type = thetype)
        thegroup.assets.append(asset)
        #db.session.add(asset)
        db.session.commit()
        flash("Asset Created", '')
    return render_template("group/admin/createasset.html",token=group_token, user=current_user, form=createAssetForm)

@groups.route('<group_token>/admin/assets', methods=['GET', 'POST'])
@login_required
def assetshome(group_token):
    thegroup = checkInGroupByTokenAndAdmin(group_token)
    return render_template("group/admin/viewassets.html",token=group_token, user=current_user, assets = thegroup.assets)

@groups.route('<group_token>/admin//assets/<asset_name_arg>', methods=['GET', 'POST'])
@login_required
def ViewSingleAsset(group_token, asset_name_arg):
    thegroup = checkInGroupByTokenAndAdmin(group_token)
    
    theasset = assets.query.filter_by(group_id=thegroup.id, asset_name=asset_name_arg).first()
    if not theasset:
        abort(404, "Asset does not exsist")
    print(theasset.id, flush=True)
    return render_template("group/admin/viewsingleasset.html",token=group_token, user=current_user, asset = theasset)

def checkInGroupByTokenAndAdmin(group_token):
    # blocks all management functions if user is not in the specified group
    # returns the group to the caller if the user is in all the admin groups
    test_group = group.query.filter_by(token=group_token).first()
    if not test_group:
        abort(403, description="No such group")
    elif current_user not in test_group.adminusers:
        abort(403, description="You're not an admin user in this group")
    return test_group