#TODO : Add hidden features
#TODO : Write errors for wrong user inputs

#DONE : Write the function to complete a task
#DONE : Write the delete item function
#DONE : Write the add item function
#DONE : Drop table from folders category in the delete folder functions
#DONE : Write the add folder function
#DONE : Write the select folders function
#DONE : Write the function to select a folder

import os
from colored import fg, attr
from cs50 import SQL
import sys

db = SQL(f"sqlite:///{os.path.dirname(__file__)}/notes.db")

'''
Commands :
$ noterr
$ noterr create-folder <foldername>
$ noterr folder <foldername>
$ noterr folder <foldername> add '<item>'
$ noterr folder <foldername> del '<item>'
$ noterr delete-folder <foldername>
$ noterr folder codes done '<item>'

Noterr will also have hidden commands for game and other cool stuff, like:
$ note tictac (play tic tac toe)

... and so on

'''
# SQLITE3 QUERIES
def show_folders():
    folders = db.execute("SELECT * FROM folders;")
    for i in folders:
        print(f"{i['name']}")

def delete_folder(name):
    db.execute(f"DROP TABLE {name}")
    db.execute(f"DELETE FROM folders WHERE name='{name}'")

def create_folder(name):
    db.execute(f"CREATE TABLE '{name}'( 'id' INTEGER PRIMARY KEY, 'task' VARCHAR(255), 'done' INTEGER);")
    db.execute(f"INSERT INTO folders (name) VALUES ('{name}')")

def add_to_folder(folder, task):
    db.execute(f"INSERT INTO {folder} (task, done) VALUES ('{task}', 0);")
    print(f"Added '{task}' to {folder}")
    print()

def delete_item(folder, name):
    db.execute(f"DELETE FROM {folder} WHERE task='{name}';")

def show_items(folder):
    items = db.execute(f"SELECT * FROM {folder}")
    for i in items:
        if i['done'] == 0:
            print(f"%s {i['task']} %s" %(fg('cyan'), attr('reset')))
        else:
            print(f"%s {i['task']} %s" %(fg('green'), attr('reset')))

def complete_item(folder, item):
    db.execute(f"UPDATE {folder} SET done = 1 WHERE task = '{item}';")

def main():
    args = sys.argv
    if len(args) == 1 and 'noterr' in args[0]:
        show_folders()
    elif args[1] == "folder" and len(args) == 3:
        print()
        show_items(args[2])
        print()
    elif args[1] == "create-folder":
        # Create new folder
        create_folder(args[2])
        print()
        print(f"Created folder {args[2]}")
        print()
    elif args[1] == "delete-folder":
        # Delete a folder
        delete_folder(args[2])
        print(f"Deleted folder {args[2]}")
    elif args[1] == "folder" and args[3] == "add":
        # Add item to folder
        add_to_folder(args[2], args[4])
    elif args[1] == "folder" and args[3] == "del":
        # Remove item from folder
        delete_item(args[2], args[4])
        print(f"Deleted {args[4]} from {args[2]}")
    elif args[1] == "folder" and args[3] == "done":
        complete_item(args[2], args[4])
    else:
        print(f"'{args[1]}' is not recognized as a command")

if __name__ == "__main__":
    main()

