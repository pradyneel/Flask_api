#Importing libraries
from flask import Flask, request, Response, jsonify, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
import os
import urllib.request
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps

#Upload Folder
UPLOAD_FOLDER = './uploads'

#Creating instance of the flask app
app = Flask(__name__)

#Configure key for JWT
app.config['SECRET_KEY'] = 'yoursecretkey'

#Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# #File conditions
# app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
