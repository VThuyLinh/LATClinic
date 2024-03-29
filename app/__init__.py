from urllib.parse import quote
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = "ABCDEFGHIJLKMNOPQRSTUVWXYZ@#$%^^^^&&&"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/latclinic?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 2

db = SQLAlchemy(app=app)
login = LoginManager(app=app)

import cloudinary

cloudinary.config(
    cloud_name="djyvckpo5",
    api_key="915431415142768",
    api_secret="***************************"
)


