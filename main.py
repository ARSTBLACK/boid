import pygame
from pygame import Vector2
import random
import math


pygame.init()
windowx = 800
windowy = 800
screen = pygame.display.set_mode((windowx, windowy))
background_colour = (234, 212, 252)
pygame.display.set_caption('birb')
pygame.display.flip()
birdgenct = 50
clock = pygame.time.Clock()
running = True

class Boid:
    def __init__(self, position, velocity):
        self.position = position  # 2D vector
        self.velocity = velocity
        self.acceleration = Vector2(0, 0)

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.length() > 4:  # <-- clamp speed
            self.velocity = self.velocity.normalize() * 4

        self.position += self.velocity
        self.acceleration *= 0

    def apply_behaviors(self, boids):
        coh = cohesion(self, boids)
        sep = separation(self, boids)
        ali = alignment(self, boids)
        bor = border(self, 50)
        self.acceleration += coh * 1.0 + sep * 1.5 + ali * 1.0 + bor * 1.0

    def draw(self, screen):
        # pygame.draw.circle(screen, (255, 255, 0), self.position, 5)
        angle = math.atan2(self.velocity.y, self.velocity.x)
        size = 10
        tip = self.position + self.velocity.normalize() * size

        left = self.position + Vector2(
            math.cos(angle + math.pi * 0.75),
            math.sin(angle + math.pi * 0.75)
        ) * size * 0.5

        right = self.position + Vector2(
            math.cos(angle - math.pi * 0.75),
            math.sin(angle - math.pi * 0.75)
        ) * size * 0.5
        pygame.draw.polygon(screen, (255, 255, 0), [tip, left, right])

        
def cohesion(boid, boids):
    boidpos = boid.position
    running_totalx = 0
    running_totaly = 0
    count = 0
    

    for bird in boids:
        if inRange(boid, bird, 50) and boid != bird:
            running_totalx += bird.position.x
            running_totaly += bird.position.y
            count += 1

    if count != 0:
        running_averagex = running_totalx / count
        running_averagey = running_totaly / count
        avgBoid = Vector2(running_averagex, running_averagey)
        steer = avgBoid - boidpos
        if steer.length() > 0.1:
            steer = steer.normalize() * 0.1
        return steer
    else:
        return Vector2(0, 0)
    
def separation(boid, boids):
    boidpos = boid.position
    steer = Vector2(0,0)
    count = 0
    for bird in boids:
        if (tooClose(boid, bird, 25)) and boid!=bird:  
            diff = boidpos - bird.position
            distance = boidpos.distance_to(bird.position)
            if distance != 0:
                steer += diff / distance
                count += 1
    if count > 0:
        steer /= count
    if steer.length() > 0.1:
        steer = steer.normalize() * 0.1
    return steer


def alignment(boid, boids):
    boidvel = boid.velocity
    steer = Vector2(0,0)
    count = 0
    totalVel = Vector2(0,0)
    avgVel = totalVel
    for bird in boids:
        if (inRange(boid, bird, 50)):
            totalVel = totalVel + bird.velocity
            count += 1
    if count > 0:
        avgVel = totalVel / count
        steer = avgVel - boid.velocity
        if steer.length() > 0.1:
            steer = steer.normalize() * 0.1
        return steer
    else:
        return Vector2(0, 0)

def border(boid, startOfEffect):
    posX = boid.position.x
    posY = boid.position.y
    steer = Vector2(0,0)
    
    if posX < startOfEffect:
        steer = steer + Vector2((startOfEffect - posX) / startOfEffect, 0)
    if posX > windowx - startOfEffect:
        steer = steer + Vector2((windowx - posX) / startOfEffect * -1, 0)

    if posY < startOfEffect:
        steer = steer + Vector2(0, (startOfEffect - posY) / startOfEffect)
    if posY > windowy - startOfEffect:
        steer = steer + Vector2(0, (windowy - posY) / startOfEffect * -1)

    return steer


def inRange(boid1, boid2, distance):
    pos1 = boid1.position
    pos2 = boid2.position
    return pos1.distance_to(pos2) < distance

def tooClose(boid1, boid2, distance):
    pos1 = boid1.position
    pos2 = boid2.position
    return pos1.distance_to(pos2) < distance  

boids = list()
for _ in range(birdgenct):
    birdx = random.random() * windowx 
    birdy = random.random() * windowy
    boids.append(Boid(Vector2(birdx, birdy), Vector2(random.randint(-1, 1), random.randint(-1, 1))))
    

while running:
    screen.fill(background_colour)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for boid in boids:
        boid.apply_behaviors(boids)
        boid.update()
        boid.draw(screen)

    pygame.display.flip()
    clock.tick(60)