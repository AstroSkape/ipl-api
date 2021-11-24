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
        #print(tuple(df['tables']))
        #rows.rename(columns = {'2':'tables'}, inplace = True)
        option = st.selectbox("Choose table", options = tuple(df['tables']))
        cur.execute("select column_name from information_schema.columns where table_schema = 'public' and table_name='"+option+"'")
        col = [row[0] for row in cur]
        #print(col)
        #column_names = [row[0] for row in cur]
        cur.execute("Select * from "+option)
        df = pd.DataFrame(cur.fetchall())
        df.columns = col
        st.table(df)
        cur.close()
        con.close()

def remove(username, pw):
    if(username != 'admin'):
        st.warning("This user does not have permission to modify the relations")
    else:
        con = psycopg2.connect(
            host = 'localhost',
            database = 'ipl',
            user = 'postgres',
            password = 'postgres'
        )
        cur = con.cursor()
        
        cur.execute("select column_name from information_schema.columns where table_schema = 'public' and table_name='sponsors'")
        col = [row[0] for row in cur]
        #venue = st.text_input("Venue id")
        #tup = (df['venue_id'])
        to_delete = st.text_input("Enter the name of the sponsor to be deleted")
        click = st.button('Update', key=1)
        show = st.button('Show Table')
        cur.execute("select * from sponsors")
        df = pd.DataFrame(cur.fetchall())
        if(show):
            df.columns = col
            st.table(df)
        if(click):
            if(to_delete in df.values):
                sql = "delete from sponsors where sponsor='"+to_delete+"'"
                print(sql)
                cur.execute(sql)
                con.commit()
                print("Yes")
            else:
                st.warning('Entered sponsor does not exist')
        cur.close()
        con.close()

def update(username, pw):
    if(username != 'admin'):
        st.warning("This user does not have permission to modify the relations")
    else:
        con = psycopg2.connect(
            host = 'localhost',
            database = 'ipl',
            user = 'postgres',
            password = 'postgres'
        )
        cur = con.cursor()
        
        cur.execute("select column_name from information_schema.columns where table_schema = 'public' and table_name='venue'")
        col = [row[0] for row in cur]
        #venue = st.text_input("Venue id")
        #tup = (df['venue_id'])
        venue = st.selectbox("Choose venue", options = ('V1','V2','V3','V4','V5','V6'))
        val = st.text_input("Enter new capacity")
        click = st.button('Update', key=1)
        show = st.button('Show Table')
        if(show):
            cur.execute("select * from venue")
            df = pd.DataFrame(cur.fetchall())
            df.columns = col
            st.table(df)
        if(click):
            print("here")
            sql = "update venue set capacity="+val+" where venue_id='"+venue+"'"
            #val = st.text_input('Enter new capacity', value='')
            print(sql)
            cur.execute(sql)
            con.commit()
            #print(cur.fetchall())
            print("Yes")
        cur.close()
        con.close()

def simple_queries(username, pw):
    con = psycopg2.connect(
            host = 'localhost',
            database = 'ipl',
            user = 'postgres',
            password = 'postgres'
        )
    cur = con.cursor()
    queries = {'Leaderboard standings':'select team_id, number_of_wins*2 AS points FROM leaderboard order by points desc;',
                'Find number of losses':'select team_id, matches_played - number_of_wins AS number_of_losses FROM leaderboard;',
                'Team with most championships':'select team_name from team where championships_won = (select max(championships_won) from team);',
                'Players with more than 1000 runs and 2 wickets':'select player_id, pname from player where total_runs>1000 and total_wickets>2;',
                'Sponsors of team 1A':"select team_ID,sponsor from sponsors where Team_ID = '1A';"}
    option = st.selectbox("Choose query", options = queries)
    cur.execute(queries[option])
    df = pd.DataFrame(cur.fetchall())
    st.table(df)
    cur.close()
    con.close()


def complex_queries(username, pw):
    con = psycopg2.connect(
            host = 'localhost',
            database = 'ipl',
            user = 'postgres',
            password = 'postgres'
        )
    cur = con.cursor()
    queries = {'Players who played in match 3 but not match 1':"select pname from player where player_id in ((select player_ as player_id from players_on_the_field where match_id = '3') except (select player_ as player_id from players_on_the_field where match_id = '1'));",
                'Support staff of teams that played in match 1':"select staff_id, role from support_staff, matches where team_id=matches.winning_team and match_id='1' union select staff_id, role from support_staff, matches where team_id=matches.losing_team and match_id='1';",
                'Find the matches played between teams 1A and 1B in venue V3':"(select M_ID from played_in where V_ID ='V3') INTERSECT (select match_id from matches where (winning_team = '1A' and losing_team = '1B') or (winning_team ='1B' and losing_team = '1A')) ;",
                'Players from teams 2A and 3B who have scored more than 500 runs':"(select pname from player where team_ID = '2A' and total_runs > 500) UNION (select pname from player where team_ID = '3B' and total_runs > 500);",
                'Teams which have more than 1 win':"select team_name, team_id from team natural join (select team_id from leaderboard where number_of_wins > 1) as t;",
                'Players on the field of the winning team of match 1':"select pname from player inner join matches on winning_team=team_id and match_id='1' except select distinct(pname) from player as p inner join matches as m on winning_team=team_id and match_id ='1'  inner join players_on_the_field as potf on m.match_id=potf.match_id and potf.player_=p.player_id;"}
    option = st.selectbox("Choose query", options = queries)
    cur.execute(queries[option])
    df = pd.DataFrame(cur.fetchall())
    st.table(df)
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
page = st.sidebar.selectbox('Choose page', options=('read', 'delete', 'update','simple queries','complex queries'))
with ref:
    if passw == '' or option == '':
        st.warning('please enter password and username')
    else:
        try:
            if page == 'read':
                st.header('Team Details 🏏 ')
                team(option, passw)
            elif page == 'delete':
                st.header('Remove sponsor')
                remove(option, passw)
            elif page == 'update':
                st.header('Update Venue')
                update(option, passw)
            elif page == 'simple queries':
                st.header('Simple queries')
                simple_queries(option,passw)
            elif page == 'complex queries':
                st.header('Complex queries')
                complex_queries(option,passw)
        except psycopg2.errors.InFailedSqlTransaction as e:
            print(e)
        except psycopg2.OperationalError as e:
            print(e)
        except psycopg2.errors.InsufficientPrivilege as e:
            print(e)