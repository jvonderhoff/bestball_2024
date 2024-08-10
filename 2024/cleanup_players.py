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

        records_to_update = []  # To store the records that will be updated

        for row in csv_reader:
            id_value = row[0]
            name_value = row[1]
            team_value = row[2]
            position_value = row[3]

            # Check if the record has a NULL Position
            cursor.execute('SELECT * FROM players WHERE Position IS NULL AND Name = ?', (name_value,))
            record = cursor.fetchone()

            if record:
                current_position = record[2]  # Assuming the position column is at index 2 in the record
                current_team = record[3]  # Assuming the team column is at index 3 in the record

                # Print the record and the values it will be updated to
                print("Record to be updated:")
                print(f"Name: {name_value}, Current Position: {current_position}, Current Team: {current_team}")
                print(f"New Position: {position_value}, New Team: {team_value}")

                records_to_update.append((name_value, position_value, team_value))

        # Ask for user confirmation before updating
        confirmation = input("Do you want to proceed with the update? (y/n): ").lower()

        if confirmation == 'y':
            conn.execute('BEGIN TRANSACTION')
            for record in records_to_update:
                name, position, team = record
                cursor.execute('UPDATE players SET Position = ?, Team = ? WHERE Name = ?', (position, team, name))
            
            conn.commit()
            print("Updates have been committed.")
        else:
            print("Update operation cancelled.")

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
finally:
    # Close the connection
    conn.close()