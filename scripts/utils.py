from collections import namedtuple
from string import ascii_lowercase, ascii_uppercase, digits
from random import choice, randint
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
    print(f'Program took: {datetime.now() - start_date} to run\n')


def get_renadom_colors(n: int) -> list:
    return [get_random_color() for _ in range(n)]


def get_random_color() -> tuple:
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    a = randint(0, 255)
    return (r, g, b, a)


def get_opaque_color(c: Color) -> Color:
    return c._replace(a=255)


# gens: int -- generations count
def get_gradient(gens: int, colors: list) -> list:
    gradient = get_gradient2(gens // (len(colors) - 1), colors[0], colors[1])

    grads = []
    for i in range(1, len(colors) - 1):
        if i == len(colors) - 2:
            remaining_gens = gens - (len(colors) - 2) * (gens // (len(colors) - 1))
            grads.append(get_gradient2(remaining_gens, colors[i], colors[i + 1]))
        else:
            grads.append(get_gradient2(gens // (len(colors) - 1), colors[i], colors[i + 1]))

    for grad in grads:
        gradient.extend(grad)

    return gradient


# gens: int -- generations count
# c1: Color -- color 1
# c2: Color -- color 2
def get_gradient2(gens: int, c1: Color, c2: Color) -> list:
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
