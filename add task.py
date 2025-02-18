from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hardware_part = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)



with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'clear' in request.form:
            db.session.query(Expense).delete()
            db.session.commit()
            return redirect(url_for('index'))

        hardware_part = request.form.get('hardware_part')
        price = request.form.get('price')

        if hardware_part and price:
            new_expense = Expense(hardware_part=hardware_part, price=float(price))
            db.session.add(new_expense)
            db.session.commit()
            return redirect(url_for('index'))

    expenses = Expense.query.all()
    total_cost = sum(exp.price for exp in expenses)
    return render_template('index.html', expenses=expenses, total_cost=total_cost)


if __name__ == '__main__':
    app.run(debug=True).