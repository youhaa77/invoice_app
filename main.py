from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from docs.swagger_config import swagger_template

# GraphQL imports
from ariadne.explorer import ExplorerGraphiQL
from gql.resolvers import query # import our resolvers
from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType



# Import models and routes
from models.invoice import db
from routes.invoice_routes import invoice_bp
from routes.analytics_routes import analytics_bp 



from flasgger import Swagger



# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


swagger = Swagger(app, template=swagger_template)


# Load schema
type_defs = load_schema_from_path("gql/schema.graphql")


# Bind resolvers
schema = make_executable_schema(type_defs, query)

# Enable GraphiQL Explorer (browser UI)
explorer_html = ExplorerGraphiQL().html(None)




# Initialize database
db.init_app(app)

# Register routes
app.register_blueprint(invoice_bp)
app.register_blueprint(analytics_bp)

@app.route("/ping")
def ping():
    return jsonify({"message": "Server is running!"})



@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return explorer_html, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=True)
    status_code = 200 if success else 400
    return jsonify(result), status_code


# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    
    # Get port from environment variable or default to 5000
    port = int(os.getenv("PORT", 5000))

    app.run(debug=True, host="0.0.0.0", port=port)


