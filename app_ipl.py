#from psycopg2 import connect, extensions, sql, OperationalError, errors
import psycopg2
import streamlit as st
import pandas as pd

global LOGGED_IN_AS
LOGGED_IN_AS = 'casual'

def team(username, pw):
    if(username!="" and pw!=""):
        con = psycopg2.connect(
            host = 'localhost',
            database = 'ipl',
            user = username,
            password = pw
        )
        cur = con.cursor()
        cur.execute("select table_name from information_schema.tables where table_schema = 'public';")
        df = cur.fetchall()
        df = pd.DataFrame(df)
        df.columns = ["tables"]
        print(tuple(df['tables']))
        #rows.rename(columns = {'2':'tables'}, inplace = True)
        option = st.selectbox("Choose table", options = tuple(df['tables']))
        cur.execute("select column_name from information_schema.columns where table_schema = 'public' and table_name='"+option+"'")
        col = [row[0] for row in cur]
        print(col)
        #column_names = [row[0] for row in cur]
        cur.execute("Select * from "+option)
        df = pd.DataFrame(cur.fetchall())
        df.columns = col
        st.table(df)
        cur.close()
        con.close()

def remove(username, pw):
    if(username!="" and pw!=""):
        con = psycopg2.connect(
            host = 'localhost',
            database = 'ipl',
            user = username,
            password = pw
        )
        cur = con.cursor()
        cur.execute("select * from information_schema.tables where table_schema = 'public';")
        

        cur.close()
        con.close()


def login(username, pw):
    '''Login using role new_user'''
    try:
        if(username!="" and pw!=""):
            con = psycopg2.connect(
                host = 'localhost',
                database = 'ipl',
                user = username,
                password = pw
            )
            ROLE = username
            st.sidebar.info('\tlogged in as ' + ROLE)
            con.close()
            return True
    except psycopg2.OperationalError as e:
        st.sidebar.warning('\tnot logged in')
        st.error(e)
        return False

title = st.container()
title.title('Welcome to IPL DB')
with st.sidebar.form(key='loginform', clear_on_submit=False):
    option = st.sidebar.selectbox('Choose user', options=('', 'staff_1a','staff_1b', 'admin', 'viewer'), key='username')
    passw = st.sidebar.text_input('password',placeholder=f'enter password for {option}', type='password')
    st.sidebar.button('sign in', key='login')
ref = st.container()
login(option, passw)
page = st.sidebar.selectbox('Choose page', options=('read', 'delete', 'update'))
with ref:
    if passw == '' or option == '':
        st.warning('please enter password and username')
    else:
        try:
            if page == 'read':
                st.header('Team Details 🏏 ')
                team(option, passw)
            if page == 'delete':
                st.header('Remove player')
                remove(option, passw)
        except psycopg2.errors.InFailedSqlTransaction as e:
            pass
        except psycopg2.OperationalError:
            pass
        except psycopg2.errors.InsufficientPrivilege:
            pass