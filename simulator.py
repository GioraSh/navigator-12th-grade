import sqlite3 as lite
import os
import time
from random import randint
import thread
import threading
from socket import *


class Client(object):


    def __init__(self,location,finish,roads_id):

        self.loc=location
        self.fin=finish
        self.roads=roads_id
        self.cur_road=roads_id[0]

    def move(self):
        cwd=os.getcwd()
        conn=lite.connect(cwd+r"\simulation.db")
        cursor=conn.cursor()
        cursor.execute("""SELECT cur_speed,distance,start_x,start_y,end_x,end_y FROM real_roads WHERE id=?""",(self.cur_road,))
        speed,dist,st_x,st_y,end_x,end_y=cursor.fetchone()
        speed=speed/3.6
        displacement=0.1*speed
        proportion=displacement/dist
        x_diff=proportion*(end_x-st_x)
        y_diff=proportion*(end_y-st_y)
        cur_x,cur_y=self.loc
        if max(st_x,end_x)>=cur_x+x_diff>=min(st_x,end_x):
            cur_x=cur_x+x_diff
        else:
            cur_x=end_x
        if max(st_y,end_y)>=cur_y+y_diff>=min(st_y,end_y):
            cur_y=cur_y+y_diff
        else:
            cur_y=end_y
        self.loc=(cur_x,cur_y)
        if self.loc==(end_x,end_y) and not self.loc==self.fin:
            self.cur_road=self.roads[self.roads.index(self.cur_road)+1]


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
        if road[0]!=-1:
            cursor.execute("""INSERT INTO real_roads(id,start_x,start_y,end_x,end_y,max_speed,distance,cur_speed) VALUES(?,?,?,?,?,?,?,?)""",tuple(road)+(road[-2],))
            conn.commit()
        else:
            cursor.execute("""INSERT INTO real_roads(id,start_x,start_y,end_x,end_y,max_speed,distance,cur_speed) VALUES(?,?,?,?,?,?,?,?)""",tuple(road)+(1,))
            conn.commit()

    cursor.execute("""SELECT * FROM real_roads""")



def run_round():
    cwd=os.getcwd()
    conn=lite.connect(cwd+r"\simulation.db")
    cursor=conn.cursor()


    cursor.execute("""SELECT id,max_speed,cur_speed FROM real_roads""")
    for road in cursor.fetchall():
        if road[0]!=-1:
            change=randint(-1,1)
            new_speed=max(min(road[-1]+change,road[1]),1)
            cursor.execute("""UPDATE real_roads set cur_speed=? WHERE id=?""",(new_speed,road[0]))
    conn.commit()


    
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
        while t<300:
            run_round()
            time.sleep(1)
            t=t+1
        if raw_input("1 for true: ")=="1":
            stopped=True
    close_simulation()

def clienthandler(clientsock,addr):
    cwd=os.getcwd()
    conn=lite.connect(cwd+r"\simulation.db")
    cursor=conn.cursor()
    
    print "new connection"
    data=eval(clientsock.recv(BUFFSIZ))
    print data
    print type(data)
    road=data[0]
    cursor.execute("""SELECT start_x,start_y FROM real_roads WHERE id=?""",(data[0],))
    loc=tuple(cursor.fetchone())
    cursor.execute("""SELECT end_x,end_y FROM real_roads WHERE id=?""",(data[-1],))
    finish=tuple(cursor.fetchone())
    print data
    
    cl=Client(loc,finish,data)    
    thread.start_new_thread(move_handler,(cl,))


    
    moving=True
    while moving:
        data=clientsock.recv(BUFFSIZ)
        if data=="get loc":
            clientsock.send(str(cl.loc))
        if cl.loc==cl.fin:
            moving==False
    

def adminhandler(clientsock,addr):
    cwd=os.getcwd()
    conn=lite.connect(cwd+r"\simulation.db")
    cursor=conn.cursor()

    data=clientsock.recv(BUFFSIZ)
    print data
    id_speed=data.split(",")
    cursor.execute("""UPDATE real_roads set cur_speed=? WHERE id=?""",(id_speed[1],id_speed[0]))
    conn.commit()
            
def move_handler(client):
    while not client.loc==client.fin:
        client.move()
        time.sleep(0.1)

try:
    close_simulation()
except error:
    print error
    pass
finally:
    thread.start_new_thread(main,())        
    HOST="127.0.0.1"
    PORT=53268
    ADDR=(HOST,PORT)
    BUFFSIZ=1024
    
    serversock=socket(AF_INET,SOCK_STREAM)
    serversock.bind(ADDR)
    serversock.listen(1)


    cwd=os.getcwd()
    conn=lite.connect(cwd+r"\simulation.db")
    cursor=conn.cursor()

    has_new=True
    runs=100
    #recieves connections
    while runs>0:
        runs=runs-1
        if has_new:
            has_new=False
            clientsock, addr=serversock.accept()
            print "\n\n\n"+"new connection"+"\n\n\n"
            data=clientsock.recv(BUFFSIZ)
            if data=="client":
                thread.start_new_thread(clienthandler,(clientsock, addr))
            elif data=="admin":
                thread.start_new_thread(adminhandler,(clientsock,addr))
            has_new=True
    serversock.close()

    
