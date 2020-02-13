from socket import *
import thread
import threading
from dijkstra import *
import time

def handler(clientsock,addr):
    sock_open=True
    while sock_open:
        user_name=(clientsock.recv(BUFFSIZ),)
        #dept=eval(clientsock.recv(BUFFSIZ))
        dept=convert_streets_to_coordinates(*eval(clientsock.recv(BUFFSIZ)))
        print dept
        #dest=eval(clientsock.recv(BUFFSIZ))
        dest=convert_streets_to_coordinates(*eval(clientsock.recv(BUFFSIZ)))
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
    print way
    print streets
    print roads
    clientsock.send(str(way))
    #clientsock.send(str(streets))
    clientsock.send(str(roads))
    data=clientsock.recv(BUFFSIZ)
    cur_node=convert_coordinate_to_id(*eval(data))
    time.sleep(1)
    last_node=cur_node
    change_last=False
    start_time=time.time()
    while not way==[]:
        if cur_node==None or cur_node==last_node:
            guess_traffic(roads[0],start_time)
            change_last=False
        else:
            way=way[1:]
            streets=streets[1:]
            roads=roads[1:]
            start_time=time.time()
            change_last=True
        try:
            clientsock.send(str(streets[0]))
        except IndexError:
            clientsock.send("done")
        else:
            data=clientsock.recv(BUFFSIZ)
            cur_node=convert_coordinate_to_id(*eval(data))
            if change_last:
                last_node=cur_node
    #clientsock.send("done")
    clientsock.close()



def one_time_nav(clientsock,info):
    way=str(find_road(*info)[0])
    clientsock.send(way)
    clientsock.close()



def traffic_nulifier():
    while True:
        nullify_traffic()
        time.sleep(300)


print lite.threadsafety       
thread.start_new_thread(traffic_nulifier,())
HOST="127.0.0.1"
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
        print "\n\n\n"+"new connection"+"\n\n\n"
        thread.start_new_thread(handler,(clientsock, addr))
        has_new=True
serversock.close()
