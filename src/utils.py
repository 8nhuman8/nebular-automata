from collections import namedtuple
from string import ascii_letters, digits
from random import choice, randint
from typing import Callable


Square = namedtuple('Square', ['x', 'y', 'gen'])
Vector = namedtuple('Vector', ['x', 'y'])
Color = namedtuple('Color', ['r', 'g', 'b', 'a'])


def generate_filename(size: int = 18) -> str:
    chars = ascii_letters + digits
    return ''.join(choice(chars) for _ in range(size))


def benchmark(func: Callable) -> Callable:
    from datetime import datetime

    def wrapper(*args):
        start_datetime = datetime.now()
        func(*args)
        end_datetime = datetime.now()

        print(f'\nStart date: {start_datetime.isoformat()}')
        print(f'End date: {end_datetime.isoformat()}')
        print(f'Program took: {end_datetime - start_datetime} to run\n')

    return wrapper


def random_colors(n: int) -> list:
    return [random_color() for _ in range(n)]


def random_color() -> tuple:
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    a = randint(0, 255)
    return [r, g, b, a]


# gens: int -- generations count
def gradient(gens: int, colors: list) -> list:
    colors = [Color(*color) for color in colors]

    grads = []
    for i in range(len(colors) - 1):
        if i == len(colors) - 2:
            remaining_gens = gens - (len(colors) - 2) * (gens // (len(colors) - 1))
            grads.append(gradient2(remaining_gens, colors[i], colors[i + 1]))
        else:
            grads.append(gradient2(gens // (len(colors) - 1), colors[i], colors[i + 1]))

    gradient = []
    for grad in grads:
        gradient.extend(grad)

    return gradient


# gens: int -- generations count
# c1: Color -- color 1
# c2: Color -- color 2
def gradient2(gens: int, c1: Color, c2: Color) -> list:
    # differences
    d_r = abs(c1.r - c2.r) / gens
    d_g = abs(c1.g - c2.g) / gens
    d_b = abs(c1.b - c2.b) / gens
    d_a = abs(c1.a - c2.a) / gens

    # gradient lists
    grad_r = [c1.r]
    grad_g = [c1.g]
    grad_b = [c1.b]
    grad_a = [c1.a]

    # t: int -- temporary copy of the color component
    t = c1.r
    if c1.r < c2.r:
        for _ in range(gens - 1):
            t += d_r
            grad_r.append(round(t))
    else:
        for _ in range(gens - 1):
            t -= d_r
            grad_r.append(round(t))

    t = c1.g
    if c1.g < c2.g:
        for _ in range(gens - 1):
            t += d_g
            grad_g.append(round(t))
    else:
        for _ in range(gens - 1):
            t -= d_g
            grad_g.append(round(t))

    t = c1.b
    if c1.b < c2.b:
        for _ in range(gens - 1):
            t += d_b
            grad_b.append(round(t))
    else:
        for _ in range(gens - 1):
            t -= d_b
            grad_b.append(round(t))

    t = c1.a
    if c1.a < c2.a:
        for _ in range(gens - 1):
            t += d_a
            grad_a.append(round(t))
    else:
        for _ in range(gens - 1):
            t -= d_a
            grad_a.append(round(t))

    return list(zip(grad_r, grad_g, grad_b, grad_a))
