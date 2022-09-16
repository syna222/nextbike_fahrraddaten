import os
import re
import sqlite3

## --- TRANSFERS ALL CSV-FILES (bikes and places in diff. folders) TO DATABASE SCHEME/FILE --- ##

#folders with csvs:
bikes_csvs_folder = r"C:\Users\vck\Documents\Python Scripts\bike_project\csvs_bikes"
places_csvs_folder = r"C:\Users\vck\Documents\Python Scripts\bike_project\csvs_places"

#create + connect to database:
conn = sqlite3.connect(":memory:")            #alternatively save as "next_bike.db"               
c = conn.cursor()

def create_tables():
    c.execute("""CREATE TABLE places (
            uid integer,
            lat real,
            lng real,
            address text
            )""")

    c.execute("""CREATE TABLE presence (
                bike_num integer,
                place_uid integer,
                date_stamp text
                )""")

    c.execute("""CREATE TABLE bikes (
                number integer,
                bike_type integer,
                lock_type text,
                active integer,
                state text,
                electric_lock integer,
                board_computer integer
                )""")

def test_database():   #c doesn't have to be passed
    #test number of entries:
    c.execute("SELECT Count(*) FROM places")
    print("counted entries from table 'places':", c.fetchall(), "\n")
    c.execute("SELECT Count(*) FROM presence")
    print("counted entries from table 'presence':", c.fetchall(), "\n")
    c.execute("SELECT Count(*) FROM bikes")
    print("counted entries from table 'bikes':", c.fetchall(), "\n")
    #check for duplicates in bike table:
    c.execute("SELECT * FROM bikes WHERE number = '220255'")
    print(c.fetchall(), "\n")
    #text example for a bike number:
    c.execute("""SELECT *
                 FROM places INNER JOIN presence
                 ON places.uid = presence.place_uid
                 WHERE presence.bike_num = '220255'""")
    print(c.fetchall(), "\n")

def fill_bikes_and_presence(bikes_csvs_folder):
    os.chdir(bikes_csvs_folder)
    file_list = os.listdir(bikes_csvs_folder)
    for name in file_list:
        file_path = os.path.join(bikes_csvs_folder, name)
        file = open(file_path, "r", encoding="utf-8")
        filedata_list = file.readlines()
        #enter filedata_list into db:
        for entry in filedata_list:
            #split into single values:
            value_list = entry.split(",")
            #check if number = value_list[0] already exists + insert into bike-table if it doesn't exist:
            c.execute("SELECT number FROM bikes WHERE number=:number", {"number":value_list[0]})
            exists = c.fetchall()
            if exists:
                pass
            else:
                c.execute("INSERT INTO bikes VALUES (:number, :bike_type, :lock_type, :active, :state, :el_lock, :board_comp)", {"number":value_list[0], "bike_type":value_list[1], "lock_type":value_list[2], "active":value_list[3], "state":value_list[4], "el_lock":value_list[5], "board_comp":value_list[6]})
                conn.commit()
            #insert into presence-table:
            c.execute("INSERT INTO presence VALUES (:number, :uid, :date_stamp)", {"number":value_list[0], "uid":value_list[7], "date_stamp":value_list[8]})
            conn.commit()

def fill_places(places_csvs_folder):
    os.chdir(places_csvs_folder)
    file_list = os.listdir(places_csvs_folder)
    for name in file_list:
        file_path = os.path.join(places_csvs_folder, name)
        file = open(file_path, "r", encoding="utf-8")
        filedata_list = file.readlines()
        #enter filedata_list into db:
        for entry in filedata_list:
            #split into single values:
            value_list = entry.split(",")
            c.execute("INSERT INTO places VALUES (:uid, :lat, :lng, :address)", {"uid":value_list[0], "lat":value_list[1], "lng":value_list[2], "address":value_list[3]})
            conn.commit() 


#MAIN:
create_tables()
fill_bikes_and_presence(bikes_csvs_folder)
fill_places(places_csvs_folder)
test_database()
conn.close()







