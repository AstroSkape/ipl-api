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
        #print(rows)

        return jsonify(rows)

    # GET: Fetch team details by team_id
    @app.route('/<team_id>')
    def fetch_by_id(team_id=None):
        print(team_id)
        cur.execute("SELECT * FROM team where team_id = '"+team_id+"'")
        rows = cur.fetchall()
        print(rows)

        return jsonify(rows)

    # POST: Add entry to players table
    @app.route('/add-player', methods=['GET' ,'POST'])
    def add_movie():
        if request.method == 'POST':
            data = request.json
            print(data)
            cur.execute("INSERT INTO player values(%s, %s, %s, %s, %s, %s)", (f"{data['player_id']}", f"{data['pname']}", f"{data['team_id']}", f"{data['total_runs']}", f"{data['total_wickets']}", f"{data['net_economy']}"))
            con.commit()
            return "done"
        else:
            return "error"

    @app.route('/delete-sponsor', methods=['POST'])
    def del_sponsor():
        if request.method == 'POST':
            data = request.json
            cur.execute("DELETE FROM sponsors where sponsor = '"+data['sponsor']+"'")
            con.commit()
            return "done"
        else:
            return "dont get"

    @app.route('/update-venue', methods=['PUT'])
    def change_capacity():
        if request.method == 'PUT':
            cur.execute("UPDATE venue set capacity=capacity*2 where venue_id='V1'")
            con.commit()
            return "updated"
        else:
            return "put"

except:
    print('Error')

if __name__ == '__main__':
    app.run(debug=False)
