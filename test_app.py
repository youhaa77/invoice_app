import pytest
from app import app, db
from models.invoice import Invoice

@pytest.fixture
def client():
    # Use in-memory SQLite for faster testing
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


# ---------- CREATE INVOICE TESTS ----------

def test_create_invoice_success(client):
    data = {
        "customer_name": "Youhanna Baddar",
        "amount": 1000,
        "currency": "EUR",
        "description": "Testing invoice",
        "payment_method": "cash",
        "payment_status": "paid"
    }
    res = client.post("/invoices", json=data)
    assert res.status_code == 201
    body = res.get_json()
    assert "id" in body
    assert body["currency"] == "EUR"

def test_create_invoice_missing_field(client):
    data = {
        "customer_name": "Test",
        "amount": 200,
        "payment_method": "cash",
        "payment_status": "paid"
    }
    res = client.post("/invoices", json=data)
    assert res.status_code == 400
    assert "errors" in res.get_json() or "error" in res.get_json()

def test_create_invoice_wrong_type(client):
    data = {
        "customer_name": "Test",
        "amount": "abc",  #  Wrong type
        "currency": "USD",
        "payment_method": "credit",
        "payment_status": "paid"
    }
    res = client.post("/invoices", json=data)
    assert res.status_code == 400

def test_create_invoice_invalid_currency(client):
    data = {
        "customer_name": "Test",
        "amount": 100,
        "currency": "XXX",  #  Invalid currency
        "payment_method": "cash",
        "payment_status": "paid"
    }
    res = client.post("/invoices", json=data)
    assert res.status_code == 400
# ---------- UPDATE INVOICE TESTS ----------

def test_update_invoice_success(client):
    # First create one
    create_data = {
        "customer_name": "John",
        "amount": 500,
        "currency": "EUR",
        "payment_method": "cash",
        "payment_status": "paid"
    }
    client.post("/invoices", json=create_data)

    update_data = {"amount": 900}
    res = client.put("/invoices/1", json=update_data)
    assert res.status_code == 200
    body = res.get_json()
    assert body["invoice"]["amount"] == 900

def test_update_invoice_invalid_type(client):
    create_data = {
        "customer_name": "John",
        "amount": 100,
        "currency": "EUR",
        "payment_method": "cash",
        "payment_status": "paid"
    }
    client.post("/invoices", json=create_data)

    update_data = {"amount": "wrong"}  #  invalid type
    res = client.put("/invoices/1", json=update_data)
    assert res.status_code == 400

def test_update_invoice_invalid_currency(client):
    create_data = {
        "customer_name": "John",
        "amount": 100,
        "currency": "EUR",
        "payment_method": "cash",
        "payment_status": "paid"
    }
    client.post("/invoices", json=create_data)

    update_data = {"currency": "XYZ"}  #  invalid currency
    res = client.put("/invoices/1", json=update_data)
    assert res.status_code == 400

def test_update_invoice_missing_id(client):
    update_data = {"amount": 500}
    res = client.put("/invoices/99", json=update_data)
    assert res.status_code == 404

# ---------- DELETE INVOICE TESTS ----------

def test_delete_invoice_success(client):
    # First create one
    data = {
        "customer_name": "John Doe",
        "amount": 300,
        "currency": "EUR",
        "payment_method": "cash",
        "payment_status": "paid"
    }
    client.post("/invoices", json=data)

    res = client.delete("/invoices/1")
    assert res.status_code == 200
    body = res.get_json()
    assert "deleted" in body["message"].lower()

def test_delete_invoice_not_found(client):
    res = client.delete("/invoices/999")
    assert res.status_code == 404
    assert "not found" in res.get_json()["error"].lower()


# ---------- ANALYTICS TESTS ----------

def test_total_revenue_success(client):
    # Create two invoices
    invoices = [
        {
            "customer_name": "Client A",
            "amount": 100,
            "currency": "USD",
            "payment_method": "cash",
            "payment_status": "paid"
        },
        {
            "customer_name": "Client B",
            "amount": 200,
            "currency": "USD",
            "payment_method": "credit",
            "payment_status": "paid"
        }
    ]
    for inv in invoices:
        client.post("/invoices", json=inv)

    res = client.get("/analytics/total-revenue/USD")
    assert res.status_code == 200
    body = res.get_json()
    assert "total_revenue" in body
    assert body["total_revenue"] == 300.0


def test_total_revenue_invalid_currency(client):
    res = client.get("/analytics/total-revenue/XYZ")
    # API should respond with a 400 for invalid currency
    assert res.status_code == 400
    print(res.get_json())

# ---------- AVERAGE INVOICE ANALYTICS TESTS ----------

def test_average_invoice_success(client):
    # Create invoices
    invoices = [
        {
            "customer_name": "Client A",
            "amount": 100,
            "currency": "USD",
            "payment_method": "cash",
            "payment_status": "paid"
        },
        {
            "customer_name": "Client B",
            "amount": 300,
            "currency": "USD",
            "payment_method": "credit",
            "payment_status": "paid"
        }
    ]
    for inv in invoices:
        client.post("/invoices", json=inv)

    res = client.get("/analytics/average-invoice/USD")
    assert res.status_code == 200
    body = res.get_json()

    assert "average_invoice_size" in body
    assert body["average_invoice_size"] > 0
    # Expected average = (100 + 300) / 2 = 200
    assert round(body["average_invoice_size"]) == 200


def test_average_invoice_invalid_currency(client):
    res = client.get("/analytics/average-invoice/XYZ")
    assert res.status_code == 400