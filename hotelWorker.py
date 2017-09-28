import sqlite3
import time

dbcon = sqlite3.connect('cronhoteldb.db')
cursor = dbcon.cursor()



# def convertTupleToString(rooms):


def dohoteltask(taskname, parameter):
    if taskname == "wakeup" or taskname == "breakfast":

        cursor.execute("SELECT FirstName FROM Residents WHERE RoomNumber=(?)", (parameter,))
        firstname = cursor.fetchone()
        cursor.execute("SELECT LastName FROM Residents WHERE RoomNumber=(?)", (parameter,))
        lastname = cursor.fetchone()
        firstname_string, = firstname
        lastname_string, = lastname

        if taskname == "wakeup":
            print (firstname_string + " " + lastname_string + " in room " + str(parameter) +
                   " received a wakeup call at " + str(time.time()))
        else:
            print (firstname_string + " " + lastname_string + " in room " + str(parameter) +
                   " has been served breakfast at " + str(time.time()))

    else:
        cursor.execute("SELECT t1.RoomNumber FROM Rooms t1 LEFT JOIN Residents t2 ON t1.RoomNumber=t2.RoomNumber "
                       "WHERE t2.RoomNumber IS NULL")
        rooms = cursor.fetchall()
        output = 'Rooms '
        for room in rooms:
            output += str(room[0])
            output += ', '
            output = output.strip(',')
        output = output[:-2]
        output += " were cleaned at "
        output += str(time.time())
        print(output)
    return time.time()
