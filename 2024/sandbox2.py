import tkinter as tk
from tkinter import ttk
import sqlite3

selected_values = []

def on_double_click(event):
    item = tree.item(tree.focus())  # Get the item that was double-clicked
    values = item['values']  # Get the values of the item
    selected_values.append(values)  # Append the values to the selected_values list
    update_labels()  # Update the labels with the selected values
    
    # Remove the selected item from the Treeview
    tree.delete(tree.focus())

def clear_selected_values():
    global selected_values
    
    # Remove the selected values from the Treeview
    for values in selected_values:
        item = tree.insert("", tk.END, values=values)
        tree.selection_add(item)
    
    selected_values = []  # Clear the selected_values list
    update_labels()  # Update the labels
    
    # Fetch data from the SQLite database
    cursor.execute("SELECT * FROM players")
    data = cursor.fetchall()
    
    # Clear the existing items from the Treeview
    tree.delete(*tree.get_children())
    
    # Insert new data into the Treeview
    for row in data:
        tree.insert("", tk.END, values=row)

def update_labels():
    # Clear the previous labels
    for label in label_list:
        label.config(text="")
    
    # Update the labels with the selected values
    for i, values in enumerate(selected_values):
        if i < len(label_list):
            label_list[i].config(text=values)

# Create the main window
root = tk.Tk()
root.title("Best Ball App")
root.geometry("1200x800")

conn = sqlite3.connect('prod_bestball_2024.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM players")
data = cursor.fetchall()




# Create a Treeview widget
tree = ttk.Treeview(root, selectmode="extended")  # Allow selecting multiple items
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
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

# Pack the Treeview and scrollbar
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Create labels to display the selected values
label_list = []
for _ in range(20):
    label = tk.Label(root, text="")
    label.pack()
    label_list.append(label)

# Create a button to clear the selected values
clear_button = tk.Button(root, text="Clear", command=clear_selected_values)
clear_button.pack()

# Set focus to the Treeview widget
tree.focus_set()

# Bind double-click event to the Treeview
tree.bind("<Double-1>", on_double_click)

# Adjust double-click timing
root.tk.call('after', 'idle', 'tk::mac::SetupDoubleButtonTime', 500)


cursor.execute("SELECT * FROM contests")
contest_data = cursor.fetchall()

# Create the Treeview for contests
contest_tree = ttk.Treeview(root, selectmode="extended")
contest_tree["columns"] = tuple(range(len(contest_data[0])))

column_names = [column[0] for column in cursor.description]

# Set the column names as Treeview headings for contests
contest_tree["show"] = "headings"
for i, column_name in enumerate(column_names):
    contest_tree.heading(i, text=column_name)

# Insert data into the contest Treeview
for row in contest_data:
    contest_tree.insert("", tk.END, values=row)

# Add a scrollbar to the contest Treeview
contest_scrollbar = ttk.Scrollbar(root, orient="vertical", command=contest_tree.yview)
contest_tree.configure(yscrollcommand=contest_scrollbar.set)

# Pack the contest Treeview and scrollbar
contest_tree.pack(side="left", fill="both", expand=True)
contest_scrollbar.pack(side="right", fill="y")

# Reposition and resize the players Treeview
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# Run the main event loop
root.mainloop()