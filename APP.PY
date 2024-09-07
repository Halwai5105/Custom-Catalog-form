from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class CatalogItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    center = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # Gender (Male/Female)
    date = db.Column(db.Date, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.form
    new_item = CatalogItem(
        name=data['name'],
        center=data['center'],
        gender=data['gender'],
        date=datetime.strptime(data['date'], '%Y-%m-%d')
    )
    db.session.add(new_item)
    db.session.commit()
    flash('Your response has been submitted.')
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = CatalogItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item has been deleted.')
    return redirect(url_for('view_items'))
    
@app.route('/view')
def view_items():
    items = CatalogItem.query.all()
    return render_template('view.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
