from flask import Flask,render_template,url_for,request,redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime
#from flask_script import Manager
#from flask_migrate import Migrate, MigrateCommand


app=Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT']=3000
app.config['MYSQL_PASSWORD'] = 'nivedita@24'
app.config['MYSQL_DB'] = 'bank'
mysql = MySQL(app)

#migrate = Migrate(app, db)
#manager = Manager(app)
#manager.add_command('db', MigrateCommand)


@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/add',methods=['GET','POST'])
def create_acc():
    if request.method=='POST':
        form=request.form
        email=request.form['email']
        name=request.form['name']
        dob=request.form['dob']
        accno=request.form['accno']
        amt=request.form['amt']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE accountno = %s', (accno,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists'
            alert=0
        else:
            cursor.execute('INSERT INTO users(name,email,dob,accountno,accbal) VALUES(%s,%s,%s,%s,%s)',(name,email,dob,accno,int(amt)))
            mysql.connection.commit()
            msg='Succesfully registered!'
            alert=1
        return render_template('create.html',msg=msg,alert=alert,em=email,nm=name,dob=dob,accno=accno,amt=amt)
    else:
        return render_template('create.html')

@app.route('/all',methods=['GET'])
def detail():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users')
    users=cursor.fetchall()
    return render_template('details.html',users=users)

@app.route('/transfer',methods=['GET','POST'])
def transfer():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users')
        users=cursor.fetchall()
        if request.method=='POST':
            frm=request.form['from']
            to=request.form['to']
            amt=request.form['amtf']
            for user in users:
                if frm==user['accountno']:
                    cursor.execute('UPDATE users SET accbal=accbal-%s WHERE accountno=%s',(int(amt),frm))
                    cursor.execute('UPDATE users SET accbal=accbal+%s WHERE accountno=%s',(int(amt),to))
                    mysql.connection.commit()
                    return render_template('success.html')
            return render_template('transfer.html',msg="Account does not exist")
        else:
            return render_template('transfer.html',users=users) 
    except:
        return 'Something went wrong'


@app.route('/checkbal',methods=['GET','POST'])
def checkbal():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users')
    users=cursor.fetchall()
    if request.method=='POST':
        accno=request.form['accno']
        for user in users:
            if accno==user["accountno"]:
                return render_template('check.html',accountno=user['accountno'],bal=user['accbal'])
        return render_template('check.html',msg='Account does not exist')
        
    else:
        return render_template('check.html')

if __name__=="__main__":
    app.run(debug=True)