from flask import Flask, render_template, url_for,flash,redirect
from flask_login import login_user,current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from datetime import datetime


import os


app = Flask(__name__)

app.config['SECRET_KEY']='4a242afdbbddf3207bf448f3d1eee530'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'    
login_manager.login_message_category = 'info'    






class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)  
    image_file = db.Column(db.String(20), default='default.jpg')  
    password = db.Column(db.String(60), nullable=False) 
    posts = db.relationship('Post', backref='author', lazy=True) 
 
    def __repr__(self):
        return f"User('{self.username}',  '{self.email}', '{self.image_file}')"



from forms import RegistrationForm,LoginForm,BookingForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@app.route("/home",methods=['GET','POST'])
def hello():
        # form=LoginForm()
        img1=os.path.join('static','images','image-deluxeroom.jpg')
        return render_template('home.html',title='Home',image=img1)

        # return render_template('home.html',title='Home',form = form ,image=img1)



@app.route("/register",methods=['GET','POST'])
def register():
        if current_user.is_authenticated:
                 return redirect(url_for('hello'))
        
        form=RegistrationForm()
        print(form.username.data)

        # if form.validate_on_submit():
        #         #print(form.username.data)
        #         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #         user = User(username= form.username.data,email= form.email.data, password=hashed_password)
        #         db.session.add(user)
        #         db.session.commit()
        #         flash(f'your account has been created', 'success')
        #         return redirect(url_for('login'))
        return render_template('register.html',title='Register',form=form)


@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('hello') )

        else:
            flash('login unsuccesful plz check username and password','danger')

    return render_template('login.html ', title='Login', form=form)

@app.route("/booking",methods=['GET','POST'])
def booking():
        print('hello idiots')
        form=BookingForm()
        img1=os.path.join('static','images','image-deluxeroom.jpg')
        #print(form.CheckIn.data)
        if form.is_submitted():
            print(form.CheckIn.data)
            print(form.CheckOut.data)
            print(form.Adults.data)
            print(form.Kids.data)

            

        #flash(f'check in date{form.CheckIn}')
    
        return render_template('booking.html',title='booking',form = form ,image=img1)






if __name__ == '__main__':
    app.run(debug=True)
