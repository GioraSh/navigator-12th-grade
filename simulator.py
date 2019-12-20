import sqlite3 as lite
import os

cwd=os.getcwd()
conn=lite.connect(cwd+r"\simulation.db")
cursor=conn.cursor()
cursor.execute("""CREATE TABLE real_roads(id INTEGER PRIMARY KEY, start_x DECIMAL, start_y DECIMAL, end_x DECIMAL, end_y DECIMAL, max_speed INTEGER, distance DECIMAL, cur_speed INTEGER)""")
conn.commit()

map_conn=lite.connect(cwd+r"\map.db")
map_cursor=map_conn.cursor()
map_cursor.execute("""SELECT id,max_speed,distance,start_node_id,end_node_id FROM roads""")
roads=map_cursor.fetchall()
needed_roads=[]
for road in roads:
    map_cursor.execute("""SELECT min_x,max_x,min_y,max_y FROM nodes WHERE id=?""",(road[3],))
    start_node=map_cursor.fetchone()
    map_cursor.execute("""SELECT min_x,max_x,min_y,max_y FROM nodes WHERE id=?""",(road[4],))
    end_node=map_cursor.fetchone()
    needed_road=[]
    for i in range(len(road)):
        if i==3:
            needed_road.append(int(10**6*(start_node[0]+start_node[1])/2)/10.0**6)
            needed_road.append(int(10**6*(start_node[2]+start_node[3])/2)/10.0**6)
        elif i==4:
            needed_road.append(int(10**6*(end_node[0]+end_node[1])/2)/10.0**6)
            needed_road.append(int(10**6*(end_node[2]+end_node[3])/2)/10.0**6)
        else:
            needed_road.append(road[i])
        needed_roads.append(needed_road)
print roads
print needed_roads

map_conn.commit()

cursor.execute("""DROP TABLE real_roads""")
