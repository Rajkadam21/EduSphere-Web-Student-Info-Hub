import pymysql
from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL

con = None
cur = None

myflask=Flask(__name__)

def connectTodb():
    global con,cur
    con=pymysql.connect(host="localhost",user="root",password="",database="project")
    cur=con.cursor()

def disconnectDB():
    cur.close()
    con.close()

def getAllStudentsData():
    connectTodb()
    selectquery = "SELECT * FROM student;"
    cur.execute(selectquery)
    data = cur.fetchall()
    disconnectDB()
    return data

def insertToStudentTable(name,rno,DOB):
    try:
        connectTodb()
        insertquery = "Insert INTO student (name,rno,DOB) values (%s,%s,%s);"
        cur.execute(insertquery, (name,rno,DOB))
        con.commit()
        disconnectDB()
        return True
    except:
        disconnectDB()
        return False

def getOneStudent(rno):
    connectTodb()
    selectquery = "SELECT * FROM student WHERE rno=%s;"
    cur.execute(selectquery,(rno, ))
    data = cur.fetchone()
    disconnectDB()
    return data

def updateStudentToTable(name,rno,DOB=None):
    try:
        connectTodb()
        updateQuery = "UPDATE student SET name=%s, DOB=%s WHERE rno=%s;"
        cur.execute(updateQuery, (name,rno,DOB))
        print(name,rno,DOB)
        con.commit()
        disconnectDB()
        return True
    except:
        disconnectDB()
        return False

def deleteStudentFromTable(rno):
    try:
        connectTodb()
        deleteQuery = "DELETE FROM student WHERE rno=%s;"
        cur.execute(deleteQuery, (rno, ))
        con.commit()
        disconnectDB()
        return True
    except:
        disconnectDB()
        return False

@myflask.route("/")
@myflask.route("/index/")
def index():
    if request.method=="GET":
        data = getAllStudentsData()
        return render_template("index.html", data=data)
    return render_template("index.html")

@myflask.route("/add/", methods=['GET','POST'])
def addstudent():
    if request.method =="POST":
        data = request.form
        if insertToStudentTable(data['txtname'], data['txtrno'], data['txtDOB']):
         message="Record inserted successfully"
        else:
         message="Due to some issue could't insert record"
        return render_template('insert.html', message=message)
    return render_template("insert.html")

@myflask.route('/edit/', methods=['GET', 'POST'])
def updateStudent():
    rno = request.args.get("rno", type=int, default=1)
    data = getOneStudent(rno)

    if request.method == "POST":
        name = request.form.get('txtname')
        dob = request.form.get('txtDOB')
        
        if updateStudentToTable(name, rno, dob):
            message = "Record updated successfully"
        else:
            message = "Due to some issue couldn't update record"
        return render_template('update.html', message=message, data=data)

    return render_template("update.html", data=data)

@myflask.route("/delete/")
def deleteStudent():
    rno=request.args.get('rno',type=int,default=1)
    deleteStudentFromTable(rno)
    return redirect(url_for("index"))

if __name__=="__main__":
    myflask.run(debug=True)