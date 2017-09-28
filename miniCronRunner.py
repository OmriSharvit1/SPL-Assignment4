import sqlite3
import hotelWorker
import os
import time

databaseexisted = os.path.isfile('cronhoteldb.db')
dbcon = sqlite3.connect('cronhoteldb.db')
cursor = dbcon.cursor()


def main():
    cursor.execute("SELECT * FROM TaskTimes")

    with dbcon:
        if databaseexisted:
            num_times = cursor.execute("SELECT NumTimes FROM TaskTimes").fetchall()
            first_iteration = 0
            times = []

        while databaseexisted and num_times.count((0,)) != len(num_times):
            cursor.execute("SELECT TaskId FROM TaskTimes WHERE NumTimes > 0")
            task_ids_to_do = cursor.fetchall()

            if first_iteration == 0:
                first_iteration = 1
                for task_id_to_do in task_ids_to_do:
                    cursor.execute("SELECT TaskName, Parameter FROM Tasks WHERE TaskId= (?)", task_id_to_do)
                    taskname, parameter = cursor.fetchone()
                    t = hotelWorker.dohoteltask(taskname, parameter)
                    times.append(t)
                    cursor.execute("UPDATE TaskTimes SET NumTimes=(NumTimes-1) WHERE TaskId=(?)", task_id_to_do)
            else:
                for task_id_to_do in task_ids_to_do:
                    # cursor.execute("SELECT TaskName, Parameter FROM Tasks WHERE TaskId= (?)", task_id_to_do)
                    # taskname, parameter = cursor.fetchone()
                    cursor.execute("SELECT DoEvery FROM TaskTimes WHERE TaskId=(?)", task_id_to_do)
                    do_every = cursor.fetchone()
                    do, = do_every
                    task_id, = task_id_to_do
                    cursor.execute("SELECT TaskName, Parameter FROM Tasks WHERE TaskId= (?)", task_id_to_do)
                    taskname, parameter = cursor.fetchone()
                    if int(time.time() - times[task_id]) == do:
                        t = hotelWorker.dohoteltask(taskname, parameter)
                        times[task_id] = t
                        cursor.execute("UPDATE TaskTimes SET NumTimes=(NumTimes-1) WHERE TaskId=(?)", task_id_to_do)

            num_times = cursor.execute("SELECT NumTimes FROM TaskTimes").fetchall()

if __name__ == '__main__':
    main()
