import sqlite3
from psycopg2 import connect, extensions, sql
import streamlit as st
import pandas as pd
from apps import home, login, read

conn = ""
usr = ""
pwd = ""
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection(u, p):
    conn_e = connect(
        dbname="ipl",
        user=u,
        host="localhost",
        password=p
    )
    return conn_e

def read_values(usr, pwd):
    #st.subheader("Read")
    st.empty()
    conn = init_connection(usr, pwd)
    sql = "select * from matches"
    with conn.cursor() as cur:
        st.subheader("Retrieve values")
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        #df = pd.read_sql(sql, con=conn)
        st.table(rows)
        if(st.checkbox('Show table')):
            "yes"


st.title("IPL")

menu = ["Home", "Login", "Read"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Home")
    st.write("Welcome to the IPL Database!")
    st.write("Only RCB Wins here :)")

elif choice == "Login":
    st.subheader("Login Section")

    usr = st.text_input("User Name")
    pwd = st.text_input("Password", type='password')
    #sql = "select * from matches"
    secrets = {"staff_1a":'staff', "staff_1B":'staff', 'admin':'admin', "viewer":'see', 'postgres':'root'}
    # '''if usr == "":
    #     st.info("You do not have input user name yet")
    # elif pwd == "":
    #     st.info("You do not have input password yet")'''
    
    if usr in secrets and secrets[usr]==pwd:
        conn = init_connection(usr, pwd)
        try:
            l,m,r = st.columns(3)
            with l:
                st.button("READ")
            with m:
                st.button("UPDATE")
            with r:
                st.button("DELETE")
            # cur.execute(sql)
            # rows = cur.fetchall()
            # conn.commit()
            # #df = pd.read_sql(sql, con=conn)
            # if(st.checkbox('Show table')):
            #     st.table(rows)
            st.success("Login Successful")
        except:
            "Permission denied"
    elif usr=="" or pwd=="":
        st.warning("Enter your credentials")
    else:
        st.warning(
            "Sorry, you can not login in, please check your user name or password.")

elif choice == "Read":
    st.subheader("Read")
    conn = init_connection(usr, pwd)
    sql = "select * from matches"
    with conn.cursor() as cur:
        st.subheader("Retrieve values")
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        #df = pd.read_sql(sql, con=conn)
        st.table(rows)
        if(st.checkbox('Show table')):
            st.table(rows)
