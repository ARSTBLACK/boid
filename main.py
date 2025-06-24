import pygame
from pygame import Vector2
import random

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
        self.position += self.velocity
        self.acceleration *= 0

    def apply_behaviors(self, boids):
        coh = cohesion(self, boids)
        sep = separation(self, boids)
        ali = alignment(self, boids)
        self.acceleration += coh * 1.0 + sep * 1.5 + ali * 1.0

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), self.position, 5)

def cohesion(boid, boids):
    boidpos = boid.position
    boidvelo = boid.velocity
    running_totalx = 0
    running_totaly = 0
    for i in range(boids):
        running_totalx += boids(0[0[i]])
        running_totaly += boids(0[1[i]])
    running_averagex = running_totalx / i
    running_averagey = running_totaly / i

    return Vector2(0,0)

def separation(boid, boids):
    return Vector2(0,0)

def alignment(boid, boids):
    return Vector2(0,0)

def inRange(boid1, boid2):
    



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



