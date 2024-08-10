import streamlit as st
import pandas as pd
import sqlite3
import numpy as np

# Establish a connection to the SQLite database
conn = sqlite3.connect('/Users/jvonderhoff/Desktop/FantasyFootball/2024/prod_bestball_2024.db')

# Define SQL queries to get player rankings and player frequencies in lineups
query_players = "SELECT Name, Rank, Team FROM players ORDER BY Rank"
query_lineups = "SELECT DISTINCT lineup_ID, player_name, player_team FROM DK_lineups"

# Read data from the SQL queries into DataFrames
df_players_ranked = pd.read_sql_query(query_players, conn)
df_lineups = pd.read_sql_query(query_lineups, conn)

# Count the frequency of each player in lineups
player_counts = df_lineups['player_name'].value_counts().reset_index()
player_counts.columns = ['Player', 'Frequency']

# Merge player counts with player rankings
player_ranking = pd.merge(df_players_ranked, player_counts, left_on='Name', right_on='Player', how='left')

# Calculate the percentage of lineups each player is in based on unique lineup_IDs
total_unique_lineups = len(df_lineups['lineup_ID'].unique())
player_ranking['Percentage'] = (player_ranking['Frequency'] / total_unique_lineups) * 100
player_ranking['Percentage'] = player_ranking['Percentage'].map("{:.0f}%".format)

# Function to apply color based on percentage
def color_percentage(val):
    if pd.isna(val) or val == 'nan':
        return 'background-color: red'
    
    try:
        percentage = int(float(val[:-1])) if '%' in val else 0
    except ValueError:
        return 'background-color: red'
    
    if percentage >= 10.01:
        return 'background-color: lightgreen'
    elif 6 <= percentage <= 10:
        return 'background-color: orange'
    else:
        return 'background-color: red'

# Apply color based on percentage
styled_player_ranking = player_ranking.style.applymap(color_percentage, subset=['Percentage'])

# Tabs for Player Selection and Player Table
tabs = st.radio("View", ["Main Page", "Player Selection", "Player Stacking"])

if tabs == "Main Page":

    # Main Page
    st.write('## Exposure')

    # Display the styled player ranking
    st.write(styled_player_ranking)
    
elif tabs == "Player Selection":
    st.write('## Player Selection Page')
    selected_player = st.sidebar.selectbox("Select a player", player_ranking['Name'])

    player_lineup_ids = df_lineups[df_lineups['player_name'] == selected_player]['lineup_ID'].unique()

    st.write(f"### Lineups that {selected_player} is in")
    for lineup_id in player_lineup_ids:
        lineup_players = df_lineups[df_lineups['lineup_ID'] == lineup_id]['player_name'].unique()
        st.write(f"**Lineup ID: {lineup_id}**")
        st.write(lineup_players)

    st.write(f"### Players and their frequency in lineups with {selected_player}")
    player_frequency_with_selected = df_lineups[df_lineups['lineup_ID'].isin(player_lineup_ids)]['player_name'].value_counts().reset_index()
    player_frequency_with_selected.columns = ['Player', 'Frequency']
    st.write(player_frequency_with_selected)


elif tabs == "Player Stacking":
    st.write('## Player Stacking Page')
    selected_player = st.sidebar.selectbox("Select a player", player_ranking['Name'])

    # Get the team of the selected player from the players table
    selected_player_team = player_ranking[player_ranking['Name'] == selected_player]['Team'].values[0]

    # Get unique lineup IDs where the selected player is present
    player_lineup_ids = df_lineups[df_lineups['player_name'] == selected_player]['lineup_ID'].unique()

    st.write(f"### Linkages for {selected_player} with players on the same team")
    for lineup_id in player_lineup_ids:
        lineup_players_same_team = df_lineups[(df_lineups['lineup_ID'] == lineup_id) & (df_lineups['player_name'] != selected_player) & (df_lineups['player_team'] == selected_player_team)]['player_name'].unique()
        
        st.write(f"**Lineup ID: {lineup_id}**")
        st.write(lineup_players_same_team)

    st.write("*Note: The above list shows players on the same team as the selected player in each lineup.*")