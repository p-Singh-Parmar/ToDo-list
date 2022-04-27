import datetime
from datetime import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# WSGI application is the standard for communicating between the web server and the web aplication
app=Flask(__name__)  # creating the object of flask; this is our WSGI application which wil be interacting; basically a standard for communicating with the sever

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False   # one time thing to avoid unneccessary warnings
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)  # nullable=False means this field cannot be left null
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)  # search web for utcnow

    def _repr_(self):  # repr method shows given statement when its object is called
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])   # creating a DECORATOR; takes 2 parameters: rule and options; rule is a str value which has the specified url
# this means whenever we're going to this url the below url is going to be activated  # POST and GET for getting the input from the html page
def hello_world():
    if request.method == 'POST':
        # print("hello")   # if our post request is going successfully then it'll print this hello
        title = request.form['title']
        desc = request.form['desc']

        todo=Todo(title=title, desc=desc)  # creating an instance of Todo whenever someone comes to my homepage
        db.session.add(todo)   # for adding that todo to the session or page
        db.session.commit()

    # to display all records; I'm gonna use a special syntax which won't be html, it will be Jinja2; 
    # Jinja2 is a Templating Engine and it is helpful when we make python apps and we pass any variable
    allTodo=Todo.query.all()   # this is to print all todos in the terminal
    #print(allTodo)
    return render_template('index.html', allTodo=allTodo) # passing this allTodo variable to index.html

@app.route('/show')
def product_page():
    allTodo=Todo.query.all()   # this is to print all todos in the terminal
    print(allTodo)
    return 'This is Products Page'

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()  # this is to get the firstr record with the passed sno
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['POST', 'GET'])
def update(sno):
    if request.method == 'POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')    # redirecting the main page after updation

    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


# Building Url dynamically
@ app.route('/success/<int:score>')  #since score passed here is an integer; if string passed, no need to write anything
def success(score):
    return 'The person has passed and the marks he obtained is'+ str(score)
    
if __name__== "__main__":
    app.run(debug=True)   # to change deffault port number port=number; debug=True automatically refreshes the server when Saved.

