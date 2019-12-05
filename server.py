from socket import *
import thread
import threading
from dijkstra import *
import time

def handler(clientsock,addr):
    sock_open=True
    while sock_open:
            user_name=(clientsock.recv(BUFFSIZ),)
            dept=eval(clientsock.recv(BUFFSIZ))
            print dept
            dest=eval(clientsock.recv(BUFFSIZ))
            print dest
            info=user_name+dept+dest
            print info
            data=clientsock.recv(BUFFSIZ)
            if data=="ongoing":
                ongoing_nav(clientsock,info)
            else:
                one_time_nav(clientsock,info)
            sock_open=False
    clientsock.close()

def ongoing_nav(clientsock,info):
    way,streets,roads=find_road(*info)
    clientsock.send(str(streets))
    data="no"
    #data=clientsock.recv(BUFFSIZ)
    #cur_node=convert_coordinate_to_id(*eval(data))
    start_time=time.time()
    while len(way)>1:
        print way
        #if cur_node==None:
        if not data=="yes":
            guess_traffic(roads[0],start_time)
        else:
            way=way[1:]
            streets=streets[1:]
            roads=roads[1:]
            start_time=time.time()
        print str(streets[0])
        clientsock.send(str(streets[0]))
        print "jghjhhgjhk"
        data=clientsock.recv(BUFFSIZ)
        print data
        #cur_node=convert_coordinate_to_id(*eval(data))
    clientsock.send("done")
    clientsock.close()


def one_time_nav(clientsock,info):
    way=str(find_road(*info)[1])
    clientsock.send(way)
    clientsock.close()



def traffic_nulifier():
    while True:
        nullify_traffic()
        time.sleep(300)


        
thread.start_new_thread(traffic_nulifier,())
HOST="localhost"
PORT=55342
ADDR=(HOST,PORT)
BUFFSIZ=1024

serversock=socket(AF_INET,SOCK_STREAM)
serversock.bind(ADDR)
serversock.listen(1)

has_new=True
runs=100
#recieves connections
while runs>0:
    runs=runs-1
    if has_new:
        has_new=False
        clientsock, addr=serversock.accept()
        thread.start_new_thread(handler,(clientsock, addr))
        has_new=True
serversock.close()
