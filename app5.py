from flask import Flask, render_template, request
# including request because file is going to be included in the request object
from flask_sqlalchemy import SQLAlchemy

app5 =Flask(__name__)
app5.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app5.config['SQLALCHEMY_DATABASE_URI']='sqlite:///exmple123.db'
db=SQLAlchemy(app5)

# creating a class to represent the table in the database that will hold files
class filecontent(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(300))
    data=db.Column(db.LargeBinary)   # for converting the binary file into blob file in dataset

@app5.route('/')
def pdf():
    return render_template('upload.html')

@app5.route('/upload', methods=['POST'])
def upload():
    # to get the file from the request
    file =request.files['inputFile']

    newFile= filecontent(name=file.filename, data=file.read())
    db.session.add(newFile)
    db.session.commit()


    return 'Saved' + file.filename + 'to the database!'

if __name__=='__main__':
    app5.run(debug=True)