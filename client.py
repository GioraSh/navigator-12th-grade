from socket import *


def get_departure():
    y_dept=raw_input("enter north/south coordinate of departure: ")
    x_dept=raw_input("enter east/west coordinate of departure: ")
    return (x_dept,y_dept)

def get_destination():
    y_dest=raw_input("enter north/south coordinate of destination: ")
    x_dest=raw_input("enter east/west coordinate of destination: ")
    return (x_dest,y_dest)

def ongoing_nav(clientsock):
    way=eval(clientsock.recv(BUFFSIZ))
    print way
    #clientsock.send(str(get_location()))
    done=False
    while not done:
        data=clientsock.recv(BUFFSIZ)
        if data=="done":
            done=True
        else:
            print data
            data=raw_input("arrived at node: ")
            clientsock.send(data)
            #clientsock.send(str(get_location()))
    clientsock.close()


def one_time_nav(clientsock):
    way=eval(clientsock.recv(BUFFSIZ))
    print way
    clientsock.close()

def get_location():
    pass

    
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
    clientsock.send(data)
    data=str(get_departure())
    clientsock.send(data)
    data=str(get_destination())
    clientsock.send(data)
    data=raw_input("is ongoing navigation?: ")
    if data=="yes":
        clientsock.send("ongoing")
        ongoing_nav(clientsock)
    else:
        clientsock.send("not ongoing")
        one_time_nav(clientsock)

clientsock.close()
    
