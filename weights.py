import sqlite3 as lite
import os
import time

def guess_traffic_1(start_node,end_node,travel_time):
    map_db=os.getcwd()+"\map.db"
    conn=lite.connect(map_db)
    cursor=conn.cursor()
    cursor.execute("""SELECT id,distance,max_speed,traffic FROM roads WHERE start_node_id=? AND end_node_id=?""",(start_node,end_node))
    road=cursor.fetchone()
    traffic=min(1,(road[1]*0.06/road[2])/travel_time)
    cursor.execute("""UPDATE roads set traffic=? WHERE id=?""",(traffic,road[0]))
    conn.commit()


def guess_traffic(road_id,start_time):
    map_db=os.getcwd()+"\map.db"
    conn=lite.connect(map_db)
    cursor=conn.cursor()
    cursor.execute("""SELECT distance,max_speed,traffic FROM roads WHERE id=?""",(road_id,))
    road=cursor.fetchall()[0]
    print "road: "
    print road
    expected_time=road[0]*3.6/road[1]
    traffic=int((time.time()-start_time)/expected_time)+1
    print (time.time()-start_time)/expected_time
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
