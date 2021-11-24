from psycopg2 import connect, extensions, sql
import streamlit as st
import pandas as pd


secrets = {"staff_1a":'staff', "staff_1B":'staff', 'admin':'admin', "viewer":'see', 'postgres':'root'}
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection(u, p):
    conn_e = connect(
        dbname="ipl",
        user=u,
        host="localhost",
        password=p
    )
    return conn_e

def app():
    st.subheader("Login Section")
    usr = st.text_input("User Name")
    pwd = st.text_input("Password", type='password')
    secrets = {"staff_1a":'staff', "staff_1B":'staff', 'admin':'admin', "viewer":'see', 'postgres':'root'}
   
    if usr in secrets and secrets[usr]==pwd:
        try:
            l,m,r = st.columns(3)
            with l:
                st.button("READ")#, on_click=read_values, args=(usr, pwd))
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