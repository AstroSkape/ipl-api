import sqlite3
from psycopg2 import connect, extensions, sql
import streamlit as st
import pandas as pd


@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    conn_e = connect(
        dbname="ipl",
        user="postgres",
        host="localhost",
        password="ramya"
    )
    return conn_e


conn = init_connection()

st.title("IPL")

menu = ["Home", "Login"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Home")
    st.write("Welcome to the IPL Database!")
    st.write("Only RCB Wins here :)")

elif choice == "Login":
    st.subheader("Login Section")

    username = st.text_input("User Name")
    pwd = st.text_input("Password", type='password')
    sql = "select * from pwd"
    with conn.cursor() as cur:
        cur.execute(sql)
        cur.fetchall()
        conn.commit()
        df = pd.read_sql(sql, con=conn)
        if username == "":
            st.info("You do not have input user name yet")
        elif pwd == "":
            st.info("You do not have input password yet")
        else:
            if username in df.values and pwd in df.values:
                st.success("Welcome back")
            else:
                st.warning(
                    "Sorry, you can not login in, please check your user name or password.")
