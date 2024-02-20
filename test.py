import pymysql
from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import logging

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

def insertToStudentTable(name, age, city, gmail, DOB=None):
    try:
        connectTodb()
        insertquery = "INSERT INTO student (name, age, city, gmail, DOB) VALUES (%s, %s, %s, %s, %s);"
        cur.execute(insertquery, (name, age, city, gmail, DOB))
        con.commit()
        disconnectDB()
        return True
    except Exception as e:
        print(f"Error inserting record: {e}")
        disconnectDB()
        return False

def getOneStudent(Roll_no):
    connectTodb()
    selectquery = "SELECT * FROM student WHERE Roll_no=%s;"
    cur.execute(selectquery,(Roll_no, ))
    data = cur.fetchone()
    disconnectDB()
    return data

def updateStudentToTable(name, age, city, gmail, Roll_no, DOB=None):
    try:
        connectTodb()
        updateQuery = "UPDATE student SET name=%s, age=%s, city=%s, gmail=%s, DOB=%s WHERE Roll_no=%s;"
        cur.execute(updateQuery, (name, age, city, gmail, DOB, Roll_no))
        con.commit()
        disconnectDB()
        return True
    except:
        disconnectDB()
        return False

def deleteStudentFromTable(Roll_no):
    try:
        connectTodb()
        deleteQuery = "DELETE FROM student WHERE Roll_no=%s;"
        cur.execute(deleteQuery, (Roll_no, ))
        con.commit()
        disconnectDB()
        return True
    except:
        disconnectDB()
        return False

@myflask.route("/")
@myflask.route("/index/")
def index():
    data = getAllStudentsData()
    return render_template("index.html", data=data)

@myflask.route("/add/", methods=['GET','POST'])
def addstudent():
    if request.method =="POST":
        data = request.form
        if insertToStudentTable(data['txtname'], data['txtage'], data['txtcity'], data['txtgmail'], data['txtDOB']):
            message="Record inserted successfully"
         
        else:
            message="Due to some issue could't insert record"
        return render_template('insert.html', message=message)
    return render_template("insert.html")

@myflask.route('/edit/', methods=['GET', 'POST'])
def updateStudent():
    Roll_no = request.args.get('rno', type=int, default=1)
    data = getOneStudent(Roll_no) 
    if request.method == "POST":
        fdata = request.form
        print(fdata)
        if updateStudentToTable(Roll_no, fdata['txtname'], fdata['txtage'], fdata['txtcity'], fdata['txtgmail'], fdata['txtDOB']):
            message = "Record updated successfully"
        else:
            message = "Due to some issue couldn't update record"
        return render_template('update.html', message=message)
    return render_template("update.html",data=data)

@myflask.route("/delete/")
def deleteStudent():
    Roll_no=request.args.get('rno',type=int,default=1)
    deleteStudentFromTable(Roll_no)
    return redirect(url_for("index"))

if __name__=="__main__":
    myflask.run(debug=True)