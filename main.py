from _decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from datetime import datetime, timedelta
import calendar

from sqlalchemy import func
from wtforms import StringField, DecimalField, SubmitField, SelectField, DateField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, NumberRange, DataRequired

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:base23@localhost:5432/finance2'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('accounts', lazy=True))

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), nullable=False)

class FinancialTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    transaction_date = db.Column(db.Date, nullable=False)
    is_income = db.Column(db.Boolean, nullable=False)

    user = db.relationship('User', backref=db.backref('transactions', lazy=True))
    account = db.relationship('Account', backref=db.backref('transactions', lazy=True))

class AccountForm(FlaskForm):
    account_name = StringField('Account Name', validators=[DataRequired()])
    initial_balance = DecimalField('Initial Balance', validators=[DataRequired()])
    submit = SubmitField('Create Account')

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    goal_name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    savings = db.Column(db.DECIMAL(10, 2), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    is_achieved = db.Column(db.Boolean, nullable=False, default=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(password) <= 5:
            flash('Password should be longer than 5 characters.', 'danger')
            return redirect(url_for('register'))
        if not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
            flash("Password should contain both letters and numbers.", 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash("Username is already taken. Please choose a different one.", 'danger')
            return redirect(url_for('register'))
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))


@app.route('/accounts', methods=['GET', 'POST'])
def accounts():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    name = user.username
    form = AccountForm()

    if form.validate_on_submit():
        new_account = Account(
            user_id=user_id,
            name=form.account_name.data,
            balance=form.initial_balance.data
        )
        db.session.add(new_account)
        db.session.commit()

        return redirect(url_for('accounts', user_id=user.id))

    if 'delete_account' in request.form:
        account_id_to_delete = request.form['delete_account']
        FinancialTransaction.query.filter_by(account_id=account_id_to_delete).delete()
        acc = Account.query.get_or_404(account_id_to_delete)
        db.session.delete(acc)
        db.session.commit()

        return redirect(url_for('accounts', user_id=user.id))

    if 'rename_account' in request.form:
        account_id_to_rename = request.form['rename_account']
        new_account_name = request.form['new_account_name']
        account = Account.query.get_or_404(account_id_to_rename)
        account.name = new_account_name
        db.session.commit()

        return redirect(url_for('accounts', user_id=user.id))

    user_accounts = Account.query.filter_by(user_id=user_id).all()

    return render_template('accounts.html', user_id=user.id, name=name, form=form, user_accounts=user_accounts)

@app.route('/calend')
def calend():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    name = user.username

    start_date = datetime(2023, 1, 1).date()
    end_date = datetime.now().date()

    events_data = []

    current_date = start_date
    while current_date <= end_date:
        daily_expenses = db.session.query(db.func.sum(FinancialTransaction.amount)).\
            filter(FinancialTransaction.user_id == user_id, FinancialTransaction.is_income == False, FinancialTransaction.transaction_date == current_date).scalar()

        if daily_expenses:
            events_data.append({
                'title': str(daily_expenses),
                'start': current_date.strftime('%Y-%m-%d')
            })

        current_date += timedelta(days=1)

    return render_template('calend.html', user=user, name=name, events_data=events_data)

@app.route('/goal')
def goal():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    name = user.username
    goal = request.form.get('goal_name')
    start_date = datetime.now().date()
    end_date = request.form.get('period')
    salary = request.form.get('salary')

    return render_template('goal.html', user=user, name=name)


@app.route('/history', methods=['GET', 'POST'])
def history():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    account = Account.query.filter_by(user_id=user_id).all()
    categories = Category.query.all()
    #last = request.args.get('show_last')

    if request.method == 'POST':
        start_date_str = request.form.get('start')
        end_date_str = request.form.get('end')
        try:
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y').date()
            end_date = datetime.strptime(end_date_str, '%d/%m/%Y').date()
            if end_date >= start_date:
                transactions = FinancialTransaction.query.filter(
                    FinancialTransaction.user_id == user_id,
                    FinancialTransaction.transaction_date.between(start_date, end_date)
                ).order_by(FinancialTransaction.transaction_date.desc()).all()
            else:
                return redirect(url_for('history'))
        except ValueError:
            return redirect(url_for('history'))
    else:
        transactions = FinancialTransaction.query.filter_by(user_id=user_id).order_by(FinancialTransaction.transaction_date.desc()).limit(25).all()

    return render_template('history.html', user=user, account=account, categories=categories, transactions=transactions)

        #return render_template('history.html', user=user, account=account, categories=categories, transactions=transactions)

    transactions = FinancialTransaction.query.filter_by(user_id=user_id).order_by(
        FinancialTransaction.transaction_date.desc()).limit(25).all()
    return render_template('history.html', user=user, account=account, categories=categories, transactions=transactions)

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    name = user.username
    today = datetime.now()
    start_date1 = today.replace(day=1)
    end_date1 = today.replace(day=calendar.monthrange(today.year, today.month)[1])
    input_start = datetime.strptime(str(start_date1), "%Y-%m-%d %H:%M:%S.%f")
    input_end = datetime.strptime(str(end_date1), "%Y-%m-%d %H:%M:%S.%f")
    start_date11 = input_start.strftime("%d/%m/%Y")
    end_date11 = input_end.strftime("%d/%m/%Y")

    if request.method == 'POST':
        start_date1 = request.form.get('start1')
        end_date1 = request.form.get('end1')
        try:
            start_date11 = datetime.strptime(start_date1, '%d/%m/%Y').date()
            end_date11 = datetime.strptime(end_date1, '%d/%m/%Y').date()
            start_date11 = start_date11.strftime("%d/%m/%Y")
            end_date11 = end_date11.strftime("%d/%m/%Y")
        except ValueError:
            return redirect(url_for('statistics'))

    expenses_by_day = (
        db.session.query(
            func.extract('day', FinancialTransaction.transaction_date).label('day'),
            func.extract('month', FinancialTransaction.transaction_date).label('month'),
            func.extract('year', FinancialTransaction.transaction_date).label('year'),
            func.sum(FinancialTransaction.amount).label('total_expenses')
        )
        .filter(
            FinancialTransaction.user_id == user_id,
            FinancialTransaction.transaction_date.between(start_date11, end_date11),
            FinancialTransaction.is_income == False
        )
        .group_by('day', 'month', 'year')
        .order_by('year', 'month', 'day')
        .all()
    )

    result = [
        [
            float(f"{entry[0]:.0f}.{entry[1]:.0f}"),
            float(entry[3])
        ] for entry in expenses_by_day
    ]

    expenses_by_category = (
        db.session.query(
            Category.category_name.label('category_name'),
            func.sum(FinancialTransaction.amount).label('total_expenses')
        )
        .join(FinancialTransaction, FinancialTransaction.category == Category.category_id)
        .filter(
            FinancialTransaction.user_id == user_id,
            FinancialTransaction.transaction_date.between(start_date11, end_date11),
            FinancialTransaction.is_income == False
        )
        .group_by(Category.category_name)
        .order_by(func.sum(FinancialTransaction.amount).desc())
        .all()
    )

    category_names = [entry.category_name for entry in expenses_by_category]
    print(category_names)
    total_expenses = [float(entry.total_expenses) for entry in expenses_by_category]
    print(total_expenses)

    return render_template('statistics.html', user=user, name=name, result=result, category_names=category_names, total_expenses=total_expenses, start_date11=start_date11, end_date11=end_date11)

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    name = user.username
    today = datetime.now()

    start_date1 = today.replace(day=1)
    end_date1 = today.replace(day=calendar.monthrange(today.year, today.month)[1])
    input_start = datetime.strptime(str(start_date1), "%Y-%m-%d %H:%M:%S.%f")
    input_end = datetime.strptime(str(end_date1), "%Y-%m-%d %H:%M:%S.%f")
    start_date11 = input_start.strftime("%d/%m/%Y")
    end_date11 = input_end.strftime("%d/%m/%Y")

    expenses_by_day = (
        db.session.query(
            func.extract('day', FinancialTransaction.transaction_date).label('day'),
            func.extract('month', FinancialTransaction.transaction_date).label('month'),
            func.extract('year', FinancialTransaction.transaction_date).label('year'),
            func.sum(FinancialTransaction.amount).label('total_expenses')
        )
        .filter(
            FinancialTransaction.user_id == user_id,
            FinancialTransaction.transaction_date.between(start_date11, end_date11),
            FinancialTransaction.is_income == False
        )
        .group_by('day', 'month', 'year')
        .order_by('year', 'month', 'day')
        .all()
    )

    result = [
        [
            float(f"{entry[0]:.0f}.{entry[1]:.0f}"),
            float(entry[3])
        ] for entry in expenses_by_day
    ]

    return render_template('dashboard.html', user=user, name=name, result=result)


@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    account_id = request.args.get('account_id')
    account = Account.query.get_or_404(account_id)
    categories = Category.query.all()
    name = None

    if request.method == 'POST':
        if 'delete_transaction' in request.form:
            transaction_id_to_delete = request.form['delete_transaction']
            transaction_to_delete = FinancialTransaction.query.get_or_404(transaction_id_to_delete)

            if transaction_to_delete.is_income:
                if account.balance >= transaction_to_delete.amount:
                    account.balance = Decimal(str(account.balance)) - Decimal(str(transaction_to_delete.amount))
                    db.session.delete(transaction_to_delete)
                    db.session.commit()
                else:
                    return redirect(url_for('transactions', user_id=user_id, account_id=account_id))
            else:
                account.balance = Decimal(str(account.balance)) + Decimal(str(transaction_to_delete.amount))
            db.session.delete(transaction_to_delete)
            db.session.commit()
        else:
            try:
                amount = float(request.form['amount'])
                category_id = request.form['category']
                is_income_str = request.form['is_income']
                is_income = is_income_str.lower() == 'true'
                name = (Category.query.filter_by(category_id=category_id).first()).category_name

                if amount <= 0:
                    return redirect(url_for('transactions', user_id=user_id, account_id=account_id))

                if is_income == False and account.balance < amount:
                    return redirect(url_for('transactions', user_id=user_id, account_id=account_id))
                else:
                    new_transaction = FinancialTransaction(
                        amount=amount,
                        category=category_id,
                        transaction_date=datetime.now().date(),
                        account_id=account_id,
                        is_income=is_income,
                        user_id=user_id
                    )

                    if is_income:
                        account.balance += amount
                    else:
                        account.balance -= amount

                    db.session.add(new_transaction)
                    db.session.commit()

                    return redirect(url_for('transactions', user_id=user_id, account_id=account_id))
            except ValueError:
                return redirect(url_for('transactions', user_id=user_id, account_id=account_id))

    transactions = FinancialTransaction.query.filter_by(user_id=user_id, account_id=account_id).all()
    return render_template('transactions.html', user=user, account=account, transactions=transactions, categories=categories, name=name)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

