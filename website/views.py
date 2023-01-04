import base64
import re
from types import new_class
from werkzeug.security import generate_password_hash,check_password_hash
from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for
from .import db 
from .models import User,Data
import io

views =Blueprint('views',__name__)
curuser = 0
@views.route("/login",methods=['GET','POST'])
def login():
        if request.method == 'POST':
              username = request.form.get('username')
              password = request.form.get('password')
              from .models import User
              user =User.query.filter_by(username=username).first()
              if user:
                    if user.password==password:
                        flash('login')
                        global curuser
                        curuser=user
                        return redirect(url_for('views.home'))
                    else:
                        flash("incorrect")
              else:
                   flash('user data does not have')
        return render_template("login.html",user=curuser)
@views.route('/logout',methods=['GET','POST'])
def logout():
    global curuser
    curuser =0
    flash('logout')
    return redirect(url_for('views.login'))

@views.route('/getinfo',methods=['GET','POST'])
def getinfo():
    if(request.method=='POST'):
        cusid=request.form.get('cusid')
        new_data =Data.query.filter_by(cusid=cusid).first()
        if new_data:
            return redirect(f'/payment/{cusid}')
        else:
            return f"Employee with cusid ={cusid} Doenst exist"
    return render_template('get.html')


@views.route('/signup',methods=['GET','POST'])
def sign_up():
    if request.method =='POST':
        email =request.form.get('email')
        username=request.form.get('uname')
        firstname =request.form.get('fname')
        lastname=request.form.get('lname')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        from .models import User
        user=User.query.filter_by(email=email).first()
        if user:
            flash("alredy")
            print("already")

        elif password1 !=password2:
            flash("password does not match")
        else:
            from .import db 
            new_user =User(username=username,firstname=firstname,email=email,password=password1,lastname=lastname,user_type="test")
            db.session.add(new_user)
            db.session.commit()
            flash("signup")
            return render_template("login.html")
    return render_template("signup.html",user=curuser)

@views.route('/home' ,methods=['GET','POST'])
def home():
    sites = [0]
    if(request.method =='POST'):
        d=request.form.get('val')
        c=request.form.get('pre')
        d=int(d)
        c=int(c)
        a=d-c
        if(a<0):
            a="current should be greater than previous"

        elif(a<=100):
            a="free"
        
        elif(a>100 and a<=200):
            b=a-100
            a=(a*2.5)

        

        elif(a>200 and a<=350):
            b=a-100
            a=(a*2.5)
        
        elif(a>350 and a<=500):
            b=a-100
            a=b*5
        
        else:
            b=a-100
            a=(b*7)
        
        sites = [a]
        
        return render_template("home.html",sites=sites)

        return render_template("home.html", sites=sites)

    if curuser != 0:
        return render_template('home.html',sites=sites)
    else:
        return redirect(url_for('views.login'))


@views.route('/data',methods=['GET','POST'])
def data():
    if request.method =='POST':
        cusid=request.form.get('cusid')
        username=request.form.get('uname')
        firstname =request.form.get('fname')
        address=request.form.get('address')
        amount=request.form.get('amount')
        houseno=request.form.get('houseno')

        from .models import Data
        data=Data.query.filter_by(cusid=cusid).first()
        if data:
            flash("alredy")
            print("already")
        
        else:
            from .import db 
            data =Data(cusid=cusid,username=username,firstname=firstname,houseno=houseno,address=address,amount=amount)
            db.session.add(data)
            db.session.commit()
            flash("add")
    return render_template("add.html")
@views.route('/data/<string:cusid>')
def RetrieveSingleEmployee(cusid):
    new_data =Data.query.filter_by(cusid=cusid).first()
    if new_data:
         return render_template('data.html', employee = new_data)
    return f"Employee with cusid ={cusid} Doenst exist"

@views.route('/payment/<string:cusid>')
def pay(cusid):
    new_data =Data.query.filter_by(cusid=cusid).first()
    return render_template('payment.html',new_data=new_data)