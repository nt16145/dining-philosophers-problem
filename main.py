#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from threading import Thread, Lock
from time import time, sleep
from random import uniform

# mutex resource
class Fork:
    def __init__(self):
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

class Table:

    def __init__(self):
        self.forks = [Fork() for i in range(5)]
        self.philosophers = [Philosopher(i, self.forks[i], self.forks[(i+1)%5]) for i in range(5)]
        self.threads = [Thread(target=self.philosophers[i].dine) for i in range(5)]

    def start(self):
        for t in self.threads:
            t.start()

if __name__ == "__main__":

    table = Table()
    table.start()

