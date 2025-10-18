swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Invoice Management API",
        "description": "API for managing invoices and performing analytics such as total revenue and average invoice value.",
        "version": "1.0.0",
        "contact": {
            "name": "Youhanna Baddar",
            "email": "youhannamen@gmail.com"
        }
    },
    "basePath": "/",
    "tags": [
        {"name": "Invoices", "description": "Invoice CRUD operations"},
        {"name": "Analytics", "description": "Revenue and invoice analytics"}
    ],
    "paths": {
        "/invoices": {
            "get": {
                "tags": ["Invoices"],
                "summary": "Get all invoices",
                "responses": {
                    "200": {"description": "List of all invoices"}
                }
            },
            "post": {
                "tags": ["Invoices"],
                "summary": "Create a new invoice",
                "parameters": [{
                    "in": "body",
                    "name": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "required": ["customer_name", "amount", "currency"],
                        "properties": {
                            "customer_name": {"type": "string", "example": "John Doe"},
                            "amount": {"type": "number", "example": 250.5},
                            "currency": {"type": "string", "example": "USD"},
                            "description": {"type": "string", "example": "Consulting service"},
                            "payment_method": {"type": "string", "example": "credit"},
                            "payment_status": {"type": "string", "example": "paid"}
                        }
                    }
                }],
                "responses": {
                    "201": {"description": "Invoice created successfully"},
                    "400": {"description": "Validation or currency error"}
                }
            }
        },
        "/invoices/{invoice_id}": {
            "get": {
                "tags": ["Invoices"],
                "summary": "Get a single invoice by ID",
                "parameters": [{
                    "name": "invoice_id",
                    "in": "path",
                    "type": "integer",
                    "required": True
                }],
                "responses": {
                    "200": {"description": "Invoice retrieved"},
                    "404": {"description": "Invoice not found"}
                }
            },
            "put": {
                "tags": ["Invoices"],
                "summary": "Update an existing invoice",
                "parameters": [
                    {"name": "invoice_id", "in": "path", "type": "integer", "required": True},
                    {"in": "body", "name": "body", "schema": {
                        "type": "object",
                        "properties": {
                            "customer_name": {"type": "string", "example": "Youhanna Baddar"},
                            "description": {"type": "string", "example": "Edited description"}
                        }
                    }}
                ],
                "responses": {
                    "200": {"description": "Invoice updated successfully"},
                    "400": {"description": "Invalid input"},
                    "404": {"description": "Invoice not found"}
                }
            },
            "delete": {
                "tags": ["Invoices"],
                "summary": "Delete an invoice",
                "parameters": [{
                    "name": "invoice_id",
                    "in": "path",
                    "type": "integer",
                    "required": True
                }],
                "responses": {
                    "200": {"description": "Invoice deleted"},
                    "404": {"description": "Invoice not found"}
                }
            }
        },

        "/invoices/{invoice_id}/exchange-rate": {
            "get": {
                "tags": ["Invoices"],
                "summary": "Get exchange rate and USD conversion details for a specific invoice",
                "parameters": [
                    {
                        "name": "invoice_id",
                        "in": "path",
                        "type": "integer",
                        "required": True,
                        "description": "ID of the invoice"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Exchange rate and conversion details retrieved successfully",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "invoice_id": {"type": "integer", "example": 5},
                                "currency": {"type": "string", "example": "EUR"},
                                "amount": {"type": "number", "example": 500},
                                "converted_amount_usd": {"type": "number", "example": 545.0},
                                "exchange_rate_to_usd": {"type": "number", "example": 1.09},
                                "base_currency": {"type": "string", "example": "USD"}
                            }
                        }
                    },
                    "404": {"description": "Invoice not found"}
                }
            }
        },
        "/analytics/total-revenue/{currency}": {
            "get": {
                "tags": ["Analytics"],
                "summary": "Get total revenue in the specified currency",
                "parameters": [{
                    "name": "currency",
                    "in": "path",
                    "type": "string",
                    "required": True,
                    "example": "USD"
                }],
                "responses": {
                    "200": {"description": "Total revenue calculated"},
                    "400": {"description": "Invalid currency code"}
                }
            }
        },
        "/analytics/average-invoice/{currency}": {
            "get": {
                "tags": ["Analytics"],
                "summary": "Get average invoice value in the specified currency",
                "parameters": [{
                    "name": "currency",
                    "in": "path",
                    "type": "string",
                    "required": True,
                    "example": "USD"
                }],
                "responses": {
                    "200": {"description": "Average invoice calculated"},
                    "400": {"description": "Invalid currency code"}
                }
            }
        }
    }
}
