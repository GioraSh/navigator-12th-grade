import sqlite3 as lite

def enter_nodes(file_name):
    conn=lite.connect(file_name)
    conn.commit()
    cursor=conn.cursor()

    try:
        cursor.execute("""SELECT id FROM nodes""")
        r=cursor.fetchall()
        #last id
        r=r[-1][0]+1
        identity=r
    except IndexError:
        identity=0

    print identity
    done=False
    while not done:
        st_name=raw_input("done?: ")
        print st_name
        if st_name!="done":
            south=eval(raw_input("south: "))
            if south=="":
                south=None
            east=eval(raw_input("east: "))
            if east=="":
                east=None
            north=eval(raw_input("north: "))
            if north=="":
                north=None
            west=eval(raw_input("west: "))
            if west=="":
                west=None
            min_x=eval(raw_input("min_x: "))
            max_x=eval(raw_input("max_x: "))
            min_y=eval(raw_input("min_y: "))
            max_y=eval(raw_input("max_y: "))
            cursor.execute("""INSERT INTO nodes(id,south,east,north,west,min_x,max_x,min_y,max_y) VALUES(?,?,?,?,?,?,?,?,?)""",(identity,south,east,north,west,min_x,max_x,min_y,max_y))
            conn.commit()
            identity=identity+1
        else:
            done=True
        
def enter_road(file_name):
    conn=lite.connect(file_name)
    conn.commit()
    cursor=conn.cursor()

    try:
        cursor.execute("""SELECT id FROM roads""")
        r=cursor.fetchall()
        #last id
        r=r[-1][0]+1
        identity=r
    except IndexError:
        identity=0

    done=False
    while not done:
        st_name=eval(raw_input("done?: "))
        if st_name!="done":
            start=eval(raw_input("enter start id: "))
            end=eval(raw_input("enter end id: "))
            max_speed=50
            distance=eval(raw_input("enter distance: "))
            direction=eval(raw_input("enter direction: "))
            cursor.execute("""INSERT INTO roads(id,start_node_id,end_node_id,max_speed,distance,name,direction) VALUES(?,?,?,?,?,?,?)""",(identity,start,end,max_speed,distance,st_name,direction))
            conn.commit()
            identity=identity+1
        else:
            done=True

def print_streets(file_name):
    conn=lite.connect(file_name)
    conn.commit()
    cursor=conn.cursor()
    cursor.execute("""SELECT name FROM roads""")
    print cursor.fetchall()
