from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    owner = db.Column(db.String(200), nullable=False)
    date_completed = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

class Owners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return '<Owner %r>' % self.id
    
with app.app_context():
        db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
         task_content = request.form['content']
         task_owner = request.form['owner']
         new_task = Todo(content=task_content, owner=task_owner, date_completed = None)

         try:
             db.session.add(new_task)
             db.session.commit()
             return redirect('/')
         except:
             return 'There was an issue adding the task ' + task_content + ' '  +  task_owner                                                                                                                                                                      
    else:
      tasks = Todo.query.order_by(Todo.date_created).all()
      owners = Owners.query.order_by(Owners.id).all()

      return render_template('index.html',tasks = tasks, owners = owners)
    
@app.route('/AddOwner', methods=['POST', 'GET'])
def addOwner():
    if request.method == 'POST':
         task_content = request.form['content']
         task_owner = request.form['owner']
         new_task = Todo(content=task_content, owner=task_owner, date_completed = None)

         try:
             db.session.add(new_task)
             db.session.commit()
             return redirect('/')
         except:
             return 'There was an issue adding the task ' + task_content + ' '  +  task_owner                                                                                                                                                                      
    else:
      tasks = Todo.query.order_by(Todo.date_created).all()
      owners = Owners.query.order_by(Owners.id).all()

      return render_template('index.html',tasks = tasks, owners = owners)    
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting the task'
    
@app.route('/ownerDelete/<int:id>')
def ownerDelete(id):
    owner_to_delete = Owners.query.get_or_404(id)

    try:
        db.session.delete(owner_to_delete)
        db.session.commit()
        return redirect('/gotoAddOwner')
    except:
        return 'There was an issue deleting the task'    
    
@app.route('/complete/<int:id>')
def complete(id):
    task_to_complete = Todo.query.get_or_404(id)
    if task_to_complete.date_completed is None:
      task_to_complete.date_completed = datetime.now(timezone.utc)
    else: 
      task_to_complete.date_completed = None  
    try:
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an issue completing the task'
    
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    
    task_to_update = Todo.query.get_or_404(id)
    owners = Owners.query.order_by(Owners.id).all()

    if request.method == 'POST':
      updated_content = request.form['content']
      updated_owner = request.form['owner']

      task_to_update.content = updated_content
      task_to_update.owner = updated_owner

      try:
        db.session.commit()
        return redirect('/')
      except:
        return 'There was an issue updating the task'

    else: 
      return render_template('update.html',task = task_to_update, owners = owners)

@app.route('/gotoAddOwner/', methods=['POST', 'GET'])
def gotoAddOwner():
  if request.method == 'POST':
       ownerName = request.form['ownerName']
       ownerID = request.form['Ownerid']
         
       new_owner = Owners(id=ownerID, name=ownerName)

       try:
         db.session.add(new_owner)
         db.session.commit()
         return redirect('/gotoAddOwner')
       except:
         return 'There was an issue adding this Owner ' + ownerID + ' '  +  ownerName
  else:
      MaxOwnerID = db.session.query(func.max(Owners.id+1)).scalar()
      owners = Owners.query.order_by(Owners.id).all()
      return render_template('addOwner.html',NewOwnerID = MaxOwnerID, owners = owners)  
       
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')
    ##)
    ##app.run(debug=True)

