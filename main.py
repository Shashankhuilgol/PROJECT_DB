from flask import Flask,render_template,request,session,redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,LoginManager,login_manager
from flask_login import login_required,current_user
#from socket import socket


#db connection
local_server=True
app= Flask(__name__)
app.secret_key='nbk'


#for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





#app.config['SQLALCHY_DATABASE_URI']='mysql://username:passwaord@locakhost/database_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/cr6 automation'
db=SQLAlchemy(app)


#app = Flask(__name__)

#creating db modle i.e tables
class Dept(db.Model):
    dno=db.Column(db.Integer(),primary_key=True)
    dname=db.Column(db.String(100))

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))


class Room(db.Model):
    rno=db.Column(db.String(50),primary_key=True)
    dno=db.Column(db.Integer())


class Item(db.Model):
    item_id=db.Column(db.String(50),primary_key=True)
    item_name=db.Column(db.String(100))
    rno=db.Column(db.String(50))



class Movement(db.Model):
    item_id=db.Column(db.String(50),primary_key=True)
    from_rno=db.Column(db.String(50))
    to_rno=db.Column(db.String(50))

class Category(db.Model):
    item_name=db.Column(db.String(50),primary_key=True)


class Vender(db.Model):
    vid=db.Column(db.String(50),primary_key=True)
    name=db.Column(db.String(50))
    billing=db.Column(db.String(1000))

class Logs(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    item_id=db.Column(db.String(50))
    action=db.Column(db.String(50))
    cdate=db.Column(db.String(50))

#passing end points and run the functions 

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home',methods=['POST','GET'])
@login_required
def home():
    query=db.engine.execute(f"SELECT * FROM `category`;")
    return render_template('item.html',query=query)

@app.route('/cat',methods=['POST','GET'])
@login_required
def cat():
    if request.method=="POST":
        item=request.form.get('item')
        query=db.engine.execute(f"INSERT INTO `category`(`item_name`) VALUES ('{item}');")
        flash(item+" added","warning")
        return redirect(url_for('home'))
    return render_template('item.html')



@app.route('/movement',methods=['POST','GET'])
def movement():
    if request.method=="POST":
        item=request.form.get('item')
        frno=request.form.get('frno')
        trno=request.form.get('trno')
        if trno =="scrap":
            query=db.engine.execute(f"DELETE FROM `item` WHERE `item_id`='{item}';")
            flash(item+" deleted","warning")
            return redirect(url_for('home'))
        query=db.engine.execute(f"UPDATE `item` SET `rno`= '{trno}' WHERE `item_id`='{item}';")
        query=db.engine.execute(f"INSERT INTO `movement`(`item_id`, `from_rno`, `to_rno`) VALUES('{item}','{frno}','{trno}')")
        cquery=db.engine.execute(f"SELECT * FROM `category`;")
        flash(item+" moved from room "+frno+" to room "+trno,"warning")
        return render_template('item.html',query=cquery)
    
    return render_template('movement.html')

@app.route('/movement1',methods=['POST','GET'])
def movement1():
    query=db.engine.execute(f"SELECT * FROM `movement`;")
    return render_template('movement1.html',query=query)



@app.route('/dept',methods=['POST','GET'])
@login_required
def dept():
    query0=db.engine.execute(f"SELECT * FROM `room`WHERE `rno`!='scrap' ;")
    query1=db.engine.execute(f"SELECT i.item_id,i.rno FROM item i, dept d,room r where d.dno=r.dno AND i.rno=r.rno AND d.dname='ISE' ORDER BY i.item_id;;")
    query2=db.engine.execute(f"SELECT i.item_id,i.rno FROM item i, dept d,room r where d.dno=r.dno AND i.rno=r.rno AND d.dname='ISE' ORDER BY i.item_id;;")
    query3=db.engine.execute(f"SELECT * FROM `room`;")
    if request.method=="POST":
        name=request.form.get('dept')
        if name=='ISE':
            query0=db.engine.execute(f"SELECT * FROM `room`WHERE `rno`!='scrap' ;")
            query1=db.engine.execute(f"SELECT i.item_id,i.rno FROM item i, dept d,room r where d.dno=r.dno AND i.rno=r.rno AND d.dname='{name}' ORDER BY i.item_id;;")
            query2=db.engine.execute(f"SELECT i.item_id,i.rno FROM item i, dept d,room r where d.dno=r.dno AND i.rno=r.rno AND d.dname='{name}' ORDER BY i.item_id;;")
            query3=db.engine.execute(f"SELECT * FROM `room`;")
            return render_template('dept.html',query=[query0,query1,query2,query3])

        elif name.lower()=='cse':
            query=db.engine.execute(f"SELECT i.item_id,i.rno FROM item i, dept d,room r where d.dno=r.dno AND i.rno=r.rno AND d.dname='{name}' ORDER BY i.item_id;;")
            return render_template('dept.html',query=query)
        elif name.lower()=='ece':
            query=db.engine.execute(f"SELECT i.item_id,i.rno FROM item i, dept d,room r where d.dno=r.dno AND i.rno=r.rno AND d.dname='{name}' ORDER BY i.item_id;;")
            return render_template('dept.html',query=query)
        else:
            flash("Invalid dept","deanger")

        flash(name,"danger")
    return render_template('dept.html',query=[query0,query1,query2,query3])


@app.route('/out',methods=['POST','GET'])
@login_required
def out():
    query0=db.engine.execute(f"SELECT * FROM `room` WHERE `rno`!='scrap';")
    query3=db.engine.execute(f"SELECT `dno` FROM `room` WHERE `rno`!='scrap';")
    if request.method=="POST":
        rno=request.form.get('rno')
        query1=db.engine.execute(f"SELECT * FROM `room` WHERE `rno`!='scrap';")
        query2=db.engine.execute(f"SELECT i.item_id,i.item_name,i.rno,d.dname FROM item i, dept d,room r where d.dno=r.dno AND i.rno=r.rno AND i.rno='{rno}' ORDER BY i.item_id;")
        return render_template('out.html',query=[query1,query2])
    return render_template('out.html',query=[query0,query3])



@app.route('/item',methods=['POST','GET'])
@login_required
def item():
    if request.method=="POST":
        name=request.form.get('dept')
        cquery=db.engine.execute(f"SELECT * FROM `category`;")
        rquery=db.engine.execute(f"SELECT * FROM `room` WHERE `rno`!='scrap';")
        vquery=db.engine.execute(f"SELECT * FROM `vender`;")
        if name.lower()=='ise':
            return render_template('ise.html',query=[cquery,rquery,vquery])
        elif name.lower()=='cse':
            return render_template('cse.html')
        elif name.lower()=='ece':
            return render_template('ece.html')
        else:
            flash("Invalid dept","deanger")

        flash(name,"warning")

    return render_template('item.html')



@app.route('/ise',methods=['POST','GET'])
@login_required
def ise():
    if request.method=="POST":
            dept=request.form.get('dept')
            itemm=request.form.get('item')
            rno=request.form.get('rno')
            vid=request.form.get('vid')
            
            x=Item.query.filter_by(item_name=itemm).count()
            x=x+1
            if x<10:
                item="MITM/"+dept+"/"+rno+"/"+itemm+"00"
            elif x>=10 and x<100:
                item="MITM/"+dept+"/"+rno+"/"+itemm+"0"
            else:
                item="MITM/"+dept+"/"+rno+"/"+itemm
            x=str(x)

            itemid=item+x

            quer=db.engine.execute(f"INSERT INTO `item`(`item_id`, `item_name`, `rno`, `vid`) VALUES('{itemid}','{itemm}','{rno}','{vid}');")
            query=db.engine.execute(f"SELECT * FROM `category`;")
            flash(itemm+" added succesfully","warning")
            return render_template('item.html',query=query)


    return render_template('ise.html')




@app.route('/sign in',methods=['POST','GET'])
def signin():
    if request.method=="POST":
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Alredy exists","warning")
            return render_template('signin.html')
        encpass=generate_password_hash(password)

        newuser=db.engine.execute(f"INSERT INTO `user` (`name`,`email`,`password`) VALUES ('{name}','{email}','{encpass}')")
        flash("Sign in Success Please Login","sucess")
        return render_template('login.html')


    return render_template('signin.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        #name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            query=query=db.engine.execute(f"SELECT * FROM `category`;")
            return render_template('item.html',query=query)
        else:
            flash("Invalid User Id or password","danger")
            return render_template('login.html')
    return render_template('login.html')


@app.route('/log')
@login_required
def log():
    query=db.engine.execute(f"SELECT * FROM `logs`;")
    return render_template('logs.html',query=query)

@app.route('/van',methods=['POST','GET'])
@login_required
def van():
    query=db.engine.execute(f"SELECT * FROM `vender`;")
    if request.method=="POST":
        vid=request.form.get('vid')
        vname=request.form.get('vname')
        query=db.engine.execute(f"INSERT INTO `vender`(`vid`, `name`, `billing`) VALUES ('{vid}','{vname}','NULL');")
        flash(" new vendor added","warning")
        query1=db.engine.execute(f"SELECT * FROM `vender`;")
        return render_template('vender.html',query=query1)
    return render_template('vender.html',query=query)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successful","warning")
    return redirect(url_for('login'))


@app.route('/test')
def test():
    # a=Dept.query.all()
    # print(a)
    # return render_template('index.html')
    try:
        Dept.query.all()
        return 'Database connected'
    except:
        return 'Database not connected'

app.run(host='127.0.0.1',port=8080,debug=True)

