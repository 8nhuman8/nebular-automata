from random import random
from collections import deque
from datetime import datetime

from utils import Square, Vector


class Nebula:
    def __init__(self, size: Vector, max_count: int, reproduce_chance: float, quadratic: bool = False):
        self.size = size
        self.starting_point = Vector(self.size.x // 2, self.size.y // 2)

        # The maximum allowable value of squares count
        self.max_count = max_count
        self.reproduce_chance = reproduce_chance
        self.quadratic = quadratic

        # Current squares count
        self.count = 1
        self.current_generation = 1

        self.squares = [[None for y in range(self.size.y + 1)] for x in range(self.size.x + 1)]
        self.not_reproduced_squares = deque()


    def _able_to_reproduce(self) -> bool:
        return random() < self.reproduce_chance


    def _output_debug_info(self) -> None:
        print(self.current_generation, end='\t')
        print(f'[{datetime.now().isoformat()}]', end='\t')
        print('{:.5f}'.format(self.count / self.max_count * 100), '%', end='\t')
        print(f'({self.count} / {self.max_count})')


    def _square_reproduce(self, square: Square, generation: int) -> list:
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
                and self._able_to_reproduce()
            ):
                if self.squares[nc.x][nc.y] is None:
                    self.squares[nc.x][nc.y] = Square(nc.x, nc.y, generation)
                    neighboring_squares.append(self.squares[nc.x][nc.y])

        return neighboring_squares


    def _get_next_generation(self, current_generation_squares: list) -> list:
        self.current_generation += 1

        next_generation_squares = []
        for square in current_generation_squares:
            next_generation_squares.extend(self._square_reproduce(square, self.current_generation))
        return next_generation_squares


    def _destroy(self) -> None:
        self.squares = [[None for y in range(self.size.y + 1)] for x in range(self.size.x + 1)]
        self.count = 1
        self.current_generation = 1
        self.not_reproduced_squares = deque()

        starting_square = Square(self.starting_point.x, self.starting_point.y, self.current_generation)
        self.squares[starting_square.x][starting_square.y] = starting_square
        self.not_reproduced_squares.append([starting_square])


    def develop(self, min_percent: float = None, max_percent: float = None) -> None:
        starting_square = Square(self.starting_point.x, self.starting_point.y, self.current_generation)
        self.squares[starting_square.x][starting_square.y] = starting_square
        self.not_reproduced_squares.append([starting_square])

        if min_percent:
            while True:
                while self.not_reproduced_squares != deque([[]]) and self.count <= self.max_count:
                    self._output_debug_info()
                    current_generation_squares = self.not_reproduced_squares.popleft()
                    self.not_reproduced_squares.append(self._get_next_generation(current_generation_squares))

                print()
                if self.count / self.max_count >= min_percent:
                    break
                else:
                    self._destroy()
        elif max_percent:
            while True:
                while self.not_reproduced_squares != deque([[]]) and self.count <= self.max_count:
                    self._output_debug_info()
                    current_generation_squares = self.not_reproduced_squares.popleft()
                    self.not_reproduced_squares.append(self._get_next_generation(current_generation_squares))

                    if self.count / self.max_count >= max_percent:
                        break

                print()
                if self.count / self.max_count >= max_percent:
                    break
                else:
                    self._destroy()
        else:
            while self.not_reproduced_squares != deque([[]]) and self.count <= self.max_count:
                self._output_debug_info()
                current_generation_squares = self.not_reproduced_squares.popleft()
                self.not_reproduced_squares.append(self._get_next_generation(current_generation_squares))
            print()
