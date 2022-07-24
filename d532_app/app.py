#connect Steps

#download zip
#extract zip to C: Users/ "user"
#uninstall python
#reinstall new Python
#checkmark pip path before confirming installation
#make sure environment systems has correct path set "Python310/Scripts"

#open visual studio code
#open folder from users
#ctr ~
#pip install virtualenv
#py -m virtualenv env
#check to make sure you are in cmd not bash
#env\Scripts\activate
#pip install flask flask-sqlalchemy
#type deactivate when done

#then install visual studio code Python extension

#TO CREATE THE test.db:
#cd D532_app
#py
#from app import db
#db.create_all()
#exit()

#TO UPDATE HEROKU SERVER
#git add .
#git commit -m ""
#git push heroku master

#https://flask.palletsprojects.com/en/2.1.x/patterns/sqlite3/
#or search how to connect flask app to SQLite db

from flask import Flask, redirect, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_side.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#@app.before_first_request
#def create_tables():
    #db.create_all()

db = SQLAlchemy(app)


class Todo(db.Model):
    #contents will become movie.db title column
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    #we can just query for LIKE "Like" in the rating column instead of using booleans
    rating = db.Column(db.String(10), nullable=False)
    genre = db.Column(db.String(15), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        movie_content = request.form['content']
        try:
            movie_rating = request.form['rating']
        except:
            movie_rating = 'Disliked'

        try:
            movie_genre = request.form['genre']
        except:
            movie_genre = 'N/A'

        new_movie = Todo(content=movie_content, rating=movie_rating, genre=movie_genre)
        

        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error while adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    movie_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the movie rating'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            task.rating = request.form['rating']
        except:
            task.rating = 'Disliked'
        try:
            task.genre = request.form['genre']
        except:
            task.genre = 'N/A'
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating the movie rating'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)



##http://127.0.0.1:5000/