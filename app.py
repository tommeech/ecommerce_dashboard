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