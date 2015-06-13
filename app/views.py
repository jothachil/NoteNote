from flask import Flask, render_template, request, url_for, redirect, flash, session, g
from urllib2 import urlopen
from app import app
from functools import wraps
import sqlite3




# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/', methods=['GET'])
@login_required
def index():
    loginvar = None
    g.db = connect_db()
    cur = g.db.execute('select * from notes')
    posts = [dict(noteid=row[0], note_title=row[1], note_content=row[2]) for row in cur.fetchall()]
    g.db.close()
    if session.get('logged_in') == True:
        loginvar = 1
        print loginvar
    else:
        loginvar = 0
    return render_template('user.html',posts1=posts,passloginvar=loginvar)

@app.route('/addstudent', methods=['POST','GET'])
@login_required
def addstudent():
    error = None
    Null= None

    loginvar = None
    if request.method == 'POST':
        notes_title=request.form['notes_title']
        notes_content=request.form['notes_content']
        g.db = connect_db()
        cur = g.db.execute("insert into notes values (?,?,?)", (Null,notes_title, notes_content))
        g.db.commit()
        g.db.close()
        return redirect(url_for("index"))
    if session.get('logged_in') == True:
        loginvar = 1
        print loginvar
    else:
        loginvar = 0

    return render_template('addstudent.html',passloginvar=loginvar)

@app.route('/login', methods=['POST','GET'])
def login():
    error = None
    loginvar = None
    if request.method == 'POST':
        if request.form['email'] != "admin@gmail.com" or request.form["password"] != "admin":
            error = "INVALID LOGIN"
            print error
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for("index"))
    if session.get('logged_in') == True:
        loginvar = 1
        print loginvar
    else:
        loginvar = 0
    return render_template('login.html',error1=error,passloginvar=loginvar)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))

@app.route('/notes/<noteids>')
@login_required
def deletenote(noteids):
    noteid1=str(noteids)
    g.db = connect_db()
    cur = g.db.execute('DELETE FROM notes WHERE noteid = ?',(noteid1,))
    g.db.commit()
    g.db.close()
    return redirect(url_for("index"))

@app.route('/edits/<noteids>', methods=['POST','GET'])
@login_required
def editnote(noteids):
    noteid1=str(noteids)
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM notes WHERE noteid = ?',(noteid1,))
    edits = [dict(noteid=row[0], note_title=row[1], note_content=row[2]) for row in cur.fetchall()]
    print edits
    loginvar = None
    if request.method == 'POST':
        notes_title=request.form['notes_title']
        notes_content=request.form['notes_content']
        g.db = connect_db()
        cur = g.db.execute("UPDATE notes SET title = ?, content = ? WHERE noteid = ?", (notes_title, notes_content,noteids))
        g.db.commit()
        g.db.close()
        return redirect(url_for("index"))
    g.db.commit()
    g.db.close()
    if session.get('logged_in') == True:
        loginvar = 1
        print loginvar
    else:
        loginvar = 0
    return render_template('edit.html',edits1=edits,passloginvar=loginvar)

def connect_db():
    return sqlite3.connect(app.database)
