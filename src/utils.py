from collections import namedtuple
from dataclasses import astuple, dataclass
from datetime import datetime
from math import ceil
from random import choice, randint
from string import ascii_letters, digits
from typing import Any, Callable, ParamSpec, TypeVar

from numpy import array, ndarray

from constants import TIME_FORMAT


P = ParamSpec('P')
T = TypeVar('T')


Square = namedtuple('Square', ['y', 'x'])
Vector = namedtuple('Vector', ['y', 'x'])


@dataclass
class Color:
    r: int
    g: int
    b: int
    a: int

    def __array__(self) -> ndarray:
        return array(astuple(self))

    def __len__(self) -> int:
        return astuple(self).__len__()

    def __getitem__(self, item: Any) -> int:
        return astuple(self).__getitem__(item)


direction_to_vector = {
    'bottom_left':  Vector(1, -1),
    'left':         Vector(0, -1),
    'top_left':     Vector(-1, -1),
    'bottom':       Vector(1, 0),
    'top':          Vector(-1, 0),
    'bottom_right': Vector(1, 1),
    'right':        Vector(0, 1),
    'top_right':    Vector(-1, 1)
}


def unique_code(size: int = 5) -> str:
    characters = ascii_letters + digits
    return ''.join(choice(characters) for _ in range(size))


def benchmark(function: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start_time = datetime.now()
        return_value = function(*args, **kwargs)
        end_time = datetime.now()

        print(f'\nStart time: {start_time.strftime(TIME_FORMAT)}')
        print(f'End time: {end_time.strftime(TIME_FORMAT)}')
        print(f'Program took {end_time - start_time} to run\n')

        return return_value

    return wrapper


def random_colors(n: int) -> list[Color]:
    return [random_color() for _ in range(n)]


def random_color() -> Color:
    return Color(*[randint(0, 255) for _ in range(4)])


def polylinear_gradient(colors: list[Color], n: int) -> list[Color]:
    if len(colors) == 1:
        return colors

    n_out = ceil(n / (len(colors) - 1))
    gradient = []

    for i in range(len(colors) - 1):
        gradient_btw_two = linear_gradient(colors[i], colors[i + 1], n_out)
        gradient.extend(gradient_btw_two)

    return gradient


def linear_gradient(start_color: Color, finish_color: Color, n: int) -> list[Color]:
    gradient = [start_color]

    for i in range(1, n):
        gradient_color = []

        for cc in range(4):
            step = i * (finish_color[cc] - start_color[cc]) / (n - 1)
            gradient_color.append(start_color[cc] + int(step))

        gradient.append(Color(*gradient_color))

    return gradient
