from flask import Flask, jsonify, render_template, Response
import sqlite3
import pathlib

working_directory = pathlib.Path(__file__).parent.absolute()
DATABASE = working_directory / 'CCL_ecommerce.db'

def query_db(query: str, args=()) -> list:
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor ()
        result = cursor.execute (query, args).fetchall()
    return result

app = Flask(__name__)

@app.route('/')
def index() -> str:
    return render_template('dashboard.html')

@app.route("/api/orders_over_time")
def orders_over_time() -> Response:

    query = """
    SELECT order_date, COUNT(order_id) AS num_orders
    FROM orders
    GROUP BY order_date
    ORDER BY order_date;
    """

    result = query_db(query)

    dates = [row[0] for row in result]
    counts = [row[1] for row in result]
    return jsonify({"dates": dates, "counts": counts})

@app.route("/api/low_stock_levels")
def low_stock_levels() -> Response:

    query = """
    SELECT p.product_name, s.quantity
    FROM stock_level s
    JOIN products p ON s.product_id = p.product_id
    ORDER BY s.quantity ASC;
    """

    result = query_db(query)

    products = [row[0] for row in result]
    quantities = [row[1] for row in result]
    return jsonify({"products": products, "quantities": quantities})


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

    result = query_db(query)

    products = [
        {"product_id": row[0], "product_name": row[1], "total_quantity": row[2]}
        for row in result
    ]
    return jsonify(products)

if __name__ == '__main__': #Will check that app.py is being run directly and not imported elsewhere
    app.run(debug=False) #Will run server in debug mode. This allows for real time code changing without needing to restart the server each time. Not to be used in a production environment due to security risks