import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("prod_2024.db")
cursor = conn.cursor()

# Execute the DELETE statement to remove null rows
cursor.execute("DELETE FROM players WHERE Id IS NULL")

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()