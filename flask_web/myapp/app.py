from flask import  Flask, render_template, url_for,request,redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

#Init app
app = Flask(__name__)



#Database
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:/// test.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

#Init Db
db = SQLAlchemy(app)

class Todo(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Integer, default=0)
    date_created =db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<task %r>' %self.id 
    

@app.route('/',methods=['POST','GET'])
def index():
    
    if request.method == 'POST':
        task_content = request.form['content']

        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an issue adding your task'
            
    else: 
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('home.html', task=tasks)

@app.route('/delete/<int:id>')

#Deleting Task from DB

def delete(id):
    task_to_delete = Todo.query.get_or_404(id)


    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'Ther was error in deleting that task'

#Updating tha Task in DB
@app.route('/update/<int:id>', methods=['GET','POST']) 
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except :
            return 'There was error during the update'

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run( debug=True)
    
    