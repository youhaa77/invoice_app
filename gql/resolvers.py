from ariadne import QueryType
from models.invoice import db, Invoice
from utils.exchange_manager import get_exchange_rates

query = QueryType()


# ------------------------------
# Query Resolvers
# ------------------------------

@query.field("listInvoices")
def resolve_list_invoices(*_):
    try:
        invoices = Invoice.query.all()
        return {"success": True, "invoices": invoices, "errors": []}
    except Exception as e:
        return {"success": False, "invoices": [], "errors": [str(e)]}


@query.field("getInvoice")
def resolve_get_invoice(*_, id):
    try:
        invoice = Invoice.query.get(id)
        if not invoice:
            return {"success": False, "invoice": None, "errors": ["Invoice not found"]}
        return {"success": True, "invoice": invoice, "errors": []}
    except Exception as e:
        return {"success": False, "invoice": None, "errors": [str(e)]}
    
