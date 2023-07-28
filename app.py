from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# initialize the app with the extension
db.init_app(app)


class Todo(db.Model):
    sno= db.Column(db.Integer, primary_key= True)
    title= db.Column(db.String(200), nullable= False)
    Desc= db.Column(db.String(1000), nullable= False)
    date_created= db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

# with app.app_context():
#     db.create_all()




@app.route('/', methods= ['GET', 'POST'])
def hello_world():
    # return "Hello World !!!"
    
    if request.method=='POST':
        print('Post')
        # print(request.form['task'])
        task= (request.form['task'])
        # print(request.form['desc'])
        desc= (request.form['desc'])

        todo= Todo( title= task, Desc= desc)
        db.session.add(todo)
        db.session.commit()

    # todo= Todo( title= "First To Do", Desc= "Start investing in stocks...")
    # db.session.add(todo)
    # db.session.commit()

    all_todo= Todo.query.all()
    # print(all_todo)
    return render_template('index.html', all_todo= all_todo)
    # return render_template('index.html')


@app.route('/show')
def show():
    all_todo= Todo.query.all()
    print(all_todo)
    return render_template('index.html', all_todo= all_todo)





@app.route('/delete/<int:sno>')
def delete(sno):
    item =Todo.query.filter_by(sno= sno).first()

    try :
        db.session.delete(item)
        db.session.commit()

    except Exception as e:
        print("Error occurred while deleting the record")

    return redirect('/')





@app.route('/update/<int:sno>', methods= ['GET', 'POST'])
def update(sno):
    item =Todo.query.filter_by(sno= sno).first()
    if request.method=='POST':
        print('Post')
        # print(request.form['task'])
        task= (request.form['task'])
        # print(request.form['desc'])
        desc= (request.form['desc'])

        item.title= task
        item.Desc= desc
        db.session.add(item)
        db.session.commit()
        return redirect('/')


    return render_template('update.html', todo= item)



if __name__== '__main__':
    app.run(debug=True) 