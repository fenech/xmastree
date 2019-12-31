from gpiozero import PiHutXmasTree
from gpiozero.tools import random_values
from time import sleep

tree = PiHutXmasTree(pwm=True)

indices = [19, 22, 4, 23, 8, 2, 16, 15, 17, 13, 24, 20, 6, 7, 12, 3, 14, 1, 10, 11, 21, 9, 5, 18]
lights = [tree[i] for i in indices]
num_lights = len(indices)

def reset():
  for light in lights:
    light.off()

def snake(i):
  lights[i%num_lights].on()
  lights[(i+1)%num_lights].on()
  lights[(i+2)%num_lights].on()
  lights[(i-1)%num_lights].off()

reset()

tree.star.source_delay = 0.1
tree.star.source = random_values()

while True:
  for _ in range(3):
    for i, _ in enumerate(indices):
      snake(i)
      snake(i+num_lights//2)
      sleep(0.1)

  reset()

  clone = lights.copy()
  while len(clone) > 0:
    for i, _ in enumerate(clone):
      lights[i].on()
      if i > 0:
        lights[i-1].off()
      sleep(0.05)
    clone.pop()

  for light in lights:
    light.source_delay = 0.1
    light.source = random_values()

  sleep(6)

  for light in lights:
    light.source = None
