from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import validates


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    transactions = db.relationship(
        "Transaction", back_populates="user", cascade="all, delete-orphan"
    )

    @validates("email")
    def validate_email(self, key, email):
        assert "@" in email, "Invalid email address"
        return email


class Transaction(db.Model):
    __tablename__ = "transactions"
    __table_args__ = (db.CheckConstraint("amount > 0", name="positive_amount"),)

    TRANSACTION_TYPES = ("Income", "Expense")

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False, server_default=func.current_date())
    description = db.Column(db.String(150))
    transaction_type = db.Column(
        db.Enum(*TRANSACTION_TYPES, name="transaction_types"), nullable=False
    )
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    status = db.Column(db.String(50), default="Pending")
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    user = db.relationship("User", back_populates="transactions")
    category = db.relationship("Category")


class Category(db.Model):
    __tablename__ = "categories"

    DEFAULT_CATEGORIES = [
        "Rent",
        "Utilities",
        "Food",
        "Transportation",
        "Entertainment",
        "Medical",
        "Other",
    ]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    transactions = db.relationship("Transaction", back_populates="category")

    @classmethod
    def insert_default_categories(cls):
        existing = {c.name for c in cls.query.all()}
        to_add = [
            cls(name=name) for name in cls.DEFAULT_CATEGORIES if name not in existing
        ]

        if to_add:
            db.session.bulk_save_objects(to_add)
            db.session.commit()
            return len(to_add)
        return 0
