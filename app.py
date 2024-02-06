# Import necessary libraries and modules
from flask import Flask, jsonify, render_template, Response, abort, make_response
import sqlite3
import pathlib
import logging
import requests  # Importing the requests library

# Setup logging to log errors and debug information to a file
logging.basicConfig(filename="app.log", level=logging.DEBUG)

# Get the absolute path of the directory containing the script
working_directory = pathlib.Path(__file__).parent.absolute()

# Define the path to the SQLite database
DATABASE = working_directory / "CCL_ecommerce.db"


# Function to execute a database query and return the result
def query_db(query: str, args=()) -> list:
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, args).fetchall()
        return result
    except sqlite3.Error as e:
        # Log any database errors and raise an HTTP 500 error with a description
        logging.error("Database error: %s", e)
        abort(500, description="Database error occurred.")


# Create a Flask web application instance
app = Flask(__name__)


# Error handler for HTTP 404 Not Found
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


# Error handler for HTTP 500 Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({"error": "Internal server error"}), 500)


# Route for the root URL ("/"), returns the rendered template "dashboard.html"
@app.route("/")
def index() -> str:
    return render_template("dashboard.html")


# Route for fetching temperature data over time from an external API
@app.route("/api/temperature_over_time", methods=["GET"])
def temperature_over_time():
    # Fetching the date range from the local database
    query = """
SELECT MIN(order_date), MAX(order_date)
FROM orders;
"""
    try:
        result = query_db(query)
        start_date, end_date = result[0]

        # Making an API call to fetch temperature data
        API_ENDPOINT = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": 50.6053,  # London UK
            "longitude": -3.5952,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "temperature_2m_max",
            "timezone": "GMT",
        }
        response = requests.get(API_ENDPOINT, params=params)
        response.raise_for_status()

        # Return the JSON response from the external API
        return jsonify(response.json())
    except Exception as e:
        # Log any errors and raise an HTTP 500 error with a description
        logging.error("Error in /api/temperature_over_time: %s", e)
        abort(500, description="Error fetching temperature data.")


# Route for fetching order data over time from the local database
@app.route("/api/orders_over_time")
def orders_over_time() -> Response:
    query = """
    SELECT order_date, COUNT(order_id) AS num_orders
    FROM orders
    GROUP BY order_date
    ORDER BY order_date;
    """
    try:
        result = query_db(query)
        dates = [row[0] for row in result]
        counts = [row[1] for row in result]
        return jsonify({"dates": dates, "counts": counts})
    except Exception as e:
        # Log any errors and raise an HTTP 500 error with a description
        logging.error("Error in /api/orders_over_time: %s", e)
        abort(500, description="Error processing data.")


# Route for fetching products with low stock levels from the local database
@app.route("/api/low_stock_levels")
def low_stock_levels() -> Response:
    # SQL query to retrieve product names and quantities with low stock levels
    query = """
    SELECT p.product_name, s.quantity
    FROM stock_level s
    JOIN products p ON s.product_id = p.product_id
    ORDER BY s.quantity ASC;
    """
    # Execute the query and retrieve the results
    result = query_db(query)

    # Extract product names and quantities from the query result
    products = [row[0] for row in result]
    quantities = [row[1] for row in result]

    # Return the results in JSON format
    return jsonify({"products": products, "quantities": quantities})


# Route for fetching the most popular products from the local database
@app.route("/api/most_popular_products")
def most_popular_products_new() -> Response:
    # SQL query to retrieve the most popular products based on order quantity
    query = """
    SELECT p.product_id, p.product_name, SUM(od.quantity_ordered) AS total_quantity
    FROM order_details od
    JOIN products p ON od.product_id = p.product_id
    GROUP BY p.product_id, p.product_name
    ORDER BY total_quantity DESC
    LIMIT 10;
    """
    # Execute the query and retrieve the results
    result = query_db(query)

    # Format the results into a list of dictionaries
    products = [
        {"product_id": row[0], "product_name": row[1], "total_quantity": row[2]}
        for row in result
    ]

    # Return the results in JSON format
    return jsonify(products)


# Route for fetching revenue generation data from the local database
@app.route("/api/revenue_generation")
def revenue_generation() -> Response:
    # SQL query to retrieve revenue data based on order details
    query = """
    SELECT o.order_date, SUM(od.price_at_time * od.quantity_ordered) AS total_revenue
    FROM order_details od
    JOIN orders o ON od.order_id = o.order_id
    GROUP BY o.order_date
    ORDER BY o.order_date;
    """
    # Execute the query and retrieve the results
    result = query_db(query)

    # Extract dates and corresponding revenues from the query result
    dates = [row[0] for row in result]
    revenues = [row[1] for row in result]

    # Return the results in JSON format
    return jsonify({"dates": dates, "revenues": revenues})


# Route for fetching product category popularity data from the local database
@app.route("/api/product_category_popularity")
def product_category_popularity() -> Response:
    # SQL query to retrieve product category sales data
    query = """
    SELECT pc.category_name, SUM(od.price_at_time * od.quantity_ordered) AS total_sales
    FROM products p
    JOIN product_categories pc ON p.category_id = pc.category_id
    JOIN order_details od ON p.product_id = od.product_id
    GROUP BY pc.category_name
    ORDER BY total_sales DESC;
    """
    # Execute the query and retrieve the results
    result = query_db(query)

    # Extract categories and corresponding sales from the query result
    categories = [row[0] for row in result]
    sales = [row[1] for row in result]

    # Return the results in JSON format
    return jsonify({"categories": categories, "sales": sales})


# Route for fetching payment method popularity data from the local database
@app.route("/api/payment_method_popularity")
def payment_method_popularity() -> Response:
    # SQL query to retrieve payment method popularity data
    query = """
    SELECT pm.method_name, COUNT(p.payment_id) AS transaction_count
    FROM payments p
    JOIN payment_methods pm ON p.method_id = pm.method_id
    GROUP BY pm.method_name
    ORDER BY transaction_count DESC;
    """
    # Execute the query and retrieve the results
    result = query_db(query)

    # Extract payment methods and corresponding transaction counts
    methods = [row[0] for row in result]
    counts = [row[1] for row in result]

    # Return the results in JSON format
    return jsonify({"methods": methods, "counts": counts})


# Start the Flask application if this script is executed directly
if __name__ == "__main__":
    # Run the app in debug mode
    app.run(debug=True)