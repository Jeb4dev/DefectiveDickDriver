from ursina import *
import random
from utils import collide

class TheCar:
    MAXSPEED = 1

    def __init__(self, speed, steering, ent):
        self._speed = speed
        self._steering = steering
        self.ent = ent
        self.forward = None

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, x):
        print(x)
        if x is None:
            self._speed = 0
            self.forward = None
        elif x == 0:
            self._speed *= .9999
        elif x == 1:
            self._speed += time.dt * .1
            if self._speed > self.MAXSPEED:
                self._speed = self.MAXSPEED
        elif x == -1:
            self._speed -= time.dt * .1
            if self._speed < -self.MAXSPEED:
                self._speed = -self.MAXSPEED

    @property
    def steering(self):
        return self._steering

    @steering.setter
    def steering(self, x):
        if x == 0:
            self._steering *= .95
            if self._steering < 1:
                self._steering = 0
        if x == 1:
            self._steering += 1
            if self._steering > 40:
                self._steering = 40
        if x == -1:
            self._steering -= 1
            if self._steering < -40:
                self._steering = -40

    def move(self, ignore_list):
        if self.forward:
            if not collide(self.ent.position, self.ent.forward, 2.5, ignore_list):
                self.speed = None
            if self.speed > 0:
                self.ent.position += self.ent.forward * self.speed
            elif self.speed < 0:
                self.ent.position -= self.ent.forward * - self.speed
        elif self.forward == False:
            if not collide(self.ent.position, self.ent.back, 2.1, ignore_list):
                self.speed = None
            if self.speed > 0:
                self.ent.position += self.ent.forward * -self.speed
            elif self.speed < 0:
                self.ent.position -= self.ent.forward * self.speed

    def rotate(self):
        if self.steering > 0:
            offset = 1
        elif self.steering < 0:
            offset = -1
        else:
            offset = 0
        if self.forward is True:
            self.ent.rotation += Vec3(0, self.steering * time.dt + (self.speed * offset), 0)
        elif self.forward is False:
            self.ent.rotation -= Vec3(0, self.steering * time.dt + (self.speed * offset), 0)

    def w(self):
        print(self.forward, self.speed, 'w')
        if self.forward == None:
            print('forward = none, now true')
            self.forward = True
            print(self.forward)
        if self.forward:
            self.speed = 1 
        if self.forward == False:
            if self.speed < 0:
                self.speed = 1

    def s(self):
        print(self.forward, self.speed, 's')
        if self.forward == None:
            print('none, now false')
            self.forward = False
        if self.forward:
            print('slowing down with s')
            if self.speed > 0:
                self.speed = -1
        if self.forward == False:
            print('speeding up with s')
            self.speed = 1

    def a(self):
        self.steering = -1

    def d(self):
        self.steering = 1

    def brake(self):
        self._speed *= .995
        if self._speed < .01:
            self._speed = 0

