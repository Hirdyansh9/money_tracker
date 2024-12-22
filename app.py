# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///money_tracker.db'
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Transaction {self.id}>'

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        person = request.form['person']
        type = request.form['type']
        amount = float(request.form['amount'])
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        reason = request.form['reason']
        
        new_transaction = Transaction(person=person, type=type, amount=amount, date=date, reason=reason)
        db.session.add(new_transaction)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    summary = calculate_summary(transactions)
    chart_data = prepare_chart_data(transactions)
    return render_template('index.html', transactions=transactions, summary=summary, chart_data=json.dumps(chart_data))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    if request.method == 'POST':
        transaction.person = request.form['person']
        transaction.type = request.form['type']
        transaction.amount = float(request.form['amount'])
        transaction.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        transaction.reason = request.form['reason']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', transaction=transaction)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    transactions = Transaction.query.filter(
        (Transaction.person.ilike(f'%{query}%')) |
        (Transaction.reason.ilike(f'%{query}%'))
    ).order_by(Transaction.date.desc()).all()
    return render_template('search_results.html', transactions=transactions, query=query)

def calculate_summary(transactions):
    summary = {}
    for transaction in transactions:
        if transaction.person not in summary:
            summary[transaction.person] = {'lent': 0, 'borrowed': 0}
        if transaction.type == 'lent':
            summary[transaction.person]['lent'] += transaction.amount
        else:
            summary[transaction.person]['borrowed'] += transaction.amount
    
    for person in summary:
        summary[person]['net'] = summary[person]['lent'] - summary[person]['borrowed']
    
    return summary

def prepare_chart_data(transactions):
    data = {}
    for transaction in transactions:
        month = transaction.date.strftime('%Y-%m')
        if month not in data:
            data[month] = {'lent': 0, 'borrowed': 0}
        if transaction.type == 'lent':
            data[month]['lent'] += transaction.amount
        else:
            data[month]['borrowed'] += transaction.amount
    
    chart_data = [{'month': k, 'lent': v['lent'], 'borrowed': v['borrowed']} for k, v in data.items()]
    chart_data.sort(key=lambda x: x['month'])
    return chart_data

if __name__ == '__main__':
    app.run(debug=True)