from flask import Blueprint, jsonify, request
from models.invoice import db, Invoice
import requests

from utils.exchange_manager import get_exchange_rates

analytics_bp = Blueprint("analytics_bp", __name__)

# Get Total Revenue (in USD or optional currency)
@analytics_bp.route("/analytics/total-revenue/<string:currency>", methods=["GET"])
def total_revenue(currency):
    target_currency = currency.upper()

    # Sum of all invoices in USD
    total_usd = db.session.query(db.func.sum(Invoice.converted_amount_usd)).scalar() or 0.0

    # Fetch exchange rates
    rates = get_exchange_rates()
    if not rates:
        return jsonify({"error": "Failed to fetch exchange rates"}), 500

    # Convert if not USD
    if target_currency not in rates:
        return jsonify({"error": f"Invalid currency code: {target_currency}"}), 400

    total_converted = total_usd * rates[target_currency]

    return jsonify({
        "base_currency": "USD",
        "target_currency": target_currency,
        "total_revenue": round(total_converted, 2)
    }), 200


@analytics_bp.route("/analytics/average-invoice/<string:currency>", methods=["GET"])
def average_invoice(currency):
    
    target_currency = currency.upper()

    rates = get_exchange_rates()

   
    if not rates:
        return jsonify({"error": "Failed to fetch exchange rates"}), 500

    if target_currency not in rates:
        return jsonify({"error": f"Invalid currency code: {target_currency}"}), 400

    total_usd = db.session.query(db.func.sum(Invoice.converted_amount_usd)).scalar() or 0.0
    count = db.session.query(db.func.count(Invoice.id)).scalar() or 0

    print("passed total and count")
    if count == 0:
        return jsonify({"message": "No invoices found", "average_invoice_size": 0}), 200

    avg_usd = total_usd / count
    

    avg_converted = avg_usd * rates[target_currency]

    return jsonify({
        "base_currency": "USD",
        "target_currency": target_currency,
        "average_invoice_size": round(avg_converted, 2)
    }), 200
