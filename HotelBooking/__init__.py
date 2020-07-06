from flask import Flask
#from flask_login import login_user,current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from datetime import datetime
from flask_login import LoginManager
from flask_admin import Admin
import pymysql


app = Flask(__name__)

app.config['SECRET_KEY']='4a242afdbbddf3207bf448f3d1eee530'
#sqslite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#for mysql 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@localhost:3307/hotelbooking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['FLASK_ADMIN_SWATCH'] = 'Darkly'
admin = Admin(app, name='TksHotel', template_mode='bootstrap3')



db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'    
login_manager.login_message_category = 'info'  


#twillo api token
sid = 'AC73bcc3e50f0dd1dd8364ba3651598f66'
token = 'c06d36c5122d6833906d69b8dbc421'
token = token + '2b'

from HotelBooking import routes