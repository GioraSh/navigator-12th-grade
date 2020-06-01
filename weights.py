import sqlite3 as lite
import os
import time
from dijkstra import *


def guess_traffic(road_id,start_time):
    map_db=os.getcwd()+"\map.db"
    conn=lite.connect(map_db)
    cursor=conn.cursor()
    cursor.execute("""SELECT distance,max_speed,traffic FROM roads WHERE id=?""",(road_id,))
    road=cursor.fetchall()[0]
    #print "road: "
    #print road
    expected_time=road[0]*3.6/road[1]
    traffic=int((time.time()-start_time)/expected_time)+1
    #print (time.time()-start_time)/expected_time
    cur_traf=road[2]
    if cur_traf>1.0/traffic:
        cursor.execute("""UPDATE roads set traffic=? WHERE id=?""",(1.0/traffic,road_id))
    conn.commit()
    
def nullify_traffic():
    map_db=os.getcwd()+"\map.db"
    conn=lite.connect(map_db)
    cursor=conn.cursor()
    cursor.execute("""UPDATE roads set traffic=1 WHERE id>-1""")
    conn.commit()


def get_nodes_info(way):
    map_db=os.getcwd()+"\map.db"
    conn=lite.connect(map_db)
    cursor=conn.cursor()
    info=[]
    for node in way_to_nodes(way):
        cursor.execute("""SELECT id,min_x,max_x,min_y,max_y FROM nodes WHERE id=?""",(node,))
        new_info=cursor.fetchone()
        if not new_info in info:
            info.append(new_info)
    return info

def way_to_nodes(way):
    nodes=[]
    for road in way:
        nodes.append(road[0])
    nodes.append(road[1])
    return nodes


def update_history(his_info):
    his_db=os.getcwd()+r"\history.db"
    conn=lite.connect(his_db)
    cursor=conn.cursor()

    try:
        cursor.execute("""SELECT id FROM history""")
        r=cursor.fetchall()
        #last id
        r=r[-1][0]+1
        identity=r
    except IndexError:
        identity=0

    cursor.execute("""INSERT INTO history(id,user_name,points,ongoing) VALUES(?,?,?,?)""",(identity,his_info[0],str(his_info[1:-1]),his_info[-1]))
    conn.commit()
    print his_info

def start_history():
    his_db=os.getcwd()+r"\history.db"
    conn=lite.connect(his_db)
    cursor=conn.cursor()

    try:
        cursor.execute("""DROP TABLE history""")
    except error:
        print error
        pass
    finally:
        cursor.execute("""CREATE TABLE history(id INTEGER PRIMARY KEY,user_name TEXT, points TEXT ,ongoing TEXT)""")
        conn.commit()

def get_history():
    his_db=os.getcwd()+r"\history.db"
    conn=lite.connect(his_db)
    cursor=conn.cursor()

    cursor.execute("""SELECT * FROM history""")
    requests=cursor.fetchall()
    hist=[]
    for req in requests:
        hist.append([req[0],req[1]]+[float(x.strip("()")) for x in req[2].strip("[]").split(", ")]+[req[3]])
    return hist


def get_road_id(node_id_1,node_id_2):
    map_db=os.getcwd()+r"\map.db"
    conn=lite.connect(map_db)
    cursor=conn.cursor()

    print node_id_1
    print node_id_2
    cursor.execute("""SELECT id FROM roads WHERE start_node_id==? AND end_node_id==?""",(node_id_1,node_id_2))
    return cursor.fetchone()[0]
