from socket import *
import thread
import time

def get_departure():
    y_dept=raw_input("enter north/south coordinate of departure: ")
    x_dept=raw_input("enter east/west coordinate of departure: ")
    #return (x_dept,y_dept)
    return (34.801165,31.908748)

def get_destination():
    y_dest=raw_input("enter north/south coordinate of destination: ")
    x_dest=raw_input("enter east/west coordinate of destination: ")
    #return (x_dest,y_dest)
    return (34.799872,31.90888)

def ongoing_nav(clientsock):
    SIMULATION_HOST="localhost"
    SIMULATION_PORT=53268
    SIMULATION_ADDR=(SIMULATION_HOST,SIMULATION_PORT)
    SIMULATION_BUFFSIZ=1024

    sim_socket=socket(AF_INET,SOCK_STREAM)
    sim_socket.connect(SIMULATION_ADDR)
    
    global arrived
    arrived=False
    way=eval(clientsock.recv(BUFFSIZ))
    roads=eval(clientsock.recv(BUFFSIZ))
    print way
    sim_socket.send(str(roads))
    time.sleep(1)
    #thread.start_new_thread(arrived_at_node,())
    clientsock.send(str(get_location(sim_socket)))
    done=False
    while not done:
        data=clientsock.recv(BUFFSIZ)
        if data=="done":
            done=True
        else:
            print data
            clientsock.send(str(get_location(sim_socket)))
    clientsock.close()


def one_time_nav(clientsock):
    way=eval(clientsock.recv(BUFFSIZ))
    print way
    clientsock.close()

def get_location(sim_socket):
    SIMULATION_BUFFSIZ=1024
    sim_socket.send("get loc")
    data=eval(sim_socket.recv(SIMULATION_BUFFSIZ))
    return data

##def arrived_at_node():
##    global arrived
##    while not arrived:
##        time.sleep(10)
##        data=raw_input("when arrived at node enter something, otherwise push enter: ")
##        if not data=="":
##            arrived=True

    
HOST="localhost"
PORT=55342
ADDR=(HOST,PORT)
BUFFSIZ=1024

clientsock=socket(AF_INET,SOCK_STREAM)

try:
    clientsock.connect(ADDR)
except error:
    if sys.exc_info()[1][0]==10061:
        print "server closed"
    else:
        print sys.exc_info()
        raise error
else:
    data=raw_input("enter username: ")
    clientsock.send("giora")
    data=str(get_departure())
    print data
    clientsock.send(data)
    data=str(get_destination())
    print data
    clientsock.send(data)
    data=raw_input("is ongoing navigation?: ")
    if data=="yes":
        clientsock.send("ongoing")
        ongoing_nav(clientsock)
    else:
        clientsock.send("not ongoing")
        one_time_nav(clientsock)

clientsock.close()
    
