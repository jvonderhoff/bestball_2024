import streamlit as st
import pandas as pd
import sqlite3

# Establish a connection to the SQLite database
conn = sqlite3.connect('/Users/jvonderhoff/Desktop/FantasyFootball/2024/prod_bestball_2024.db')

# Define your SQL queries
query = "SELECT * FROM DK_lineups"
query2 = "SELECT Name, Rank FROM players"

# Use Pandas to read data from the SQL queries into DataFrames
df_dk_lineups = pd.read_sql_query(query, conn)
df_players = pd.read_sql_query(query2, conn)

# Sidebar for filtering
st.sidebar.title('Draft Dashboard')
selected_lineup = st.sidebar.selectbox('Select Lineup ID:', df_dk_lineups['Lineup ID'])

# Display the selected lineup data
st.write(f'### Lineup ID: {selected_lineup}')
st.write(df_dk_lineups[df_dk_lineups['Lineup ID'] == selected_lineup])

# Show player details
st.write('### Players Information')
st.write(df_players)
