import sqlite3 as lite
import os

def guess_traffic(start_node,end_node,time):
    map_db=os.getcwd()+"\map.db"
    conn=lite.connect(map_db)
    cursor=conn.cursor()
    cursor.execute("""SELECT 
