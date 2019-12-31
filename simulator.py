import sqlite3 as lite
import os
import time
from random import randint

def start_table():
    cwd=os.getcwd()
    conn=lite.connect(cwd+r"\simulation.db")
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE real_roads(id INTEGER PRIMARY KEY, start_x DECIMAL, start_y DECIMAL, end_x DECIMAL, end_y DECIMAL, max_speed INTEGER, distance DECIMAL, cur_speed INTEGER)""")
    conn.commit()

    map_conn=lite.connect(cwd+r"\map.db")
    map_cursor=map_conn.cursor()
    map_cursor.execute("""SELECT id,start_node_id,end_node_id,max_speed,distance FROM roads""")
    roads=map_cursor.fetchall()
    needed_roads=[]
    for road in roads:
        map_cursor.execute("""SELECT min_x,max_x,min_y,max_y FROM nodes WHERE id=?""",(road[1],))
        start_node=map_cursor.fetchone()
        map_cursor.execute("""SELECT min_x,max_x,min_y,max_y FROM nodes WHERE id=?""",(road[2],))
        end_node=map_cursor.fetchone()
        needed_road=[]
        for i in range(len(road)):
            if i==1:
                needed_road.append(int(10**6*(start_node[0]+start_node[1])/2)/10.0**6)
                needed_road.append(int(10**6*(start_node[2]+start_node[3])/2)/10.0**6)
            elif i==2:
                needed_road.append(int(10**6*(end_node[0]+end_node[1])/2)/10.0**6)
                needed_road.append(int(10**6*(end_node[2]+end_node[3])/2)/10.0**6)
            else:
                needed_road.append(road[i])
        needed_roads.append(needed_road)
    map_conn.commit()

    for road in needed_roads:
        cursor.execute("""INSERT INTO real_roads(id,start_x,start_y,end_x,end_y,max_speed,distance,cur_speed) VALUES(?,?,?,?,?,?,?,?)""",tuple(road)+(road[-2],))
        conn.commit()

    cursor.execute("""SELECT * FROM real_roads""")
    print cursor.fetchall()



def run_round():
    cwd=os.getcwd()
    conn=lite.connect(cwd+r"\simulation.db")
    cursor=conn.cursor()


    cursor.execute("""SELECT id,max_speed,cur_speed FROM real_roads""")
    for road in cursor.fetchall():
        change=randint(-1,1)
        if road[-1]+change==48:
            print 48
        new_speed=max(min(road[-1]+change,road[1]),1)
        cursor.execute("""UPDATE real_roads set cur_speed=? WHERE id=?""",(new_speed,road[0]))

    cursor.execute("""SELECT cur_speed FROM real_roads""")
    print cursor.fetchall()

    
def close_simulation():
    cwd=os.getcwd()
    conn=lite.connect(cwd+r"\simulation.db")
    cursor=conn.cursor()
    cursor.execute("""DROP TABLE real_roads""")
    conn.commit()





def main():
    start_table()
    stopped=False
    while not stopped:
        t=0
        while t<100:
            run_round()
            time.sleep(0.1)
            t=t+1
        if raw_input("1 for true: ")=="1":
            stopped=True
    close_simulation()
        
