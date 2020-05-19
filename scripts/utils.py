from collections import namedtuple
from string import ascii_lowercase, ascii_uppercase, digits
from random import choice
from datetime import datetime


Square = namedtuple('Square', ['x', 'y', 'gen'])
Vector = namedtuple('Vector', ['x', 'y'])
Color = namedtuple('Color', ['r', 'g', 'b', 'a'])


def generate_filename(size: int=18) -> str:
    chars = ascii_lowercase + ascii_uppercase + digits
    return ''.join(choice(chars) for _ in range(size))


def get_runtime(start_date: datetime) -> None:
    print(f'\nStart date: {start_date.isoformat()}')
    print(f'End date: {datetime.now().isoformat()}')
    print(f'Program took: {datetime.now() - start_date} to run')


# gen: int -- generations count
# c1: Color -- color 1
# c2: Color -- color 2
def get_gradient(gen: int, c1: Color, c2: Color) -> list:
    # differences
    d_r = abs(c1.r - c2.r) / gen
    d_g = abs(c1.g - c2.g) / gen
    d_b = abs(c1.b - c2.b) / gen
    d_a = abs(c1.a - c2.a) / gen

    # gradient lists
    grad_r = [c1.r]
    grad_g = [c1.g]
    grad_b = [c1.b]
    grad_a = [c1.a]

    # t: int -- temporary copy of the color component
    if c1.r < c2.r:
        t = c1.r
        for _ in range(2, gen + 1):
            t += d_r
            grad_r.append(round(t))
    else:
        t = c1.r
        for _ in range(2, gen + 1):
            t -= d_r
            grad_r.append(round(t))

    if c1.g < c2.g:
        t = c1.g
        for _ in range(2, gen + 1):
            t += d_g
            grad_g.append(round(t))
    else:
        t = c1.g
        for _ in range(2, gen + 1):
            t -= d_g
            grad_g.append(round(t))

    if c1.b < c2.b:
        t = c1.b
        for _ in range(2, gen + 1):
            t += d_b
            grad_b.append(round(t))
    else:
        t = c1.b
        for _ in range(2, gen + 1):
            t -= d_b
            grad_b.append(round(t))

    if c1.a < c2.a:
        t = c1.a
        for _ in range(2, gen + 1):
            t += d_a
            grad_a.append(round(t))
    else:
        t = c1.a
        for _ in range(2, gen + 1):
            t -= d_a
            grad_a.append(round(t))

    return list(zip(grad_r, grad_g, grad_b, grad_a))
