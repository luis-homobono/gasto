from datetime import datetime

from gasto.extensions import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # Relationships
    balances = db.relationship("Balance", backref="user", lazy=True)
    budgets = db.relationship("Budget", backref="user", lazy=True)
    accounts = db.relationship("Account", backref="user", lazy=True)
    incomes = db.relationship("Incomes", backref="user", lazy=True)
    expenses = db.relationship("Expenses", backref="user", lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(pwhash=self.password_hash, password=password)

    def __repr__(self):
        return f"<User {self.username}>"


class Balance(db.Model):
    __tablename__ = "balances"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.now())
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    assets = db.relationship(
        "Assets", backref="balance", lazy=True, cascade="all, delete-orphan"
    )
    liabilities = db.relationship(
        "Liabilities", backref="balance", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(self, date, user_id):
        self.date = date
        self.user_id = user_id

    def __repr__(self):
        return f"<Balance {self.date}>"


class AssetLiabilityType(db.Model):
    __tablename__ = "assets_liabilities_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    is_asset = db.Column(db.Boolean, default=False)
    # Relationships
    assets = db.relationship("Asset", backref="asset_liabity_type", lazy=True)
    liabilities = db.relationship("Liability", backref="asset_liabity_type", lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<AssetLiabilityType {self.name}>"


class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    is_current = db.Column(db.Boolean, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # Relationships
    balance_id = db.Column(db.Integer, db.ForeignKey("balances.id"), nullable=False)
    type_id = db.Column(
        db.Integer, db.ForeignKey("assets_liabilities_types.id"), nullable=False
    )

    def __init__(self, name, amount, is_current, balance_id, type_asset_id):
        self.name = name
        self.amount = amount
        self.is_current = is_current
        self.balance_id = balance_id
        self.type_asset_id = type_asset_id

    def __repr__(self):
        return f"<Asset {self.name}: {self.amount}>"


class Liability(db.Model):
    __tablename__ = "liabilities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    is_current = db.Column(db.Boolean, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # Relationships
    balance_id = db.Column(db.Integer, db.ForeignKey("balances.id"), nullable=False)
    type_id = db.Column(
        db.Integer, db.ForeignKey("assets_liabilities_types.id"), nullable=False
    )

    def __init__(self, name, amount, is_current, balance_id, type_liability_id):
        self.name = name
        self.amount = amount
        self.is_current = is_current
        self.balance_id = balance_id
        self.type_liability_id = type_liability_id

    def __repr__(self):
        return f"<Liability {self.name}: {self.amount}>"


class Budget(db.Model):
    __tablename__ = "budgets"

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    incomes = db.relationship(
        "Income", backref="budget", lazy=True, cascade="all, delete-orphan"
    )
    expenses = db.relationship(
        "Expense", backref="budget", lazy=True, cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.UniqueConstraint("month", "year", "user_id", name="_month_year_user_uc"),
    )

    def __init__(self, month, year, user_id):
        self.month = month
        self.year = year
        self.user_id = user_id

    def __repr__(self):
        return f"<Budget {self.month}/{self.year} - User: {self.user_id}>"


class Income(db.Model):
    __tablename__ = "incomes"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    income_date = db.Column(db.Date, nullable=False, default=datetime.now())
    # Relationships
    budget_id = db.Column(db.Integer, db.ForeignKey("budgets.id"), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey("periods.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    def __init__(self, description, amount, income_date):
        self.description = description
        self.amount = amount
        self.income_date = income_date

    def __repr__(self):
        return f"<Income {self.description}: {self.amount}>"


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    expense_date = db.Column(db.Date, nullable=False, default=datetime.now())
    # Relationships
    budget_id = db.Column(db.Integer, db.ForeignKey("budgets.id"), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey("periods.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    def __init__(self, description, amount, expense_date):
        self.description = description
        self.amount = amount
        self.expense_date = expense_date

    def __repr__(self):
        return f"<Expense {self.description}: {self.amount}>"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=True)
    is_expense = db.Column(db.Boolean, default=False)
    # Relationships
    expenses = db.relationship("Expense", backref="category", lazy=True)
    incomes = db.relationship("Income", backref="category", lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Category {self.name}>"


class Period(db.Model):
    __tablename__ = "periods"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    amount_days = db.Column(db.Integer, unique=True, nullable=False)
    # Relationships
    expenses = db.relationship("Expense", backref="period", lazy=True)
    incomes = db.relationship("Income", backref="period", lazy=True)

    def __init__(self, name, amount_days):
        self.name = name
        self.amount_days = amount_days


class AccountType(db.Model):
    __tablename__ = "account_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    # Relationships
    accounts = db.relationship("Account", backref="account_type", lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<AccountType {self.name}>"


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    initial_balance = db.Column(db.Numeric(10, 2), nullable=False)
    current_balance = db.Column(db.Numeric(10, 2), nullable=False)
    # Relationships
    account_type_id = db.Column(
        db.Integer, db.ForeignKey("account_types.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    income = db.relationship("Income", backref="account", lazy=True)
    expenses = db.relationship("Expense", backref="account", lazy=True)

    def __init__(
        self, name, initial_balance, current_balance, type_account_id, user_id
    ):
        self.name = name
        self.initial_balance = initial_balance
        self.current_balance = current_balance
        self.type_account_id = type_account_id
        self.user_id = user_id

    def __repr__(self):
        return f"<Account {self.name}: {self.current_balance}>"
