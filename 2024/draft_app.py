from tkinter import *
from tkinter import ttk
import sqlite3
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

selected_values = []
# double click function
def on_double_click(event):
    item = my_tree.item(my_tree.focus())  # Get the item that was double-clicked
    values = item['values']  # Get the values of the item
    selected_values.append(values)  # Append the values to the selected_values list
    logging.info("Appended values: %s", values)  # Log the value
    update_labels()  # Update the labels with the selected values

    # Remove the selected item from the Treeview
    my_tree.delete(my_tree.focus())

def update_labels():
    # Clear the previous labels
    for label in label_list:
        label.config(text="")
    
    # Update the labels with the selected values
    for i, values in enumerate(selected_values):
        if i < len(label_list):
            formatted_data = f"{values[0]} {values[1]} {values[2]} {values[3]} {values[4]}"
            label_list[i].config(text=formatted_data)

    
    
contest_columns = ['Contest ID', 'Contest Name', 'Entry Fee', 'Site']  # Replace with your actual column names


def on_contest_select(*args):
    selected_contest_name = selected_contest.get()
    logging.info("selected_contest_name data: %s", selected_contest_name)  # Log the value
    selected_contest_data = next(row for row in contest_data if row[1] == selected_contest_name)
    logging.info("selected_contest_data data: %s", selected_contest_data)  # Log the value
    
    # Format the contest data
    formatted_data = "\n".join(f"{key}: {value}" for key, value in zip(contest_columns, selected_contest_data))
    

    # Update the label with the contest data
    contest_data_label.config(text=formatted_data)
'''
def show_selected_data():
    selected_contests = selected_contest.get()
    lineup = [f"Player Name: {values[0]}, Team: {values[1]}, Position: {values[2]}, Dk Rank: {values[3]}" for values in selected_values]
    message = f"Selected Contests: {selected_contests}\n\nLineup:\n" + "\n".join(lineup)
    messagebox.showinfo("Selected Data", message)
    logging.info("Message Box Lineup: %s", lineup)  # Log the value
    logging.info("Message Box Contest: %s", message)  # Log the value
'''
def add_new_lineup():
    # Create New Window
    add_lineup = Tk()
    add_lineup.title("Add Lineup")
    add_lineup.geometry("500x250")

    # Get Contests 
    selected_contest_name = selected_contest.get()
    selected_contest_data = next(row for row in contest_data if row[1] == selected_contest_name)
    
    # Get Date
    draft_date_display = draft_date.get()

    # Get pick
    draft_pick_display = draft_pick.get()

    # Generate UUID for Contest ID
    Lineup_ID = str(uuid.uuid4())

    review_lineup_data = []
    for values in selected_values:
        lineup_data = [
            Lineup_ID, values[0], values[1], values[2], values[3], 
            selected_contest_data[0], selected_contest_data[1], 
            selected_contest_data[2], selected_contest_data[3], draft_date_display, draft_pick_display
        ]
        review_lineup_data.append(lineup_data)

    '''
    # Get Lineup
    lineup = [f"LIneupId: {Lineup_ID} Player ID: {values[0]}, Player Name: {values[1]}, Team: {values[2]}, Position: {values[3]}, contest_ID: {selected_contest_data[0]}, Contest Name: {selected_contest_data[1]}, Contest Entry Fee: {selected_contest_data[2]}, Contest Site: {selected_contest_data[3]}, Draft Date: {draft_date_display}" for values in selected_values]
    '''

    '''
    data = f"Contest: {contest_name}\nLineup ID: {Lineup_ID} \n Draft Date: {draft_date_display}\nLineup:\n" + "\n".join(lineup)
    


    data = f"\n".join(lineup)
    

    label = Label(add_lineup, text=data)
    label.pack(padx=10, pady=10)
    '''


    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    lineup_treeview = ttk.Treeview(add_lineup, yscrollcomman=tree_scroll.set, selectmode=EXTENDED)
    lineup_treeview.pack()


    # Define the columns for the Treeview
    lineup_treeview["columns"] = ("lineup_ID", "player_ID", "player_name", "player_team", "player_position",
                        "contest_ID", "contest_name", "contest_fee", "contest_site", "draft_date", "draft_pick")

    # Format the columns
    lineup_treeview.column("#0", width=0, stretch=NO)
    lineup_treeview.column("lineup_ID", width=100, minwidth=100, stretch=NO)
    lineup_treeview.column("player_ID", width=100, minwidth=100, stretch=NO)
    lineup_treeview.column("player_name", width=100, minwidth=100, stretch=NO)
    lineup_treeview.column("player_team", width=100, minwidth=100, stretch=NO)
    lineup_treeview.column("player_position", width=100, minwidth=100, stretch=NO)
    lineup_treeview.column("contest_ID", width=100, minwidth=100, stretch=NO)
    lineup_treeview.column("contest_name", width=100, minwidth=100, stretch=NO)
    lineup_treeview.column("contest_fee", width=100, minwidth=100, stretch=NO)
    lineup_treeview.column("contest_site", width=100, minwidth=100, stretch=NO)
    lineup_treeview.column("draft_date", width=100, minwidth=100, stretch=NO)
    lineup_treeview.column("draft_pick", width=100, minwidth=100, stretch=NO)

    # Add column headings
    lineup_treeview.heading("#0", text="", anchor=W)
    lineup_treeview.heading("lineup_ID", text="lineup_ID", anchor=W)
    lineup_treeview.heading("player_ID", text="Player_ID", anchor=W)
    lineup_treeview.heading("player_name", text="player_name", anchor=W)
    lineup_treeview.heading("player_team", text="player_team", anchor=W)
    lineup_treeview.heading("player_position", text="player_position", anchor=W)
    lineup_treeview.heading("contest_ID", text="contest_id", anchor=W)
    lineup_treeview.heading("contest_name", text="contest_name", anchor=W)
    lineup_treeview.heading("contest_fee", text="contest_fee", anchor=W)
    lineup_treeview.heading("contest_site", text="contest_site", anchor=W)
    lineup_treeview.heading("draft_date", text="draft_date", anchor=W)
    lineup_treeview.heading("draft_pick", text="draft_pick", anchor=W)

    # Insert data into the Treeview
    for data in review_lineup_data:
        lineup_treeview.insert("", END, text=data[0], values=data[0:])

    # Create the button widget
    submit_button = Button(add_lineup, text="Submit", command=submit_action)

    # Pack the button widget
    submit_button.pack(pady=10)
    

def submit_action():
    
    # Get Contests
    selected_contest_name = selected_contest.get()
    selected_contest_data = next(row for row in contest_data if row[1] == selected_contest_name)
    
    # Get Date
    draft_date_display = draft_date.get()

    # Get pick
    draft_pick_display = draft_pick.get()

    # Generate UUID for Contest ID
    Lineup_ID = str(uuid.uuid4())
    
    final_lineup_data = []
    for values in selected_values:
        lineup_data = [
            Lineup_ID, values[0], values[1], values[2], values[3], 
            selected_contest_data[0], selected_contest_data[1], 
            selected_contest_data[2], selected_contest_data[3], draft_date_display, draft_pick_display
        ]
        final_lineup_data.append(lineup_data)
        logging.info("final_lineup_data data: %s", lineup_data)  # Log the value
    
    conn = sqlite3.connect('prod_bestball_2024.db')
    cursor = conn.cursor()
    
    cursor.executemany('INSERT INTO lineups VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', final_lineup_data)
    
    # Commit the transaction
    conn.commit()
    
    # Close the database connection
    conn.close()

# Create the main window
root = Tk()
root.title("Lineups")
root.geometry("2000x1000")


# Connect to database
conn = sqlite3.connect('prod_bestball_2024.db')
cursor = conn.cursor()

# Get data from players table
cursor.execute("SELECT rowid, * FROM players")
player_data = cursor.fetchall()

# Get contests from contests
cursor.execute("SELECT * FROM contests")
contest_data = cursor.fetchall()
contest_names = [row[1] for row in contest_data]
formatted_contest_names = ', '.join(str(value) for value in contest_names)


selected_contest = StringVar()
contest_optionmenu = OptionMenu(root, selected_contest , formatted_contest_names)
contest_optionmenu.pack(padx=50, pady=50)

# Create date textbox
draft_date = Entry(root, width=10)
draft_date.pack(padx=10, pady=10)

# Create pick textbox
draft_pick = Entry(root, width=10)
draft_pick.pack(padx=10, pady=10)


# Add some Style
style = ttk.Style()

# Pick A Theme
style.theme_use('default')

# Configure the Treeview Colors
style.configure('Treeview',
                backgroud="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackgroud="#D3D3D3")

# Change Selected Color
style.map('Treeview',
          background=[('selected', "#347083")])

# Create a Treeview Scrollbar
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Create a Treeview Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create The Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcomman=tree_scroll.set, selectmode=EXTENDED)
my_tree.pack()

# Configure the Scrollbar
tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ("ID", "Player Name", "Team", "Position","Dk Rank")

# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=50)
my_tree.column("Player Name", anchor=W, width=240)
my_tree.column("Team", anchor=W, width=140)
my_tree.column("Position", anchor=W, width=140)
my_tree.column("Dk Rank", anchor=W, width=140)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("Player Name", text="Player Name", anchor=W)
my_tree.heading("Team", text="Team", anchor=W)
my_tree.heading("Position", text="Position", anchor=W)
my_tree.heading("Dk Rank", text="Dk Rank", anchor=W)

'''
# Add Fake Data
data = [
    ["Jared Goff", "Det", "QB"],
    ["Tyreek Hill", "MIA", "WR"],
    ["Sam Laporta", "Det", "TE"],
    ["Raheem Moestart", "MIA", "RB"]
]
'''

# Create Striped Row Tags
my_tree.tag_configure('rest', background="White")
my_tree.tag_configure('qb', background="orange")
my_tree.tag_configure('rb', background="lightblue")
my_tree.tag_configure('WR', background="lightgreen")
my_tree.tag_configure('TE', background="lightyellow")

# Add our data to the screen
global count
count = 0

'''
for record in data:
    if count % 2 == 0: 
        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3]), tags=('evenrow',))
    else:
        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2], record[3]), tags=('oddrow',))
    #increment counter
    count += 1
'''
for record in player_data:
    if record[3] == "QB":
        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3],record[4]), tags=('qb',))
    elif record[3] == "RB":
        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3],record[4]), tags=('rb',))
    elif record[3] == "WR":
        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3],record[4]), tags=('WR',))
    elif record[3] == "TE":
        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3],record[4]), tags=('TE',))
    else:
        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3],record[4]), tags=('rest',))
    #increment counter
    count += 1



# Add Selection area
data_frame = LabelFrame(root, text="Lineup")
data_frame.pack(fill="x", expand="yes", padx=20)


contest_data_label = Label(data_frame, text="") 
contest_data_label.grid()


selected_contest.trace('w', on_contest_select)



# Create labels to display the selected values
label_list = []
for _ in range(20):
    label = Label(data_frame, text="")
    label.grid()
    label_list.append(label)



button = Button(root, text="Show Selected Data", command=add_new_lineup)
button.pack(pady=10)



# Bind double-click event to the Treeview
my_tree.bind("<Double-1>", on_double_click)

# Run the main event loop
root.mainloop()






