from flask import *
from flask_cors import CORS
from flask import request
from dotenv import load_dotenv
import psycopg2
import os
#import pandas as pd

app = Flask(__name__)
CORS(app)

load_dotenv()

# PostgreSQL Database credentials loaded from the .env file
DATABASE = os.getenv('DATABASE')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')


try:
    con = psycopg2.connect(
        database=DATABASE,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD)

    cur = con.cursor()

    # GET: Fetch all movies from the database
    @app.route('/')
    def fetch_all_movies():
        cur.execute('SELECT * FROM player')
        rows = cur.fetchall()
        print(rows)

        return jsonify(rows)
except:
    print('Error')

if __name__ == '__main__':
    app.run(debug=False)
