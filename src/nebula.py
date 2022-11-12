from collections import deque
from datetime import datetime
from random import random

from utils import Square, Vector


class Nebula:
    def __init__(self, size: Vector, max_count: int, reproduce_chance: float, starting_point: Vector, quadratic: bool):
        self.size = size
        self.max_count = max_count
        self.reproduce_chance = reproduce_chance
        self.starting_point = starting_point
        self.quadratic = quadratic

        # Current squares count
        self.current_count = 1
        self.current_generation = 1

        self.squares = [[None for _ in range(self.size.y + 1)] for _ in range(self.size.x + 1)]
        self.__not_reproduced_squares = deque()
        self.population = []


    def __able_to_reproduce(self) -> bool:
        return random() < self.reproduce_chance


    def __output_debug_info(self) -> None:
        print(self.current_generation, end='\t')
        print(f'[{datetime.now().isoformat()}]', end='\t')
        print(f'{self.current_count / self.max_count * 100 : .5f} %', end='\t')
        print(f'({self.current_count} / {self.max_count})')


    def __square_reproduce(self, square: Square, generation: int) -> list[Square]:
        self.current_count += 1

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
                0 <= nc.x <= self.size.x and
                0 <= nc.y <= self.size.y and
                self.__able_to_reproduce() and
                self.squares[nc.x][nc.y] is None
            ):
                self.squares[nc.x][nc.y] = Square(nc.x, nc.y, generation)
                neighboring_squares.append(self.squares[nc.x][nc.y])

        return neighboring_squares


    def __get_next_generation(self, current_generation_squares: list[Square]) -> list[Square]:
        self.current_generation += 1

        next_generation_squares = []
        for square in current_generation_squares:
            next_generation_squares.extend(self.__square_reproduce(square, self.current_generation))

        self.population.append(next_generation_squares)

        return next_generation_squares


    def __destroy(self) -> None:
        self.squares = [[None for _ in range(self.size.y + 1)] for _ in range(self.size.x + 1)]
        self.current_count = 1
        self.current_generation = 1
        self.__not_reproduced_squares = deque()

        starting_square = Square(self.starting_point.x, self.starting_point.y, self.current_generation)
        self.population = []

        self.squares[starting_square.x][starting_square.y] = starting_square
        self.__not_reproduced_squares.append([starting_square])


    def __develop_one_generation(self) -> None:
        self.__output_debug_info()
        current_generation_squares = self.__not_reproduced_squares.popleft()
        self.__not_reproduced_squares.append(self.__get_next_generation(current_generation_squares))


    def develop(self, min_percent: float | None = None, max_percent: float | None = None) -> None:
        starting_square = Square(self.starting_point.x, self.starting_point.y, self.current_generation)
        self.population.append([starting_square])

        self.squares[starting_square.x][starting_square.y] = starting_square
        self.__not_reproduced_squares.append([starting_square])

        pass_once = True

        while min_percent or max_percent or pass_once:
            while self.__not_reproduced_squares != deque([[]]) and self.current_count <= self.max_count:
                self.__develop_one_generation()
                if max_percent:
                    if self.current_count / self.max_count >= max_percent:
                        break

            print()
            pass_once = False

            if max_percent:
                if self.current_count / self.max_count >= max_percent:
                    break
                else:
                    self.__destroy()

            if min_percent:
                if self.current_count / self.max_count >= min_percent:
                    break
                else:
                    self.__destroy()
