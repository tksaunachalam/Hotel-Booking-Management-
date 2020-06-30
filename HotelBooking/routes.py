import os, random
from flask import render_template, url_for,flash,redirect, request
from HotelBooking import app , db ,bcrypt
from HotelBooking.forms import RegistrationForm, LoginForm, BookingForm, EnquiryForm, ConfirmBooking, AmenityForm
from flask_login import login_user,current_user, logout_user, login_required
from datetime import datetime, date , timedelta
from HotelBooking.models import User,Enquiry, Rooms, Bookings, Cost
from twilio.rest import Client
# for printing pdf
from flask_weasyprint import HTML, render_pdf


account_sid = 'AC73bcc3e50f0dd1dd8364ba3651598f66'
auth_token = 'b183116d7684bf4e9a343bee57eeb151'
client = Client(account_sid, auth_token)


@app.route("/")
@app.route("/home",methods=['GET','POST'])
def hello():
        
        # form=LoginForm()
        enqform = EnquiryForm()
        img1=os.path.join('static','images','image-deluxeroom.jpg')

        #clear old bookings where check_out date is before current date
        current_date = datetime.today()
        bookings = Bookings.query.filter(Bookings.check_out_date < current_date).all()
        for booking in bookings:
            room = Rooms.query.get(booking.r_id)  
            if room:
                if room.r_status == 1:
                    print(f'removing room {room.r_id}')
                    room.r_status = 0 # vacated room
                    db.session.add(room)
                    db.session.delete(booking)  #if you decide to remove the booking record
                    db.session.commit()
            
        if enqform.validate_on_submit():

            enquiry = Enquiry(name= enqform.Name.data,email= enqform.Email.data, msg=enqform.Msg.data)
            db.session.add(enquiry)
            db.session.commit()
            flash(f'Thank You for Reaching Out to Us! We will get Back Shortly', 'success')


        return render_template('home.html',title='Home',image=img1,form1=enqform)

        # return render_template('home.html',title='Home',form = form ,image=img1)



@app.route("/register",methods=['GET','POST'])
def register():
        if current_user.is_authenticated:
                 return redirect(url_for('hello'))
        
        form=RegistrationForm()


        if form.validate_on_submit():
                #print(form.username.data)
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(username= form.username.data,email= form.email.data, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                flash(f'your account has been created', 'success')
                return redirect(url_for('login'))
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
            next_page = request.args.get('next')

            #if user is admin(id=0) redirect to admin page
            if int(current_user.get_id()) == 0:
                return redirect('/admin')

            return redirect(next_page) if next_page else redirect(url_for('hello') )

        else:
            flash('login unsuccesful plz check username and password','danger')

    return render_template('login.html ', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('hello'))

@app.route("/about")
def about():
    return render_template('about.html',title='About')


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    enqform = EnquiryForm()
    if enqform.validate_on_submit():
        enquiry = Enquiry(name= enqform.Name.data,email= enqform.Email.data, msg=enqform.Msg.data)
        db.session.add(enquiry)
        db.session.commit()
        flash(f'Thank You for Reaching Out to Us! We will get Back Shortly', 'success')
    
    return render_template('contact.html', title='Contact Us',form1=enqform)


#global variable which contains the details for the search query given by the user  
search_input ={
    "check_in_date":"",
    "check_out_date":"",
    "capacity":0
}
@app.route("/booknow",methods=['GET','POST'])
@login_required
def booking():
        print('hello idiots')
        form=BookingForm()
        img1=os.path.join('static','images','image-deluxeroom.jpg')
        print(type(form))   
        if form.is_submitted():

            #searchform = form
            print(form.CheckIn.data)
            print(form.CheckOut.data)
            print(form.Adults.data)
            print(form.Kids.data)
            search_input['check_in_date'] = datetime.strptime(form.CheckIn.data, '%d-%m-%Y')
            search_input['check_out_date'] = datetime.strptime(form.CheckOut.data, '%d-%m-%Y')
            search_input['capacity'] = int(form.Kids.data) + int(form.Adults.data)
            

            #flash('Available','success')
            return redirect(url_for('rooms'))
            
        #flash(f'check in date{form.CheckIn}')
    
        return render_template('booknow.html',title='BookNow',form = form ,image=img1)

@app.route("/rooms",methods=['GET','POST'])
@login_required
def rooms():

    
    rooms = Rooms.query.all()
    costs = Cost.query.all()
    # print(search_input['capacity'])
    # print(type(search_input['check_in_date']))
    if rooms :

        return render_template('rooms.html', rooms=rooms, costs = costs, search_input = search_input, Cost = Cost)
    else:
        msg = 'No rooms available currently'
        return render_template('rooms.html', msg=msg)


@app.route("/bookings/<string:id>", methods=['GET', 'POST'])
@login_required
def bookings(id):

    global b_id, amount
    #booking id
    b_id = random.randint(1000, 10000)
    # if current_user.is_authenticated:
        #the user id of the current user logged in who is making the booking
    u_id = current_user.get_id()
    check_in = search_input['check_in_date']
    check_out = search_input['check_out_date']
    if check_in =='' and check_out =='':
        return redirect(url_for('booking'))
    else:
        no_of_days = check_out - check_in
        no_of_days = no_of_days.days
     
    room = Rooms.query.get(id)
    room_type = room.r_type + ' room'    
    amount = Cost.query.filter_by(item=room_type).first().price  #retreiving the cost for the selected room type 
    amount = amount * no_of_days
    cnform = ConfirmBooking()   #confirmation form
    amenities_form = AmenityForm()

    if cnform.Submit.data and not check_in:
        flash('Enter the details','warning')
        return redirect(url_for('booking'))
     
    if cnform.Submit.data and check_in:
        
        print(amenities_form.Amenities.data)
        print(cnform.ModeOfPayment.data)

        booking = Bookings(b_id= b_id, u_id= u_id,r_id= id, payment_mode= cnform.ModeOfPayment.data, check_in_date= check_in, check_out_date=check_out)
     
        msg='Your Booking Has Been Confirmed!'
    #un comment the follwing lines ,this is just for testing
        room.r_status = 1 #booked
        db.session.add(booking)
        db.session.add(room)
        db.session.commit()
        #to clear the request made by the user 
        check_in = None
        search_input["check_in_date"]=None

        # message = client.messages \
        #         .create(
        #              body="Your Booking is confirmed!!We are eager to serve you",
        #              from_='+12015844162',
        #              to='+917550221044'
        #          )
        # print(message.sid)

        flash(f'{msg} Booking Id {b_id}','success')
        return redirect(url_for('printbill', id=b_id))
    
    if cnform.Cancel.data:
        
        return redirect(url_for('hello'))
        
    return render_template('confirmbooking.html',title="Confirm Booking", form=cnform, amn_form = amenities_form, room=room, check_in=check_in.date(), check_out=check_out.date(), amount=amount)

@app.route("/mybookings", methods=['GET', 'POST'])
@login_required
def mybookings():
    u_id = current_user.get_id()
    current_date  = date.today() #current date 
    cancel_deadline = timedelta(days = 2)  #can cancel 2 days before checkin
    allbookings = Bookings.query.filter_by(u_id= u_id).all()
    return render_template('mybookings.html', title="MyBookings", bookings = allbookings, current_date = current_date, cancel_deadline = cancel_deadline)

@app.route("/cancel/<string:id>", methods=['GET', 'POST'])
@login_required
def cancel(id):
    u_id = current_user.get_id()

    booking = Bookings.query.get(id)
    r_id = booking.r_id
    room = Rooms.query.get(r_id) 
    db.session.delete(booking)
    room.r_status = 0 #available 
    db.session.add(room)
    db.session.commit()
    msg='Your Booking has been cancelled'
    flash(msg,'danger')
    return redirect(url_for('hello'))

    return render_template('dummy.html')

@app.route("/printbill/<string:id>", methods=['GET', 'POST'])
#@login_required
def printbill(id):
    u_id = current_user.get_id()
    email = User.query.get(u_id).email
    username = User.query.get(u_id).username
    booking = Bookings.query.get(id)   #here b_id is global var
    r_id = booking.r_id
    check_in = booking.check_in_date
    check_out = booking.check_out_date
    mode_of_payment = booking.payment_mode
    r_type = Rooms.query.get(r_id).r_type
    current_date  = date.today()
    
    room_type = r_type + ' room'    
    no_of_days = (check_out - check_in).days
    cost = Cost.query.filter_by(item=room_type).first().price  #retreiving the cost for the selected room type 
    cost = cost * no_of_days

    html = render_template('invoice.html', title='Bill', username=username, email=email, b_id=id, r_type=r_type, cost=cost, mode_of_payment=mode_of_payment, booking_date=current_date, check_in = check_in, check_out= check_out)
    
    #uncomment following to print pdf    
    if request.method == 'POST' and request.form['submit']=='submit':
        return render_pdf(HTML(string=html))


    return html
    #return render_template('invoice.html', title='Bill', username=username, email=email, b_id=b_id, r_type=r_type, cost=amount, mode_of_payment=mode_of_payment, booking_date=current_date, check_in = check_in, check_out= check_out, html=html)

