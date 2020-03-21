# coding: utf-8
from __future__ import unicode_literals
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g
from flask.ext.login import login_user , logout_user , current_user , login_required
from flask.ext.admin import Admin, BaseView, expose, AdminIndexView
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin

import requests
import os.path as op
from app import app,db
from models import User

from functools import wraps
