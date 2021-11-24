import sqlite3
from psycopg2 import connect, extensions, sql
import streamlit as st
import pandas as pd

def init_connection(u, p):
    conn_e = connect(
        dbname="ipl",
        user=u,
        host="localhost",
        password=p
    )
    return conn_e

def app():
    st.subheader("Read")
    # conn = init_connection(usr, pwd)
    # sql = "select * from matches"
    # with conn.cursor() as cur:
    #     st.subheader("Retrieve values")
    #     cur.execute(sql)
    #     rows = cur.fetchall()
    #     conn.commit()
    #     #df = pd.read_sql(sql, con=conn)
    #     st.table(rows)
    #     if(st.checkbox('Show table')):
    #         "yes"