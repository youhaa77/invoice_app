from flask import Blueprint, request, jsonify
from models.invoice import db, Invoice
from utils.exchange_manager import get_exchange_rates
from utils.invoice_schema import InvoiceSchema
from marshmallow import ValidationError

invoice_bp = Blueprint("invoice_bp", __name__)
invoice_schema = InvoiceSchema()

# Create a new invoice with conversion

@invoice_bp.route("/invoices", methods=["POST"])
def create_invoice():
    try:
        # Validate and load data
        data = invoice_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    rates = get_exchange_rates()
    currency = data["currency"].upper()

    if currency not in rates:
        return jsonify({"error": f"Unsupported currency code: {currency}"}), 400

    rate = rates[currency]
    converted_amount_usd = data["amount"] / rate

    invoice = Invoice(
        **data,
        converted_amount_usd=converted_amount_usd,
        exchange_rate_to_usd=rate,
        base_currency="USD"
    )

    db.session.add(invoice)
    db.session.commit()

    return jsonify(invoice.to_dict()), 201


# Get all invoices
@invoice_bp.route("/invoices", methods=["GET"])
def get_invoices():
    invoices = Invoice.query.all()
    return jsonify([invoice.to_dict() for invoice in invoices]), 200


# Get single invoice by ID
@invoice_bp.route("/invoices/<int:invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    return jsonify(invoice.to_dict()), 200


@invoice_bp.route("/invoices/<int:invoice_id>", methods=["PUT"])
def update_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404

    try:
        # Validate only fields provided (partial update)
        data = invoice_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    # Update only the provided fields
    for key, value in data.items():
        setattr(invoice, key, value)

    # If amount or currency changed → recalculate conversion
    if "amount" in data or "currency" in data:
        rates = get_exchange_rates()
        if not rates:
            return jsonify({"error": "Failed to fetch exchange rates"}), 500

        currency = invoice.currency.upper()
        if currency not in rates:
            return jsonify({"error": f"Invalid currency code: {currency}"}), 400

        rate = rates[currency]
        invoice.exchange_rate_to_usd = rate
        invoice.converted_amount_usd = invoice.amount / rate

    db.session.commit()

    return jsonify({
        "message": "Invoice updated successfully",
        "invoice": invoice.to_dict()
    }), 200


# Delete an invoice
@invoice_bp.route("/invoices/<int:invoice_id>", methods=["DELETE"])
def delete_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404

    db.session.delete(invoice)
    db.session.commit()

    return jsonify({"message": f"Invoice {invoice_id} deleted successfully"}), 200

@invoice_bp.route("/invoices/<int:invoice_id>/exchange-rate", methods=["GET"])
def get_invoice_exchange_rate(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404

    return jsonify({
        "invoice_id": invoice.id,
        "currency": invoice.currency,
        "amount": invoice.amount,
        "converted_amount_usd": invoice.converted_amount_usd,
        "exchange_rate_to_usd": invoice.exchange_rate_to_usd,
        "base_currency": invoice.base_currency
    }), 200
