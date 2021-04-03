from ursina import *
import random
from utils import collide


# normal, top-down, PointLight, normal, super
# Light,DirectionalLight,PointLight,AmbientLight,SpotLight
class Lighting(PointLight):
    def __init__(self, parent, position, color_, rotation):
        super().__init__(
            parent=parent,
            position=position,
            rotation=rotation,
            shadows=True,
            color=color_

        )


class CheckPoint(Entity):
    checkpoints = []
    car = None
    lastpoint = 0

    def __init__(self, model, clr, position, scale):
        super().__init__(model=model,
                         color=clr,
                         position=position,
                         scale=scale,
                         double_sided=True,
                         collider='cube'
                         )
        self.checkpoints.append(self)
        self.light = Entity(model='cube', position=position, scale = 25, color=color.rgba(64,64,0,64))
        self.getby = round(time.time() + distance(self.car, self))

    def is_cleared(self, ignore_list):
        touching = boxcast(
            self.position,
            direction=self.up,
            distance=5,
            thickness=(20, 20),
            traverse_target=scene,
            ignore=ignore_list,
            debug=False).entities

        less_touching = [e for e in touching if 'player_car' in e.name]
        if len(less_touching) == 1:
            
            self.lastpoint = (self.getby - time.time())
            if self.lastpoint < 0:
                self.lastpoint = 0
            CheckPoint.spawn_new()
            self.checkpoints.remove(self)
            destroy(self.light, delay=0)
            destroy(self, delay=0)

            return True

    @classmethod
    def init_car(cls, car):
        cls.car = car

    @classmethod
    def init_light(cls, light):
        cls.light = light

    @classmethod
    def spawn_new(cls):

        cls('cube', 
            color.rgba(0,0,0,0),
            (random.randint(-250,250),
            0,
            random.randint(-250,250)), 
            (28,28,28)
            )
        cls.light.position = cls.checkpoints[0].position
        # cls.light.position = cls.checkpoints[0].position+Vec3(0, 20, 0)

        '''  for x in range(15):
            z = random.random() * 3 
            Obstacle(color.rgba((35*z), (20*z), (20*z)),
                     scale = (random.uniform(3, 8),
                              random.uniform(3, 25),
                              random.uniform(3, 8)))
'''


class Obstacle(Entity):
    obstacles = []
    car = None

    def __init__(self, color, scale):
        super().__init__(model='cube',
                         color=color,
                         position=(0, 0, 0),
                         scale=scale,
                         collider='cube'
                         )
        self.get_position()
        self.obstacles.append(self)

    def get_position(self):
        MAXMAP = 120
        while True:
            self.position = Vec3(random.randint(-MAXMAP, MAXMAP), (self.scale[1] // 2) - .5,
                                 random.randint(-MAXMAP, MAXMAP))
            if distance(self.position, self.car) > 20:
                break

    @classmethod
    def init_car(cls, car):
        cls.car = car

    @classmethod
    def shuffle(cls):
        for obstacle in cls.obstacles:
            obstacle.get_position()

    @classmethod
    def clear_all(cls):
        while cls.obstacles:
            cls.obstacles[-1].enabled = False
            destroy(cls.obstacles.pop(), delay=0)


class TheCar:
    BOUNDS = (120, 120)
    MAXSPEED = 1

    def __init__(self, ent):
        self.ent = ent
        self._speed = 0
        self._steering = 0
        self._hp = 100
        self.score = 0
        self.paused = True
        self.new_game = True
        self.audio_list = []
        self.lights = False
        self.light_time = 100
        self.story_time = time.time() + 10

    @property
    def hp(self):
        return self._hp if self._hp > 0 else 0

    @hp.setter
    def hp(self, x):
        if x == None:
            self._hp = 100
        else:
            self._hp = x

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, x):
        if x == None:
            self._speed = 0
        if x == 0:
            self._speed *= .994
            if abs(self._speed) < .001:
                self._speed = 0
        elif x == 1:
            self._speed += time.dt * .1
            if self._speed < .33:
                self._speed += time.dt * .05
                if self._speed < .1:
                    self._speed += time.dt * .05
                    if self._speed < 0:
                        self._speed += time.dt * .1

            if self._speed > self.MAXSPEED:
                self._speed = self.MAXSPEED
        elif x == -1:
            self._speed -= time.dt * .1
            if self._speed > 0:
                self._speed -= time.dt * .15
                if self._speed > .5:
                    self._speed -= time.dt * .2

            if self._speed < -self.MAXSPEED:
                self._speed = -self.MAXSPEED

    @property
    def steering(self):
        return self._steering

    @steering.setter
    def steering(self, x):
        if x == None:
            self._steering *= .8
            if abs(self.steering < 2):
                self._steering = 0
        if x == 0:
            self._steering *= .92
            if abs(self._steering) < 2:
                self._steering = 0
        if x == 1:
            self._steering += 2
            if self._steering < -40:
                self._steering += 6
            if self._steering < 0:
                self._steering += 4
            if self._steering > 100:
                self._steering = 100
        if x == -1:
            self._steering -= 2
            if self._steering > 40:
                self._steering -= 6
            if self._steering > 0:
                self._steering -= 4
            if self._steering < -100:
                self._steering = -100

    def move(self, ignore_list):
        if self.speed > 0:
            if collide(self.ent.position, self.ent.forward, 2.5, ignore_list, self._speed):
                speed = self.speed
                if self.lights:
                    self.hp -= self.speed * 20
                    self.light_time -= self.speed * 40
                else:
                    self.hp -= self.speed * 40
                self.speed = None
                return speed
        if self.speed < 0:
            if collide(self.ent.position, self.ent.back, 2.3, ignore_list, self._speed):
                speed = self.speed
                if self.lights:
                    self.hp -= abs(self.speed) * 20
                    self.light_time -= abs(self.speed) * 40
                else:
                    self.hp -= abs(self.speed) * 40
                self.speed = None
                return -speed
        self.ent.position += self.ent.forward * self.speed
        return 0

    def pause(self):
        self.paused = not self.paused

    def rotate(self):
        if self.steering > 0:
            offset = 1
        elif self.steering < 0:
            offset = -1
        else:
            offset = 0
        if abs(self.speed) > 0.01:
            reverse_multiplier = 1
            if self.speed < 0:
                reverse_multiplier = -1
            self.ent.rotation += Vec3(0, (self.steering * time.dt + (abs(self.speed) * offset)) * reverse_multiplier, 0)

    def w(self):
        self.speed = 1

    def s(self):
        self.speed = -1

    def a(self):
        self.steering = -1

    def d(self):
        self.steering = 1

    def brake(self, coasting):
        self._speed *= .99
        if not coasting:
            self._speed -= (1 - self.speed) * time.dt
        if self._speed < .01:
            self._speed = 0


class Arrow(Entity):
    def __init__(self):
        super().__init__(model='assets/models/arrow',
                color=color.rgba(70, 40, 40, 200))
