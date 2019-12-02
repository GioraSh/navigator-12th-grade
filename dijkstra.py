import os
import sqlite3 as lite
import thread
import threading
from random import randint
from weights import *

def convert_coordinate_to_id(x,y):
    map_db=os.getcwd()+"\map.db"
    conn=lite.connect(map_db)
    cursor=conn.cursor()
    cursor.execute("""SELECT id FROM nodes WHERE min_x<=? AND ?<=max_x AND min_y<=? AND ?<=max_y""",(x,x,y,y))
    try:
        n=cursor.fetchall()[0][0]
    except IndexError:
        n=None
    conn.commit()
##    n=randint(0,17)
    return n

def roads_from_node(node):
    map_db=os.getcwd()+"\map.db"
    conn=lite.connect(map_db)
    cursor=conn.cursor()
    cursor.execute("""SELECT end_node_id,max_speed,distance,traffic FROM roads WHERE start_node_id=?""",(node,))
    sql_roads=cursor.fetchall()
    conn.commit()
    roads=[]
    for road in sql_roads:
        roads.append((road[0],road[2]*0.06/(road[1]*road[3])+0.2))
    return roads
   
def find_road(user_name,x_start,y_start,x_end,y_end):
    start_node=(convert_coordinate_to_id(x_start,y_start))
    print start_node
    end_node=(convert_coordinate_to_id(x_end,y_end))
    print end_node
    navigator_db=os.getcwd()+r"\navigator.db"
    navigation_conn=lite.connect(navigator_db)
    navigation_cursor=navigation_conn.cursor()
    navigation_cursor.execute("""CREATE TABLE """+str(user_name)+"""(id INTEGER PRIMARY KEY,time DECIMAL,previous_node INTEGER,finished TEXT)""")

    map_db=os.getcwd()+"\map.db"
    map_conn=lite.connect(map_db)
    map_cursor=map_conn.cursor()

    map_cursor.execute("""SELECT id FROM nodes""")
    for i in range(map_cursor.fetchall()[-1][0]+1):
        navigation_cursor.execute("""INSERT INTO """+str(user_name)+"""(id,time,previous_node,finished) VALUES(?,?,?,?)""",(i,None,None,"FALSE"))
        navigation_conn.commit()
    navigation_cursor.execute("""UPDATE """+str(user_name)+""" set time=?,finished=? WHERE id=?""",(0,"TRUE",start_node))
    navigation_conn.commit()

    navigation_cursor.execute("""SELECT * FROM """+user_name)
    print navigation_cursor.fetchall()
    
    node=start_node
    while not node==end_node:
        for road in roads_from_node(node):
            navigation_cursor.execute("""SELECT finished FROM """+str(user_name)+""" WHERE id=?""",(road[0],))
            if navigation_cursor.fetchone()[0]=="FALSE":
                navigation_cursor.execute("""SELECT time FROM """+str(user_name)+""" WHERE id=?""",(node,))
                new_time_to_get=navigation_cursor.fetchone()[0]+road[1]
                navigation_cursor.execute("""SELECT time FROM """+str(user_name)+""" WHERE id=?""",(road[0],))
                curr_time_to_get=navigation_cursor.fetchone()[0]
                if not curr_time_to_get==  None:
                    if curr_time_to_get>new_time_to_get:
                        navigation_cursor.execute("""UPDATE """+str(user_name)+""" set time=?,previous_node=? WHERE id=?""",(new_time_to_get,node,road[0]))

                else:
                    navigation_cursor.execute("""UPDATE """+str(user_name)+""" set time=?,previous_node=? WHERE id=?""",(new_time_to_get,node,road[0]))

                navigation_conn.commit()
        navigation_cursor.execute("""SELECT time FROM """+str(user_name)+""" WHERE finished=? AND time IS NOT ?""",("FALSE",None))
        a=navigation_cursor.fetchall()
        navigation_cursor.execute("""SELECT id FROM """+str(user_name)+""" WHERE time=?""",(min(a,key=lambda x: x[0])))
        node=navigation_cursor.fetchone()[0]
        navigation_cursor.execute("""UPDATE """+str(user_name)+""" set finished=? WHERE id=?""",("TRUE",node))
        navigation_conn.commit()
        

    navigation_cursor.execute("""SELECT * FROM """+str(user_name))
    print navigation_cursor.fetchall()
    the_way=[]
    while not node==start_node:
        navigation_cursor.execute("""SELECT previous_node FROM """+str(user_name)+""" WHERE id=?""",(node,))
        prev_node=navigation_cursor.fetchone()[0]
        the_way=[(prev_node,node)]+the_way
        node=prev_node
    streets=[]
    for road in the_way:
        map_cursor.execute("""SELECT name,direction FROM roads WHERE start_node_id=? AND end_node_id=?""",road)
        streets.append(map_cursor.fetchone())
    print the_way
    print streets
    navigation_cursor.execute("""SELECT time FROM """+str(user_name)+""" WHERE id=?""",(end_node,))
    print navigation_cursor.fetchall()
    navigation_cursor.execute("""DROP TABLE """+str(user_name))    



