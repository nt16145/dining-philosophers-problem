#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import time, sleep
from random import uniform
from threading import Thread, Lock, Condition

DIRTY = 0
CLEAN = 1

class ForkSyncManager:

    def __init__(self):
        self.condition = Condition()


    def wait(self):
        """
        All of the objects provided by this module
        that have acquire() and release() methods can be used as context managers for a with statement.
        """
        with self.condition:
            self.condition.wait()


    def notifyAll(self):
        with self.condition:
            self.condition.notify_all()



class Fork:

    def __init__(self, pid):

        self.pid = pid # philosopher's ID
        self.state = DIRTY
        self.lock = Lock()
        self.manager = ForkSyncManager()


    def request(self, pid):

        while self.pid != pid:
            if self.state == DIRTY:
                self.lock.acquire()
                self.state = CLEAN
                self.pid = pid
                self.lock.release()
            else:
                self.manager.wait()


    def done(self):

        self.state = DIRTY
        self.manager.notifyAll()



class Philosopher:

    def __init__(self, pid, name, left, right):

        self.pid = pid
        self.name = name
        self.left = left
        self.right = right

        self.thread = Thread(target=self.dine)
        self.thread.start()


    def dine(self):

        while True:
            self.eat()
            self.think()


    def eat(self):

        print("%sが左右のフォークを拾う．" % self.name)
        self.left.request(self.pid)
        self.right.request(self.pid)

        print("%sが食事中..." % self.name)
        sleep(uniform(0.2, 0.5))

        print("%sがフォークを左右に戻す．" % self.name)
        self.left.done()
        self.right.done()


    def think(self):
        print("%sが思索中..." % self.name)
        sleep(uniform(0.2, 0.5))


class Table:

    def __init__(self):
        pass


    def start(self):
        print("--- 食事開始 ---")
        PhilosopherNames = ('Aristotle','Kant','Buddha','Marx', 'Russel')
        self.forks = [Fork(p+1) for p in range(5)]
        self.philosophers = [Philosopher(i, PhilosopherNames[i], self.forks[(i%5)],self.forks[(i+1)%5]) for i in range(5)]



if __name__ == "__main__":
        table = Table()
        table.start()

