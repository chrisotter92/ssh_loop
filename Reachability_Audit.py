import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from modules import ssh_device, SQL_Query
from modules.SQL_Connection import SQLConnection
from multiprocessing import Pool
from threading import Thread


def audit(device, deviceStatus):
    # Used to keep track of data in myThreads().
    hostname, ip, handler, devicetype = device.split('|')
    if 'not_supported' in handler:
        deviceStatus.append([hostname, 5])
    else:
        with ssh_device.SSH_Device(ip, handler) as ssh:
            if ssh.net_connect:
                deviceStatus.append([hostname, 1])
            elif ssh.error == "Connection timed out.":
                deviceStatus.append([hostname, 2])
            elif ssh.error == "Authentication failure.":
                deviceStatus.append([hostname, 3])
            else:
                deviceStatus.append([hostname, 4])


# Function to update SQL database
def sqlUpdate(hostname, status):
    with SQLConnection('test') as sc:
        if not sc.cursor:
            print("SQL connection failed.")
            exit()
        sc.cursor.execute('''CALL reachability ('{}', '{}')'''.format(hostname, status))
        sc.connection.commit()


# Threading function that's called by the multiprocesses, builds threads based of len of list sent
def myThreads(devices):
    # Used to keep track of the status of devices
    deviceStatus = []
    threads = len(devices)
    ranTreads = []
    for y in range(threads):
        thread = Thread(target=audit, args=[devices[y], deviceStatus])
        thread.start()
        ranTreads.append(thread)
    # Ensures all threads are done before closing existing threads
    [thread.join() for thread in ranTreads]
    return deviceStatus


def main():
    try:
        # Used to declare the number of threads wanted in each process
        spawnThreads = 50
        # SQL query to get all devices in inventory table
        sqlDict = SQL_Query.openQuery('test', 'inventory_table')
        # List of all devices
        deviceList = [('{}|{}|{}|{}'.format(sqlDict['hostname'][x], sqlDict['ip'][x], sqlDict['netmikohandler'][x],
                                               sqlDict['devicetype'][x])) for x in range(len(sqlDict['hostname']))]
        # Once deviceList is build, list of lists is build for a range of 50 devices in each list
        completeList = ([deviceList[i:i + spawnThreads] for i in range(0, len(deviceList), spawnThreads)])
        # Makes a pool of 32 (for 32 CPUs)
        pool = Pool(processes=32)
        # Maps myThreads function with an index from completeList containing a list of 50 devices
        statusLists = pool.map(myThreads, completeList)
        # Closes the pools
        pool.close()
        # Completes pool job
        pool.join()
        # Once all data is collected SQL inventory is updated for reachability status for each device
        [[sqlUpdate(devices[0], devices[1]) for devices in lists] for lists in statusLists]
    except Exception as err:
        raise err


if __name__ == '__main__':
    main()
