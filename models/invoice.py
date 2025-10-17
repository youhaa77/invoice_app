from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    #  Payment details
    payment_method = db.Column(db.String(20), nullable=False, default="cash")  # cash, credit, etc.
    payment_status = db.Column(db.String(20), nullable=False, default="paid")  # paid, pending, refunded

    #  Conversion details
    converted_amount_usd = db.Column(db.Float, nullable=False)
    exchange_rate_to_usd = db.Column(db.Float, nullable=False)
    base_currency = db.Column(db.String(10), default="USD")

    #  Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "amount": self.amount,
            "currency": self.currency,
            "description": self.description,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "converted_amount_usd": self.converted_amount_usd,
            "exchange_rate_to_usd": self.exchange_rate_to_usd,
            "base_currency": self.base_currency,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
