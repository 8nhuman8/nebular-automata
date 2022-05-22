from collections import deque
from datetime import datetime
from random import random

from utils import Square, Vector


class Nebula:
    def __init__(self, size: Vector, max_count: int, reproduce_chance: float, starting_point: Vector | None = None, quadratic: bool = False):
        self.size = size

        if starting_point is None:
            starting_point = Vector(size.x // 2, size.y // 2)
        elif not (1 <= starting_point.x <= size.x) or (1 <= starting_point.y <= size.y):
            raise IndexError('Starting point coordinate components must be less than or equal to the size of an image.')
        self.starting_point = starting_point

        # The maximum allowable value of squares count
        if max_count is None:
            max_count = (size.x * size.y) // 2
        self.max_count = max_count

        self.reproduce_chance = reproduce_chance
        self.quadratic = quadratic

        # Current squares count
        self.count = 1
        self.current_generation = 1

        self.squares = [[None for _ in range(self.size.y + 1)] for _ in range(self.size.x + 1)]
        self.__not_reproduced_squares = deque()


    def __able_to_reproduce(self) -> bool:
        return random() < self.reproduce_chance


    def __output_debug_info(self) -> None:
        print(self.current_generation, end='\t')
        print(f'[{datetime.now().isoformat()}]', end='\t')
        print('{:.5f}'.format(self.count / self.max_count * 100), '%', end='\t')
        print(f'({self.count} / {self.max_count})')


    def __square_reproduce(self, square: Square, generation: int) -> list[Square]:
        self.count += 1

        x = square.x
        y = square.y

        neighboring_coordinates = None

        right = Vector(x + 1, y)
        up = Vector(x, y + 1)
        left = Vector(x - 1, y)
        bottom = Vector(x, y - 1)

        if self.quadratic:
            right_up = Vector(x + 1, y + 1)
            right_down = Vector(x + 1, y - 1)
            left_up = Vector(x - 1, y + 1)
            left_down = Vector(x - 1, y - 1)

            neighboring_coordinates = [right, up, left, bottom, right_up, right_down, left_up, left_down]
        else:
            neighboring_coordinates = [right, up, left, bottom]

        neighboring_squares = []
        # 'nc' stands for 'neighboring coordinate'
        for nc in neighboring_coordinates:
            if (
                nc.x <= self.size.x
                and nc.x >= 0
                and nc.y <= self.size.y
                and nc.y >= 0
                and self.__able_to_reproduce()
            ):
                if self.squares[nc.x][nc.y] is None:
                    self.squares[nc.x][nc.y] = Square(nc.x, nc.y, generation)
                    neighboring_squares.append(self.squares[nc.x][nc.y])

        return neighboring_squares


    def __get_next_generation(self, current_generation_squares: list[Square]) -> list[Square]:
        self.current_generation += 1

        next_generation_squares = []
        for square in current_generation_squares:
            next_generation_squares.extend(self.__square_reproduce(square, self.current_generation))
        return next_generation_squares


    def __destroy(self) -> None:
        self.squares = [[None for _ in range(self.size.y + 1)] for _ in range(self.size.x + 1)]
        self.count = 1
        self.current_generation = 1
        self.__not_reproduced_squares = deque()

        starting_square = Square(self.starting_point.x, self.starting_point.y, self.current_generation)
        self.squares[starting_square.x][starting_square.y] = starting_square
        self.__not_reproduced_squares.append([starting_square])


    def __develop_one_generation(self) -> None:
        self.__output_debug_info()
        current_generation_squares = self.__not_reproduced_squares.popleft()
        self.__not_reproduced_squares.append(self.__get_next_generation(current_generation_squares))


    def develop(self, min_percent: float | None = None, max_percent: float | None = None) -> None:
        starting_square = Square(self.starting_point.x, self.starting_point.y, self.current_generation)
        self.squares[starting_square.x][starting_square.y] = starting_square
        self.__not_reproduced_squares.append([starting_square])

        minp_exists = min_percent is not None
        maxp_exists = max_percent is not None
        pass_once = True

        while minp_exists or maxp_exists or pass_once:

            while self.__not_reproduced_squares != deque([[]]) and self.count <= self.max_count:
                self.__develop_one_generation()
                if maxp_exists:
                    if self.count / self.max_count >= max_percent:
                        break

            pass_once = False
            print()

            if maxp_exists:
                if self.count / self.max_count >= max_percent:
                    break
                else:
                    self.__destroy()

            if minp_exists:
                if self.count / self.max_count >= min_percent:
                    break
                else:
                    self.__destroy()
