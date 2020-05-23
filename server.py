from socket import *
import thread
import threading
from dijkstra import *
import time

def handler(clientsock,addr):
    data=clientsock.recv(BUFFSIZ)
    if data=="client":
        client_handler(clientsock,addr)
    else:
        admin_handler(clientsock,addr)


def admin_handler(clientsock,addr):
    data=clientsock.recv(BUFFSIZ)
    while data!="close":
        if data=="history":
            for request in get_history():
                clientsock.send(str(request))
                print request
                clientsock.recv(BUFFSIZ)
            clientsock.send("sent history")
        elif data=="roadID":
            data=clientsock.recv(BUFFSIZ)
            data=data.split("; ")
            print data
            print eval(data[0])
            data=get_road_id(convert_streets_to_coordinates(*eval(data[0])),convert_streets_to_coordinates(*eval(data[1])))
            print data
            clientsock.send(data)
        data=clientsock.recv(BUFFSIZ)
    clientsock.close()

    
def client_handler(clientsock,addr):
    sock_open=True
    while sock_open:
        user_name=(clientsock.recv(BUFFSIZ),)
        print user_name
        #dept=eval(clientsock.recv(BUFFSIZ))
        points_ammount=eval(clientsock.recv(BUFFSIZ))
        print points_ammount
        infos=[]
        his_info=[user_name[0]]
        for i in range(points_ammount):
            infos.append(user_name)
        for i in range(points_ammount):
            point=convert_streets_to_coordinates(*eval(clientsock.recv(BUFFSIZ)))
            infos[i]=infos[i]+point
            his_info.append(point)
            if i>0:
                infos[i-1]=infos[i-1]+point
        print infos
        data=clientsock.recv(BUFFSIZ)
        his_info.append(data)
        update_history(his_info)
        if data=="ongoing":
            ongoing_nav(clientsock,infos,points_ammount)
        else:
            one_time_nav(clientsock,infos,points_ammount)
        sock_open=False
    clientsock.close()

def ongoing_nav(clientsock,infos,points_ammount):
    for i in range(points_ammount-1):
        way,streets,roads=find_road(*infos[i])           
        nodes=get_nodes_info(way)
        clientsock.send(str(nodes))
        data=clientsock.recv(BUFFSIZ)
        clientsock.send(str(way))
        time.sleep(1)
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
                clientsock.send("arrived at point")
            else:
                data=clientsock.recv(BUFFSIZ)
                cur_node=convert_coordinate_to_id(*eval(data))
                if change_last:
                    last_node=cur_node
    clientsock.send("arrived at destination")
    clientsock.close()



def one_time_nav(clientsock,infos,points_ammount):
    way=[]
    for i in range(points_ammount-1):
        way=way+find_road(*infos[i])[0]
    nodes=get_nodes_info(way)
    clientsock.send(str(nodes))
    data=clientsock.recv(BUFFSIZ)
    clientsock.send(str(way))
    clientsock.close()



def traffic_nulifier():
    while True:
        nullify_traffic()
        time.sleep(300)
        print get_history()


print lite.threadsafety
start_history()
thread.start_new_thread(traffic_nulifier,())
HOST="192.168.0.101"
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
