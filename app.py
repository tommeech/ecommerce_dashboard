# Import necessary modules and libraries
from flask import Flask, jsonify, render_template, Response, abort, make_response
import sqlite3
import pathlib
import logging
import requests  # Importing the requests library

# Setup logging
logging.basicConfig(filename="app.log", level=logging.DEBUG)

# Get the absolute path of the current file's directory
working_directory = pathlib.Path(__file__).parent.absolute()

# Define the path to the SQLite database file
DATABASE = working_directory / "CCL_ecommerce.db"

# Function to execute a database query and return the result
def query_db(query: str, args=()) -> list:
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, args).fetchall()
        return result
    except sqlite3.Error as e:
        # Log database errors
        logging.error("Database error: %s", e)
        # Raise a 500 Internal Server Error with a description
        abort(500, description="Database error occurred.")

# Create a Flask web application
app = Flask(__name__)

# Define error handlers for 404 and 500 errors
@app.errorhandler(404)
def not_found(error):
    # Return a JSON response for 404 errors
    return make_response(jsonify({"error": "Not found"}), 404)

@app.errorhandler(500)
def internal_error(error):
    # Return a JSON response for 500 errors
    return make_response(jsonify({"error": "Internal server error"}), 500)

# Define a route for the root URL ("/") that renders a template
@app.route("/")
def index() -> str:
    # Render the "dashboard.html" template for the root URL
    return render_template("dashboard.html")

# Define an API endpoint to retrieve orders over time
@app.route("/api/orders_over_time")
def orders_over_time() -> Response:
    query = """
    SELECT order_date, COUNT(order_id) AS num_orders
    FROM orders
    GROUP BY order_date
    ORDER BY order_date;
    """
    try:
        # Execute the database query and retrieve the result
        result = query_db(query)
        # Extract dates and counts from the result
        dates = [row[0] for row in result]
        counts = [row[1] for row in result]
        # Return a JSON response with dates and counts
        return jsonify({"dates": dates, "counts": counts})
    except Exception as e:
        # Log errors for debugging
        logging.error("Error in /api/orders_over_time: %s", e)
        # Raise a 500 Internal Server Error with a description
        abort(500, description="Error processing data.")

# Define an API endpoint to retrieve products with low stock levels
@app.route("/api/low_stock_levels")
def low_stock_levels() -> Response:
    query = """
    SELECT p.product_name, s.quantity
    FROM stock_level s
    JOIN products p ON s.product_id = p.product_id
    ORDER BY s.quantity ASC;
    """
    # Execute the database query and retrieve the result
    result = query_db(query)

    # Extract product names and quantities from the result
    products = [row[0] for row in result]
    quantities = [row[1] for row in result]

    # Return a JSON response with products and quantities
    return jsonify({"products": products, "quantities": quantities})

# Define an API endpoint to retrieve most popular products
@app.route("/api/most_popular_products")
def most_popular_products_new() -> Response:
    query = """
    SELECT p.product_id, p.product_name, SUM(od.quantity_ordered) AS total_quantity
    FROM order_details od
    JOIN products p ON od.product_id = p.product_id
    GROUP BY p.product_id, p.product_name
    ORDER BY total_quantity DESC
    LIMIT 10;
    """
    # Execute the database query and retrieve the result
    result = query_db(query)

    # Create a list of dictionaries with product information
    products = [
        {"product_id": row[0], "product_name": row[1], "total_quantity": row[2]}
        for row in result
    ]

    # Return a JSON response with the list of products
    return jsonify(products)

# Define an API endpoint to retrieve revenue generation information
@app.route("/api/revenue_generation")
def revenue_generation() -> Response:
    query = """
    SELECT o.order_date, SUM(od.price_at_time * od.quantity_ordered) AS total_revenue
    FROM order_details od
    JOIN orders o ON od.order_id = o.order_id
    GROUP BY o.order_date
    ORDER BY o.order_date;
    """
    # Execute the database query and retrieve the result
    result = query_db(query)

    # Extract dates and revenues from the result
    dates = [row[0] for row in result]
    revenues = [row[1] for row in result]

    # Return a JSON response with dates and revenues
    return jsonify({"dates": dates, "revenues": revenues})

# Define an API endpoint to retrieve product category popularity information
@app.route("/api/product_category_popularity")
def product_category_popularity() -> Response:
    query = """
    SELECT pc.category_name, SUM(od.price_at_time * od.quantity_ordered) AS total_sales
    FROM products p
    JOIN product_categories pc ON p.category_id = pc.category_id
    JOIN order_details od ON p.product_id = od.product_id
    GROUP BY pc.category_name
    ORDER BY total_sales DESC;
    """
    # Execute the database query and retrieve the result
    result = query_db(query)

    # Extract category names and sales from the result
    categories = [row[0] for row in result]
    sales = [row[1] for row in result]

    # Return a JSON response with categories and sales
    return jsonify({"categories": categories, "sales": sales})

# Define an API endpoint to retrieve payment method popularity information
@app.route("/api/payment_method_popularity")
def payment_method_popularity() -> Response:
    query = """
    SELECT pm.method_name, COUNT(p.payment_id) AS transaction_count
    FROM payments p
    JOIN payment_methods pm ON p.method_id = pm.method_id
    GROUP BY pm.method_name
    ORDER BY transaction_count DESC;
    """
    # Execute the database query and retrieve the result
    result = query_db(query)

    # Extract payment methods and transaction counts from the result
    methods = [row[0] for row in result]
    counts = [row[1] for row in result]

    # Return a JSON response with payment methods and counts
    return jsonify({"methods": methods, "counts": counts})

# Run the application if this script is executed directly
if __name__ == "__main__":
    # Start the Flask application in debug mode
    app.run(debug=True)