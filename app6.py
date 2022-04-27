from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app6=Flask(__name__)
app6.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app6.config['SQLALCHEMY_DATABASE_URI']='sqlite:///new.db'
db=SQLAlchemy(app6)

class ExampleTable(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(300))
    data=db.Column(db.LargeBinary)   # for converting the binary file into blob file in dataset

@app6.route('/')
def pdf():
    return render_template('upload.html')

@app6.route('/upload', methods=['POST'])
def upload():
    # to get the file from the request
    file =request.files['inputFile']

    newFile= ExampleTable(name=file.filename, data=file.read())
    db.session.add(newFile)
    db.session.commit()


    return 'Saved ' + file.filename + ' to the database!'

if __name__=='__main__':
    app6.run(debug=True)