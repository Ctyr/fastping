"""
Fast icmp ping tool.
Authors: TyrChen
Date:    2015/09/01
"""
import threading
import Queue
import subprocess
import os
import sys

__author__ = 'TyrChen'


def pinger(ip):
    with open(os.devnull, 'w') as dev_null:
        try:
            subprocess.check_call(['ping', '-c1', ip], stdout=dev_null)
        except:
            return False
        else:
            return True


def ping(jobs, result):
    ip = jobs.get()
    if pinger(ip):
        result.put(ip)


def fastping(net, start, end):

    jobs = Queue.Queue()
    result = Queue.Queue()
    thread_list = []

    for i in range(start, end):
        ip = '192.168.%d.%d' % (net, i)
        jobs.put(ip)
        thread = threading.Thread(target=ping, args=(jobs, result))
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

    result_list = []
    while not result.empty():
        result_list.append(result.get())
    return result_list

if __name__ == '__main__':

    if len(sys.argv) > 4 or len(sys.argv) < 2:
        print 'Usage: %s net [start] [end]' % sys.argv[0]
        exit(1)

    start = sys.argv[2] if len(sys.argv) == 3 else 1
    end = sys.argv[3] if len(sys.argv) == 4 else 254
    net = sys.argv[1]
    start, end, net = map(int, [start, end, net])

    result = fastping(net, start, end)

    for ip in sorted(result, key=lambda x: int(x.split('.')[3])):
        print ip
