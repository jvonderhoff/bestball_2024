from tkinter import *
from tkinter import ttk
import sqlite3

'''
import tkinter as tk
from tkinter import ttk
import sqlite3
'''

# Create Function to Delete a Record
def delete():

    conn = sqlite3.connect('prod_bestball_2024.db')
    cursor = conn.cursor()

    # Delete a record
    cursor.execute("DELETE from players WHERE Name = " + delete_box.get())

    # Commit Changes
    conn.commit()

    # Close Connection
    conn.close()

    delete_box.delete(0, END)



def submit():

    conn = sqlite3.connect('prod_bestball_2024.db')
    cursor = conn.cursor()

    # Insert Into Table
    cursor.execute("INSERT INTO PLAYERS VALUES (:id, :name, :team, :position)",
                   {
                       'id': id.get(),
                       'name': name.get(),
                       'team': team.get(),
                       'position': postion.get()
                       
                   })

    # Commit Changes
    conn.commit()

    # Close Connection
    conn.close()

    # Clear The Text Boxes
    id.delete(0, END)
    name.delete(0, END)
    team.delete(0, END)
    postion.delete(0, END)

# Create the main window
root = Tk()
root.title("Player Management")
root.geometry("1200x800")

# Create Text Boxes
id = Entry(root, width=30)
id.grid(row=0, column=1, padx=20)
name = Entry(root, width=30)
name.grid(row=1, column=1, padx=20)
team = Entry(root, width=30)
team.grid(row=2, column=1)
postion = Entry(root, width=30)
postion.grid(row=3, column=1)
delete_box = Entry(root, width=30)
delete_box.grid(row=4, column=1)

# Create Text Box Label
id_label = Label(root, text="ID")
id_label.grid(row=0, column=0)
name_label = Label(root, text="Name")
name_label.grid(row=1, column=0)
team_label = Label(root, text="Team")
team_label.grid(row=2, column=0)
postion_label = Label(root, text="Postion")
postion_label.grid(row=3, column=0)
delete_label = Label(root, text="OID")
delete_label.grid(row=4, column=0)

# Create Submit Button
submit_btn = Button(root, text="Add Player", command=submit)
submit_btn.grid(row=6, column=1)

# Create Delete Button
delete_btn = Button(root, text="Delete Player", command=delete)
delete_btn.grid(row=7, column=1)

# Drop Down Box
pos_drop = ttk.Combobox(root, value=["QB","RB","WR","TE"])
pos_drop.grid(row=8, column=1)

# Run the main event loop
root.mainloop()