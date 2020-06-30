from HotelBooking import db, login_manager, admin
from datetime import datetime
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)  
    image_file = db.Column(db.String(20), default='default.jpg')  
    password = db.Column(db.String(60), nullable=False) 
 
    def __repr__(self):
        return f"User('{self.id}', '{self.username}',  '{self.email}', '{self.image_file}')"


class Enquiry(db.Model):
    name = db.Column(db.String(20),primary_key=True,unique=False, nullable=False)
    email  = db.Column(db.String(20),unique=False, nullable=False)
    msg  =  db.Column(db.String(20),unique=False, nullable=False)

class Rooms(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    r_no = db.Column(db.Integer, unique=True)
    r_type =  db.Column(db.String(20))
    r_capacity = db.Column(db.Integer)
    r_status = db.Column(db.Boolean)   #1 if booked
    
    def __repr__(self):
        return f"Rooms('{self.r_id}',  '{self.r_no}', '{self.r_type}',{self.r_status})"



class Bookings(db.Model):
    b_id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('user'))

    r_id = db.Column(db.Integer, db.ForeignKey('rooms.r_id'), nullable=False)
    rooms = db.relationship('Rooms', backref=db.backref('rooms'))
    
    payment_mode = db.Column(db.String(20),unique=False, nullable=False)
    check_in_date = db.Column(db.DateTime, nullable=False)
    check_out_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Bookings('{self.b_id}',  '{self.u_id}', '{self.r_id}')"

class Cost(db.Model):
    code = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.String(20), unique=False)
    price = db.Column(db.Integer, nullable = False )

    def __repr__(self):
        return f"Cost('{self.code}','{self.item}','{self.price}')"

class MyModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and int(current_user.get_id())==0)


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Enquiry, db.session))
admin.add_view(MyModelView(Rooms, db.session))
admin.add_view(MyModelView(Bookings, db.session))
admin.add_view(MyModelView(Cost, db.session))


# class BookedRooms(db.Model):

#     r_id = db.Column(db.Integer, db.ForeignKey('rooms.r_id'), nullable=False)
#     rooms = db.relationship('Rooms', backref=db.backref('rooms'))

#     b_id = db.Column(db.Integer, primary_key=True)
#     bookings = db.relationship('Bookings', backref=db.backref('Bookings'))

#     u_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     user = db.relationship('User', backref=db.backref('user'))

#     check_in_date = db.Column(db.DateTime, nullable=False)
#     check_out_date = db.Column(db.DateTime, nullable=False)
