from flask import Flask, request,render_template
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Hoang0907198643@localhost/QuanLyKhachSan?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)