#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from threading import Thread, Lock
from time import time, sleep
from random import uniform

DIRTY = 0
CLEAN = 1

class ChandyMisraSolver(Thread):

    def __init__(self):
        self.forks = [Fork() for i in range(5)]
        self.philosophers = [Philosopher("P%d"%(i+1), forks[i], forks[(i+1)%5]) for i in range(5)]

    def sendMessageFrom(self, philosopher):
        i = self.philosophers.index(philosopher)
        self.philosophers[(i-1)%5].receiveMessage()
        self.philosophers[(i+1)%5].receiveMessage()

    def execute(self):
        threads = [Thread(target=philosophers[i].dine) for i in range(5)]
        for t in threads:
            t.start()


# mutex resource
class Fork:
    def __init__(self, state=DIRTY):
        self.state = state
        self.lock = Lock()
    def use(self):
        self.lock.acquire() # lock
    def put(self):
        self.lock.release() # unlock


class Philosopher:

    def __init__(self, ID, left, right, num=100):
        self.ID = ID
        self.left = left
        self.right = right
        self.num = num

    def dine(self):
        print("%dが食事開始" % self.ID)
        for i in range(self.num):
            print("%d %2d回目の食事" % (self.ID, i+1))
            self.useLeftFork()
            self.useRightFork()
            self.eat()
            self.putLeftFork()
            self.putRightFork()
        self.left.state = DIRTY
        self.right.state = DIRTY
        print("%dが食事終了" % self.ID)

    def useLeftFork(self):
        start = time()
        self.left.use()
        print("%d 思索時間: %f [sec]" % (self.ID, (time() - start)))

    def useRightFork(self):
        start = time()
        self.right.use()
        print("%d 思索時間: %f [sec]" % (self.ID, (time() - start)))

    def putLeftFork(self):
        self.left.put()

    def putRightFork(self):
        self.right.put()

    def eat(self, eating_time=None):
        if eating_time:
            sleep(eating_time)
        else:
            sleep(uniform(0.1, 0.2))

    def receiveMessage(self):
        if self.left.state == DIRTY:
            self.left.state = CLEAN
            self.putLeftFork()
        if self.right.state == DIRTY:
            self.right.state = CLEAN
            self.putRightFork()

if __name__ == "__main__":

    solver = ChandyMisraSolver()
    solver.execute()
