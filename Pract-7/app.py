from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def db():
    return mysql.connector.connect(host="localhost", user="root", password="Sakshi@2005", database="Pract_7")

@app.route('/')
def home():
    con=db();cur=con.cursor()
    cur.execute("SELECT * FROM students")
    data=cur.fetchall();con.close()
    return render_template("index.html", students=data)

@app.route('/add',methods=['POST'])
def add():
    n,a,c=request.form['name'],request.form['age'],request.form['course']
    con=db();cur=con.cursor()
    cur.execute("INSERT INTO students(name,age,course) VALUES(%s,%s,%s)",(n,a,c))
    con.commit();con.close()
    return redirect('/')

@app.route('/edit/<int:id>',methods=['POST'])
def edit(id):
    n,a,c=request.form['name'],request.form['age'],request.form['course']
    con=db();cur=con.cursor()
    cur.execute("UPDATE students SET name=%s,age=%s,course=%s WHERE id=%s",(n,a,c,id))
    con.commit();con.close()
    return redirect('/')

@app.route('/del/<int:id>')
def delete(id):
    con=db();cur=con.cursor()
    cur.execute("DELETE FROM students WHERE id=%s",(id,))
    con.commit();con.close()
    return redirect('/')

app.run(debug=True)
