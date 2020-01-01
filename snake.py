from gpiozero import PiHutXmasTree
from gpiozero.tools import random_values
from time import sleep
from random import choice

def reset(lights):
  for light in lights:
    light.off()


def snake_step(i):
  lights[i%num_lights].on()
  lights[(i+1)%num_lights].on()
  lights[(i+2)%num_lights].on()
  lights[(i-1)%num_lights].off()


def snake(lights):
  for _ in range(3):
    for i, _ in enumerate(lights):
      snake_step(i)
      snake_step(i+num_lights//2)
      sleep(0.1)

  reset(lights)


def chase(lights):
  if len(lights) == 0:
    return

  for i, _ in enumerate(lights):
    lights[i].on()
    if i > 0:
      lights[i-1].off()
    sleep(0.05)

  chase(lights[:-1])


def flicker(lights):
  for light in lights:
    light.source_delay = 0.1
    light.source = random_values()

  sleep(6)

  for light in lights:
    light.source = None


def blink(lights):
  for _ in range(8):
    thirds = len(lights) // 3
    for i in range(3):
      for light in tree[i*thirds:(i+1)*thirds]:
        light.on()
      sleep(0.2)
      for light in tree[i*thirds:(i+1)*thirds]:
        light.off()


def dnb(lights):
  for r in range(1, 6):
    for _ in range(2, 2**r):
      for light in lights:
        light.on()
      sleep(1/(2**r))
      for light in lights:
        light.off()
      sleep(1/(2**r))


tree = PiHutXmasTree(pwm=True)

indices = [19, 22, 4, 23, 8, 2, 16, 15, 17, 13, 24, 20, 6, 7, 12, 3, 14, 1, 10, 11, 21, 9, 5, 18]
lights = [tree[i] for i in indices]
num_lights = len(indices)

reset(lights)

tree.star.source_delay = 0.1
tree.star.source = random_values()

effects = [snake, chase, flicker, blink, dnb]

while True:
  choice(effects)(lights)
