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