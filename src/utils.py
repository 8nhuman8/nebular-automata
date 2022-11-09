from collections import namedtuple
from math import ceil
from random import choice, randint
from string import ascii_letters, digits
from typing import Callable


Square = namedtuple('Square', ['x', 'y', 'gen'])
Vector = namedtuple('Vector', ['x', 'y'])
Color = namedtuple('Color', ['r', 'g', 'b', 'a'])


def generate_filename(size: int = 18) -> str:
    chars = ascii_letters + digits
    return ''.join(choice(chars) for _ in range(size))


def benchmark(func: Callable) -> Callable:
    from datetime import datetime

    def wrapper(*args, **kwargs):
        start_datetime = datetime.now()
        return_value = func(*args, **kwargs)
        end_datetime = datetime.now()

        print(f'\nStart date: {start_datetime.isoformat()}')
        print(f'End date: {end_datetime.isoformat()}')
        print(f'Program took: {end_datetime - start_datetime} to run\n')

        return return_value

    return wrapper


def random_colors(n: int) -> list[Color]:
    return [random_color() for _ in range(n)]


def random_color() -> Color:
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    a = randint(0, 255)
    return Color(r, g, b, a)


# gens: int -- generations count
def gradient(gens: int, colors: list[Color]) -> list[Color]:
    gens_for_color = ceil(gens / (len(colors) - 1))

    grads = []
    for i in range(len(colors) - 1):
        grads.append(gradient2(gens_for_color, colors[i], colors[i + 1]))

    remaining_gens = gens - (len(colors) - 2) * gens_for_color
    remaining_gens = remaining_gens if remaining_gens != 0 else 1
    grads.append(gradient2(remaining_gens, colors[len(colors) - 2], colors[len(colors) - 1]))

    gradient_ = []
    for grad in grads:
        gradient_.extend(grad)

    return gradient_


# gens: int -- generations count
# c1: Color -- color 1
# c2: Color -- color 2
def gradient2(gens: int, c1: Color, c2: Color) -> list[Color]:
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

    # cc1 - color component of the 1st color
    # cc2 - color component of the 2nd color
    # d_c - difference
    def fill_grad(cc1: int, cc2: int, d_c: int, grad_list: list[int]) -> list[int]:
        sign = lambda x: (x > 0) - (x < 0)
        t = cc1
        d_cc = cc2 - cc1
        for _ in range(gens - 1):
            t += sign(d_cc) * d_c
            grad_list.append(round(t))
        return grad_list

    grad_r = fill_grad(c1.r, c2.r, d_r, grad_r)
    grad_g = fill_grad(c1.g, c2.g, d_g, grad_g)
    grad_b = fill_grad(c1.b, c2.b, d_b, grad_b)
    grad_a = fill_grad(c1.a, c2.a, d_a, grad_a)

    return [Color(*color) for color in list(zip(grad_r, grad_g, grad_b, grad_a))]
