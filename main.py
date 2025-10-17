from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from docs.swagger_config import swagger_template

# Import models and routes
from models.invoice import db
from routes.invoice_routes import invoice_bp
from routes.analytics_routes import analytics_bp 


from apscheduler.schedulers.background import BackgroundScheduler
from utils.exchange_manager import fetch_rates_from_api
from flasgger import Swagger

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


swagger = Swagger(app, template=swagger_template)

# Initialize database
db.init_app(app)

# Register routes
app.register_blueprint(invoice_bp)
app.register_blueprint(analytics_bp)

@app.route("/ping")
def ping():
    return jsonify({"message": "Server is running!"})

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    # Set up scheduler to fetch exchange rates daily at 2 AM
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_rates_from_api, "cron", hour=2, minute=0)
    scheduler.start()
    


    # Get port from environment variable or default to 5000
    port = int(os.getenv("PORT", 5000))

    app.run(debug=True, host="0.0.0.0", port=port)


