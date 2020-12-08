from gpiozero import PiHutXmasTree
from gpiozero.tools import random_values
from time import sleep
from signal import pause
from random import choice


def reset(lights):
    for light in lights:
        light.off()


def snake_source(offset, period):
    while True:
        for i in range(period):
            yield offset <= i % period < offset + 3


def snake(lights, tree):
    period = len(lights) // 2
    for i, light in enumerate(lights):
        light.source_delay = 0.1
        light.source = snake_source(i % period, period)


def chase_source(lights, offset):
    num_lights = len(lights)

    while True:
        for c in range(num_lights):
            for i in range(num_lights - c):
                yield i == offset or offset > num_lights - c
        for i in range(num_lights):
            yield 1
        for i in range(num_lights):
            yield offset < num_lights - i


def chase(lights, tree):
    for i, light in enumerate(lights):
        light.source_delay = 0.05
        light.source = chase_source(lights, i)


def flicker(lights, tree):
    for light in lights:
        light.source_delay = 0.1
        light.source = random_values()


def blink_source(lights, offset):
    num_lights = len(lights)
    parts = 3

    while True:
        for i in range(parts):
            yield offset // (num_lights // parts) == i


def blink(lights, tree):
    for i, light in enumerate(tree[1:]):
        light.source_delay = 0.2
        light.source = blink_source(lights, i)


def dnb_source(light):
    while True:
        for r in range(1, 6):
            for _ in range(2, 2**r):
                yield 0
                yield 1
            light.source_delay = 1/(2**r)


def dnb(lights, tree):
    for light in lights:
        light.source = dnb_source(light)


if __name__ == "__main__":
    tree = PiHutXmasTree(pwm=True)

    ordered_indices = [19, 22, 4, 23, 8, 2, 16, 15, 17, 13,
                       24, 20, 6, 7, 12, 3, 14, 1, 10, 11, 21, 9, 5, 18]
    lights = [tree[i] for i in ordered_indices]

    reset(lights)

    tree.star.source_delay = 0.1
    tree.star.source = random_values()

    effects = [snake, chase, flicker, blink, dnb]

    while True:
        choice(effects)(lights, tree)
        sleep(24)
