from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Drug(db.Model):
    code = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    atc_code = db.Column(db.String(20), nullable=False)
    dosage_form = db.Column(db.String(20), nullable=True)
    pack_size = db.Column(db.Integer, nullable=True)
    pack_price = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return '<Task %r>' % self.id

with app.app_context():
        db.create_all()

@app.route('/', methods=['GET','POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')

@app.route('/find_by_code', methods=['POST'])
def find_by_code():
    if request.method == 'POST':
      in_code = request.form['code']
      if in_code.strip() != "":

        found_drugs = Drug.query.filter(Drug.name.ilike(f"{in_code}%")).order_by((Drug.pack_price / Drug.pack_size).asc()).all()
        if found_drugs is None:
          return f'There is no drug found matching {in_code}'
        else:
          return render_template('choosedrug.html',drugs = found_drugs)
      else:
         return f'No code entered'
      
@app.route('/home', methods=['GET'])
def home():
    if request.method == 'GET':
      return render_template('index.html')   

@app.route('/find_by_name', methods=['POST'])
def find_by_name():
    if request.method == 'POST':
      in_name = request.form['name']
      if in_name.strip() != "":

        found_drugs = Drug.query.filter(Drug.name.ilike(f"{in_name}%")).order_by((Drug.pack_price / Drug.pack_size).asc()).all()
        if found_drugs is None:
          return f'There is no drug found matching {in_name}'
        else:
          return render_template('choosedrug.html',drugs = found_drugs)
      else:
         return f'No name entered'

@app.route('/fetch/<string:drug_dosage_form>/<string:drug_atc_code>', methods=['GET'])
def fetch(drug_dosage_form,drug_atc_code):
    if request.method == 'GET':
      found_drugs = Drug.query.filter(
        Drug.dosage_form == drug_dosage_form,
        Drug.atc_code == drug_atc_code).order_by((Drug.pack_price / Drug.pack_size).asc()).all()


    if found_drugs is None:
      return f'There is no equivilent drugs found'
    else:
      return render_template('listequivelents.html',drugs = found_drugs)

if __name__ == "__main__":

    app.run()
    ##app.run(debug=True)

