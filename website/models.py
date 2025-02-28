from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model, UserMixin):
    """
    User Model
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now)
    transactions = db.relationship("Transaction")

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name


class Transaction(db.Model):
    """
    Transaction Model
    """

    transactions = ["Income", "Expense"]

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime)
    description = db.Column(db.String(150))
    transaction_type = db.Column(db.Enum(*transactions, name="transaction_types"))
    category = db.Column(db.Integer, db.ForeignKey("category.id"))
    status = db.Column(db.String(150))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


    # def __init__(
    #     self, user_id, amount, date, description, transaction_type, category, status
    # ):
    #     self.user_id = user_id
    #     self.amount = amount
    #     self.date = date
    #     self.description = description
    #     self.transaction_type = transaction_type
    #     self.category = category
    #     self.status = status

    # def __repr__(self):
    #     return "<Transaction {}>".format(self.id)


class Category(db.Model):
    """
    Category Model
    """

    categories = [
        "Rent",
        "Utilities",
        "Food",
        "Transportation",
        "Entertainment",
        "Medical",
        "Other",
    ]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Category {}>".format(self.id)

    @classmethod
    def insert_default_categories(cls):
        """
        Insert default categories into the database
        """
        for category in cls.categories:
            if not cls.query.filter_by(name=category).first():
                db.session.add(cls(name=category))
        db.session.commit()
