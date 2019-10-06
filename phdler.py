#!/usr/bin/env python
from __future__ import unicode_literals
import youtube_dl
import requests
import sys
import urllib.parse as urlparse
import sqlite3
import os
from prettytable import PrettyTable
from sqlite3 import Error
              

############### FUNCTIONS

# Database location
database = r"./database.db"

def type_check(item):
    if item == "model":
        print ("Valid type (model) selected.")
    elif item == "pornstar":
        print ("Valid type (pornstar) selected.")
    elif item == "channel":
        print ("Valid type (channel) selected.")
    elif item == "user":
        print ("Valid type (user) selected.")
    elif item == "playlist":
        print ("Valid type (playlist) selected.")
    elif item == "all":
        print ("Valid type (all) selected.")
    else:
        how_to_use("Not a valid type.")
        sys.exit()

def ph_url_check(url):
    parsed = urlparse.urlparse(url)
    if parsed.netloc == "www.pornhub.com":
        print ("PornHub url validated.")
    else:
        print ("This is not a PornHub url.")
        sys.exit()

def ph_type_check(url):
    parsed = urlparse.urlparse(url)
    if parsed.path.split('/')[1] == "model":
        print ("This is a MODEL url,")
    elif parsed.path.split('/')[1] == "pornstar":
        print ("This is a PORNSTAR url,")
    elif parsed.path.split('/')[1] == "channels":
        print ("This is a CHANNEL url,")
    elif parsed.path.split('/')[1] == "users":
        print ("This is a USER url,")
    elif parsed.path.split('/')[1] == "playlist":
        print ("This is a PLAYLIST url,")
    elif parsed.path.split('/')[1] == "view_video.php":
        print ("This is a VIDEO url. Please paste a model/pornstar/user/channel/playlist url.")
        sys.exit()
    else:
        print ("Somethings wrong with the url. Please check it out.")
        sys.exit()

def ph_alive_check(url):
    request = requests.get(url)
    if request.status_code == 200:
        print ("and the URL is existing.")
    else:
        print ("but the URL does not exist.")
        sys.exit()

def dl_start():
    conn = create_connection(database)
    with conn:
        
        print("downloading new items")
        dl_all_new_items(conn)
        print("downloading all items")
        dl_all_items(conn)


def dl_all_items(conn):

    cur = conn.cursor()
    cur.execute("SELECT * FROM ph_items")
    
    rows = cur.fetchall()
 
    for row in rows:
        if row[1] == "model":
            url_after = "/videos/upload"
        elif row[1] == "pornstar":
            url_after = "/videos"
        elif row[1] == "users":
            url_after = "/videos/public"
        elif row[1] == "channels":
            url_after = "/videos"
        else:
            url_after = ""

        print("-----------------------------")
        print(row[1])
        print(row[2])
        print("https://www.pornhub.com/" + str(row[1]) + "/" + str(row[2]) + url_after)
        print("-----------------------------")

        # Find more available options here: https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L129-L279
        outtmpl = get_dl_location('DownloadLocation') + '/' + str(row[1]) + '/' + str(row[2]) + '/%(title)s.%(ext)s'
        ydl_opts_start = {
            'format': 'best',
            'playliststart:': 1,
            'playlistend': 4,
            'outtmpl': outtmpl,
            'nooverwrites': True,
            'no_warnings': False,
            'ignoreerrors': True,
        }

        url = "https://www.pornhub.com/" + str(row[1]) + "/" + str(row[2] + url_after)
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            ydl.download([url])

        cur.execute("UPDATE ph_items SET lastchecked=CURRENT_TIMESTAMP WHERE name = ?", (row[2],))


def dl_all_new_items(conn):

    cur = conn.cursor()
    cur.execute("SELECT * FROM ph_items WHERE new='1'")
    
    rows = cur.fetchall()
 
    for row in rows:
        
        if str(row[1]) == "model":
            url_after = "/videos/upload"
        elif str(row[1]) == "pornstar":
            url_after = "/videos"
        elif str(row[1]) == "users":
            url_after = "/videos/public"
        elif str(row[1]) == "channels":
            url_after = "/videos"
        else:
            url_after = ""

        print("-----------------------------")
        print(row[1])
        print(row[2])
        print("https://www.pornhub.com/" + str(row[1]) + "/" + str(row[2]) + url_after)
        print("-----------------------------")

        # Find more available options here: https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L129-L279
        outtmpl = get_dl_location('DownloadLocation') + '/' + str(row[1]) + '/' + str(row[2]) + '/%(title)s.%(ext)s'
        ydl_opts = {
            'format': 'best',
            'outtmpl': outtmpl,
            'nooverwrites': True,
            'no_warnings': False,
            'ignoreerrors': True,
        }

        url = "https://www.pornhub.com/" + str(row[1]) + "/" + str(row[2]) + url_after
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        cur.execute("UPDATE ph_items SET new='0', lastchecked=CURRENT_TIMESTAMP WHERE name = ?", (row[2],))


def custom_dl(url):
    ph_url_check(url)
    ph_alive_check(url)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def add_check(name_check):
    if name_check == "batch":
        u_input = input("Please enter full path to the batch-file.txt (or c to cancel): ")
        if u_input == "c":
            print("Operation canceled.")
        else:
            with open(u_input, 'r') as input_file:
                for line in input_file:
                    line = line.strip()
                    add_item(line)

    else:
        add_item(name_check)


def add_item(name_check):
    parsed = urlparse.urlparse(name_check)
    ph_url_check(name_check)
    ph_type_check(name_check)
    ph_alive_check(name_check)
    item_type = parsed.path.split('/')[1]
    item_name = parsed.path.split('/')[2]
    
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM ph_items WHERE name = ?", (item_name,))
    data=cur.fetchone()[0]
    if data==0:
        with conn:
            item = (item_type, item_name, '1');
            item_id = create_item(conn, item)

        print(item_name + " added to database.")
    else:
        print("Item already exists in database")


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_item(conn, item):
    sql = ''' INSERT INTO ph_items(type,name,new)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, item)
    return cur.lastrowid


def select_all_items(conn, item):
    cur = conn.cursor()
    if item == "all":
        cur.execute("SELECT * FROM ph_items")
    else:
        cur.execute("SELECT * FROM ph_items WHERE type='" + item + "'")
 
    rows = cur.fetchall()
 
    t = PrettyTable(['Id.', 'Type', 'Name', 'Date created', 'Last checked', 'Url'])
    t.align['Id.'] = "l"
    t.align['Type'] = "l"
    t.align['Name'] = "l"
    t.align['Date created'] = "l"
    t.align['Last checked'] = "l"
    t.align['Url'] = "l"
    for row in rows:
        url = "https://www.pornhub.com/" + str(row[1]) + "/" + str(row[2])
        t.add_row([row[0], row[1], row[2], row[4], row[5], url])
    print(t)


def list_items(item):
    conn = create_connection(database)
    with conn:
        print("Listing items from database:")
        select_all_items(conn, item)


def delete_single_item(conn, id):
    sql = 'DELETE FROM ph_items WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()


def delete_item(item_id):
    conn = create_connection(database)
    with conn:
        delete_single_item(conn, item_id);


def create_config(conn, item):
    sql = ''' INSERT INTO ph_settings(option, setting)
              VALUES(?,?) '''
    c = conn.cursor()
    c.execute(sql, item)
    return c.lastrowid


def prepare_config():
    conn = create_connection(database)
    u_input = input("Please enter the FULL PATH to your download location: ")
    with conn:
        item = ('DownloadLocation', u_input)
        item_id = create_config(conn, item)

def check_for_database():
    if os.path.exists(database) == True:
        print("Database exists.")
    else:
        print("Database does not exist.")
        print("Looks like this is your first time run...")
        first_run()

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Tables created.")
    except Error as e:
        print(e)

def create_tables(): 
    sql_create_items_table = """ CREATE TABLE IF NOT EXISTS ph_items (
                                        id integer PRIMARY KEY,
                                        type text,
                                        name text,
                                        new integer DEFAULT 1,
                                        datecreated DATETIME DEFAULT CURRENT_TIMESTAMP,
                                        lastchecked DATETIME DEFAULT CURRENT_TIMESTAMP
                                    ); """

    sql_create_settings_table = """ CREATE TABLE IF NOT EXISTS ph_settings (
                                        id integer PRIMARY KEY,
                                        option text,
                                        setting text,
                                        datecreated DATETIME DEFAULT CURRENT_TIMESTAMP
                                    ); """
 
    # create a database connection
    conn = create_connection(database)
 
    # create tables
    if conn is not None:
        # create items table
        create_table(conn, sql_create_items_table)
        create_table(conn, sql_create_settings_table)
        prepare_config()
    else:
        print("Error! cannot create the database connection.")


def get_dl_location(option):
    conn = create_connection(database)
    if conn is not None:
        c = conn.cursor()
        c.execute("SELECT * FROM ph_settings WHERE option='" + option + "'")
     
        rows = c.fetchall()
     
        for row in rows:
            dllocation = row[2]
        return dllocation

    else:
        print("Error! somethings wrong with the query.")


def first_run():
    create_tables()


def how_to_use(error):
    print("Error: " + error)
    print("Please use the tool like this:")
    t = PrettyTable(['Tool', 'command', 'item'])
    t.align['Tool'] = "l"
    t.align['command'] = "l"
    t.align['item'] = "l"
    t.add_row(['phdler', 'start', ''])
    t.add_row(['phdler', 'custom', 'url (full PornHub url)'])
    t.add_row(['phdler', 'add', 'model | pornstar | channel | user | playlist | batch (for .txt file)'])
    t.add_row(['phdler', 'list', 'model | pornstar | channel | user | playlist | all'])
    t.add_row(['phdler', 'delete', 'model | pornstar | channel | user | playlist'])
    print(t)

def help_command():
    print("------------------------------------------------------------------")
    print("You asked for help, here it comes! Run phdler with these commands:")
    t = PrettyTable(['Command', 'argument', 'description'])
    t.align['Command'] = "l"
    t.align['argument'] = "l"
    t.align['description'] = "l"
    t.add_row(['start', '', 'start the script'])
    t.add_row(['custom', 'url', 'download a single video from PornHub'])
    t.add_row(['add', 'model | pornstar | channel | user | playlist | batch (for .txt file)', 'adding item to database'])
    t.add_row(['list', 'model | pornstar | channel | user | playlist', 'list selected items from database'])
    t.add_row(['delete', 'model | pornstar | channel | user | playlist', 'delete selected items from database'])
    print(t)
    print("Example: phdler add pornhub-url")
    print("------------------------------------------------------------------")

############### SCRIPT RUN

check_for_database()

if len(sys.argv) > 1:

    if sys.argv[1] == "start":
        dl_start()

    elif sys.argv[1] == "test":
        get_dl_location('DownloadLocation')
        
    elif sys.argv[1] == "custom":
        if len(sys.argv) > 2:
            custom_dl(sys.argv[2])
        else:
            how_to_use("Missing item")

    elif sys.argv[1] == "add":
        if len(sys.argv) > 2:
            add_check(sys.argv[2])
        else:
            how_to_use("Missing item")

    elif sys.argv[1] == "delete":
        if len(sys.argv) > 2:
            type_check(sys.argv[2])
            list_items(sys.argv[2])
            u_input = input("Please enter the ID to delete (or c to cancel): ")
            if u_input == "c":
                print("Operation canceled.")
            else:
                delete_item(u_input)
        else:
            how_to_use("Missing item")

    elif sys.argv[1] == "list":
        if len(sys.argv) > 2:
            type_check(sys.argv[2])
            list_items(sys.argv[2])
        else:
            how_to_use("Missing item")

    elif sys.argv[1] == "help":
        help_command()

    else:
        how_to_use("Command not found!")

else:
    how_to_use("Missing command.")
