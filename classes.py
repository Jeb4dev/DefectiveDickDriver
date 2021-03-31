from ursina import *
import random
from utils import collide
# normal, top-down, PointLight, normal, super
# Light,DirectionalLight,PointLight,AmbientLight,SpotLight


class Lighting(AmbientLight):
    def __init__(self, parent, position, color_):
        super().__init__(
            parent=parent,
            position=position,
            shadows=True,
            color=color_


        )



class CheckPoint(Entity):

    checkpoints = []
    car = None

    def __init__(self, model, color, position, scale):
        super().__init__(model=model, 
                         color=color, 
                         position=position, 
                         scale=scale, 
                         double_sided=True,
                         collider = 'cube'
                        )
        self.checkpoints.append(self)

    def is_cleared(self, ignore_list):
        touching = boxcast(self.position,
            direction=self.up,
            distance=5,
            thickness=(20,20),
            traverse_target=scene,
            ignore=ignore_list,
            debug=False).entities
        less_touching = [e for e in touching if 'Cube' not in e.name 
                                             and 'check_point' not in e.name 
                                             and 'terrain' not in e.name]
        if len(less_touching) == 1:
            self.__del__()
            CheckPoint.spawn_new()
            return True
        
    def __del__(self):
        self.disable()
        self.checkpoints.remove(self)

    @classmethod
    def init_car(cls, car):
        car = car

    @classmethod
    def spawn_new(cls):
        cls('cube', color.rgba(255,255,0,64), (random.randint(-100,100), 0, random.randint(-100,100)), (20,20,20))
        



class TheCar:
    BOUNDS = (120,120)
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
            self._steering *= .92
            if abs(self._steering) < .1:
                self._steering = 0
        if x == 1:
            self._steering += 1
            if self._steering > 60:
                self._steering = 60
        if x == -1:
            self._steering -= 1
            if self._steering < -60:
                self._steering = -60

    def move(self, ignore_list):
        if self.forward:
            if not collide(self.ent.position, self.ent.forward, 2.5, ignore_list, self._speed):
                self.speed = None
            if self.speed > 0:
                self.ent.position += self.ent.forward * self.speed
            elif self.speed < 0:
                self.ent.position -= self.ent.forward * - self.speed
        elif self.forward == False:
            if not collide(self.ent.position, self.ent.back, 2.1, ignore_list, self._speed):
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
        if self.forward is True and abs(self.speed) > 0.01:
            self.ent.rotation += Vec3(0, self.steering * time.dt + (self.speed * offset), 0)
        elif self.forward is False and abs(self.speed) > 0.01:
            self.ent.rotation -= Vec3(0, self.steering * time.dt + (self.speed * offset), 0)

    def w(self):
        if self.forward == None:
            self.forward = True
        if self.forward:
            self.speed = 1 
        if self.forward == False:
            if self.speed < 0:
                self.speed = 1

    def s(self):
        if self.forward == None:
            self.forward = False
        if self.forward:
            if self.speed > 0:
                self.speed = -1
        if self.forward == False:
            self.speed = 1

    def a(self):
        self.steering = -1

    def d(self):
        self.steering = 1

    def brake(self, coasting):
        self._speed *= .99
        if not coasting:
            self._speed -= (1-self.speed) * time.dt
        if self._speed < .01:
            self._speed = 0




