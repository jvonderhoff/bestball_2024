import csv
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('prod_bestball_2024.db')
cursor = conn.cursor()

try:
    # Read data from the CSV file and update the specified columns in the database
    with open('/Users/jvonderhoff/Downloads/Best-Ball-2024---DK-Ranks-1-2.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if it exists

        updated_records = []  # To store the records that will be updated

        for row in csv_reader:
            id_value = row[0]
            name_value = row[1]
            team_value = row[2]
            position_value = row[3]
            legup_rank_value = row[4]
            adp_value = row[6]

            # Check if the record already exists in the database
            cursor.execute('SELECT * FROM players WHERE Id = ? AND Name = ?', (id_value, name_value))
            existing_record = cursor.fetchone()

            if existing_record:
                # Print the existing record that will be updated
                print("Existing record:")
                print(existing_record)

                # Store the record that will be updated
                updated_records.append((id_value, name_value, legup_rank_value, adp_value))
            else:
                # Insert a new record if it doesn't already exist
                cursor.execute('INSERT INTO players (Id, Name, Position, Team, Wk17, Rank, Adp) VALUES (?, ?, ?, ?, ?, ?, ?)',
                               (id_value, name_value, position_value, team_value, None, legup_rank_value, adp_value))
                               

        # Prompt for user confirmation before performing the update
        confirmation = input("Do you want to proceed with the update? (y/n): ").lower()

        if confirmation == 'y':
            conn.execute('BEGIN TRANSACTION')
            # Update the rank and ADP columns for matching records
            for record in updated_records:
                id_value, name_value, legup_rank_value, adp_value = record
                cursor.execute('UPDATE players SET rank = ?, ADP = ? WHERE Id = ? AND Name = ?', (legup_rank_value, adp_value, id_value, name_value))

            # Commit the changes
            conn.commit()
            print("Changes have been committed.")
        else:
            print("Update operation cancelled.")

        # Print all records after the update
        cursor.execute('SELECT * FROM players')
        updated_records = cursor.fetchall()
        print("Updated records:")
        for record in updated_records:
            print(record)

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
finally:
    # Close the connection
    conn.close()