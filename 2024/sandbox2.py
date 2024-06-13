from tkinter import *
from tkinter import ttk
import sqlite3
import uuid
import logging
from tkinter import messagebox


# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def select_row(event):
    selected_item = my_tree.focus()
    # Retrieve the values of the selected row
    values = my_tree.item(selected_item, 'values')
    if values:
        print("Selected row:", values)


# Create the main window
root = Tk()
root.title("Lineups")
root.geometry("1500x1000")


# Connect to database
conn = sqlite3.connect('prod_bestball_2024.db')
cursor = conn.cursor()

# Get data from players table
cursor.execute("SELECT * FROM players")
player_data = cursor.fetchall()


 # Commit the transaction
conn.commit()
    
# Close the database connection
conn.close()


# Add some Style
style = ttk.Style()

# Pick A Theme
style.theme_use('default')

# Configure the Treeview Colors
style.configure('Treeview',
                backgroud="#D3D3D3",
                foreground="black",
                rowheight=100,
                fieldbackgroud="#D3D3D3")

# Change Selected Color
style.map('Treeview',
          background=[('selected', "#347083")])

# Create a Treeview Scrollbar
tree_frame = Frame(root)
tree_frame.grid(pady=10, row=5, column=1)

# Create a Treeview Scrollbar
tree_scroll = Scrollbar(root)
tree_scroll.grid(row=0, column=1, sticky="ns")

# Create The Treeview
my_tree = ttk.Treeview(root, yscrollcommand=tree_scroll.set, selectmode=BROWSE)
my_tree.grid(row=0, column=0, sticky="nsew")

tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ("ID", "Player Name", "Position", "Team", "wk17","Dk Rank", "Dk ADP")

# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=100)
my_tree.column("Player Name", anchor=W, width=200)
my_tree.column("Position", anchor=W, width=70)
my_tree.column("Team", anchor=W, width=70)
my_tree.column("wk17", anchor=W, width=70)
my_tree.column("Dk Rank", anchor=W, width=70)
my_tree.column("Dk ADP", anchor=W, width=70)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("Player Name", text="Player Name", anchor=W)
my_tree.heading("Position", text="Position", anchor=W)
my_tree.heading("Team", text="Team", anchor=W)
my_tree.heading("wk17", text="wk17", anchor=W)
my_tree.heading("Dk Rank", text="Dk Rank", anchor=W)
my_tree.heading("Dk ADP", text="Dk ADP", anchor=W)


# Create Striped Row Tags
my_tree.tag_configure('rest', background="White")
my_tree.tag_configure('qb', background="orange")
my_tree.tag_configure('rb', background="lightblue")
my_tree.tag_configure('WR', background="lightgreen")
my_tree.tag_configure('TE', background="lightyellow")

# Add our data to the screen
global count
count = 0

tag_mapping = {
    "QB": "qb",
    "RB": "rb",
    "WR": "WR",
    "TE": "TE",
}

data = []
for record in player_data:
    tag = tag_mapping.get(record[2], "rest")
    values = (record[0], record[1], record[2], record[3], record[4], record[5], record[6])
    data.append((count, values, tag))
    count += 1
    logging.info("record: %s", record)

# Insert the data into the Treeview widget
for item in data:
    my_tree.insert(parent='', index='end', iid=item[0], text='', values=item[1], tags=(item[2],))


# Bind the row selection event to the Treeview widget
my_tree.bind("<<TreeviewSelect>>", select_row)





# Run the main event loop
root.mainloop()
