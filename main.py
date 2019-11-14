#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from threading import Thread, Lock
from time import time, sleep
from random import uniform

DIRTY = 0
CLEAN = 1

class ChandyMisraSolver(Thread):

    def __init__(self, philosophers, forks):
        self.philosophers = philosophers
        self.forks = forks


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

    def __init__(self, name, left, right, num=100):
        self.name = name
        self.left = left
        self.right = right
        self.num = num

    def dine(self):
        print("%sが食事開始" % self.name)
        for i in range(self.num):
            print("%s %2d回目の食事" % (self.name, i+1))
            self.useLeftFork()
            self.useRightFork()
            self.eat()
            self.putLeftFork()
            self.putRightFork()
        print("%sが食事終了" % self.name)

    def useLeftFork(self):
        start = time()
        self.left.use()
        print("%s 思索時間: %f [sec]" % (self.name, (time() - start)))

    def useRightFork(self):
        start = time()
        self.right.use()
        print("%s 思索時間: %f [sec]" % (self.name, (time() - start)))

    def putLeftFork(self):
        self.left.put()

    def putRightFork(self):
        self.right.put()

    def eat(self, eating_time=None):
        if eating_time:
            sleep(eating_time)
        else:
            sleep(uniform(0.75, 1.25))


if __name__ == "__main__":

    forks = [Fork() for i in range(5)]
    philosophers = [Philosopher("P%d"%(i+1), forks[i], forks[(i+1)%5]) for i in range(5)]
    threads = [Thread(target=philosophers[i].dine) for i in range(5)]
    for t in threads:
        t.start()
