#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import time, sleep
from random import uniform
from threading import Thread, Lock, Condition

DIRTY = 0
CLEAN = 1

class SyncChannel:

    def __init__(self):
        self.lock = Lock()
        self.condition = Condition(self.lock)

    def wait(self):
        # This "with" statement do "acquire(lock)" and "release(unlock)".
        with self.condition:
            self.condition.wait()

    def notifyAll(self):
        with self.condition:
            self.condition.notifyAll()


class TableSetup:

    def __init__(self):
        self.done = False
        self.channel = SyncChannel()



class Fork:

    def __init__(self, fid, pid):
        self.fid = fid # forks's ID
        self.pid = pid # philosopher's ID
        self.state = DIRTY
        self.lock = Lock()
        self.channel = SyncChannel()


    def request(self, pid):
        while self.pid != pid:
            if self.state == DIRTY:
                self.lock.acquire()
                self.state = CLEAN
                self.pid = pid
                self.lock.release()
            else:
                self.channel.wait()

    def done(self):
        print("%d: done!" % self.pid)
        self.state = DIRTY
        self.channel.notifyAll()



class Philosopher:

    def __init__(self, pid, name, table_setup, left, right):
        self.pid = pid
        self.name = name
        self.setup = table_setup
        self.left = left
        self.right = right

        self.thread = Thread(target=self.dine)
        self.thread.start()


    def dine(self):
        self.setup.channel.wait()

        self.think()
        self.eat()
        while not self.setup.done:
            self.think()
            self.eat()


    def eat(self):

        self.left.request(self.pid)
        self.right.request(self.pid)

        print("%sが左右のフォークを拾う．" % self.name)
        #self.left.lock.acquire()
        #self.right.lock.acquire()

        print("%sが食事中..." % self.name)

        print("%sがフォークを左右に戻す．" % self.name)

        self.left.done()
        self.right.done()
        #self.left.lock.release()
        #self.right.lock.release()


    def think(self):
        print("%sが思索中..." % self.name)


class Table:

    """
             F5
          P1    P5
       F1          F4
    P2                P4
        F2       F3
             P3
    """

    def __init__(self):
        self.setup = TableSetup()
        self.forks = [Fork(1, 1), Fork(2, 2), Fork(3, 3), Fork(4, 4), Fork(5, 1)]
        self.philosophers = [Philosopher(1, "P1", self.setup, self.forks[0], self.forks[1]),
                             Philosopher(2, "P2", self.setup, self.forks[1], self.forks[2]),
                             Philosopher(3, "P3", self.setup, self.forks[2], self.forks[3]),
                             Philosopher(4, "P4", self.setup, self.forks[3], self.forks[4]),
                             Philosopher(5, "P5", self.setup, self.forks[4], self.forks[0])]


    def start(self):
        print("--- 食事開始 ---")
        self.setup.channel.notifyAll()


    def stop(self):
        print("--- 食事終了 ---")
        self.setup.done = False



if __name__ == "__main__":

    table = Table()
    table.start()
