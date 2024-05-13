import tkinter as tk
from tkinter import ttk
import sqlite3
import logging

# Configure logging
logging.basicConfig(filename='update.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def add_row():
    new_values = [entry.get() for entry in entry_fields]

    # Insert the new row into the database
    cursor.execute("INSERT INTO players (Id, Name, Position, Team) VALUES (?, ?, ?, ?)",
                   (new_values[0], new_values[1], new_values[2], new_values[3]))

    # Get the ID of the newly inserted row
    row_id = cursor.lastrowid

    # Update the Treeview with the new row
    tree.insert("", tk.END, values=(row_id, *new_values))

    # Clear the entry fields
    for entry in entry_fields:
        entry.delete(0, tk.END)
    
    # Log the Add
    log_message = f"Add player: Id={new_values[0]}, Name={new_values[1]}, Position={new_values[2]}, Team={new_values[3]}"
    logging.info(log_message)

def edit_row():
    selected_item = tree.focus()
    if selected_item:
        item_values = tree.item(selected_item)["values"]

        # Show the selected values in the entry fields
        #for i, value in enumerate(item_values[1:], start=1):  # Exclude the first value
        #    entry_fields[i].delete(0, tk.END)
        #    entry_fields[i].insert(0, value)

        new_values = [entry.get() for entry in entry_fields[1:]]  # Exclude the first entry field

        # Update the database with the new values
        cursor.execute("UPDATE players SET Name=?, Position=?, Team=? WHERE Id=?",
                       (*new_values, item_values[0]))

        # Commit the changes to the database
        conn.commit()

        # Update the values in the tree view
        tree.item(selected_item, values=(item_values[0], *new_values))

        # Log the update
        log_message = f"Updated player: Id={item_values[0]}, Name={new_values[0]}, Position={new_values[1]}, Team={new_values[2]}"
        logging.info(log_message)
    
def delete_row():
    selected_item = tree.focus()
    if selected_item:
        item_values = tree.item(selected_item)["values"]

        # Delete the row from the database
        cursor.execute("DELETE FROM players WHERE id=?", (item_values[0],))

        # Commit the changes to the database
        conn.commit()

        # Remove the item from the Treeview
        tree.delete(selected_item)

        # Clear the entry fields
        for entry in entry_fields:
            entry.delete(0, tk.END)


# Create the main window
root = tk.Tk()
root.title("Best Ball App")
root.geometry("1200x800")

# Create a Notebook widget
tab_control = ttk.Notebook(root)
tab_control.pack(fill=tk.BOTH, expand=True)

# Create Tab 1
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Tab 1")



# Create Players Tab 
players_tab = ttk.Frame(tab_control)
tab_control.add(players_tab, text="Players")

conn = sqlite3.connect('prod_2024.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM players")
data = cursor.fetchall()

# Create a Treeview widget
tree = ttk.Treeview(players_tab)
tree["columns"] = tuple(range(len(data[0])))  # Assuming each row has the same number of columns

column_names = [column[0] for column in cursor.description]

# Set the column names as Treeview headings
tree["show"] = "headings"
for i, column_name in enumerate(column_names):
    tree.heading(i, text=column_name)


# Insert data into the Treeview
for row in data:
    tree.insert("", tk.END, values=row)

# Add a scrollbar to the Treeview
scrollbar = ttk.Scrollbar(players_tab, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

# Pack the Treeview and scrollbar
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Create entry fields for data editing
entry_fields = []
# Create labels and entry fields
for i, column_name in enumerate(column_names):
    label = tk.Label(players_tab, text=column_name)
    label.pack(side=tk.TOP)
    entry = tk.Entry(players_tab)
    entry.pack(side=tk.TOP)
    entry_fields.append(entry)

# Disable an entry field based on its name
#column_name_to_disable = "Id"
#index_to_disable = column_names.index(column_name_to_disable)
#entry_fields[index_to_disable].config(state=tk.DISABLED)

# Create Add, Edit, and Delete buttons
add_button = tk.Button(players_tab, text="Add", command=add_row)
add_button.pack(side=tk.TOP)

edit_button = tk.Button(players_tab, text="Edit", command=edit_row)
edit_button.pack(side=tk.TOP)

delete_button = tk.Button(players_tab, text="Delete", command=delete_row)
delete_button.pack(side=tk.TOP)


# Run the main event loop
root.mainloop()


