from datetime import datetime
from random import random

from utils import Square, Vector

from constants import TIME_FORMAT


class Nebula:
    def __init__(self,
        size: Vector,
        max_count: int,
        probability: float,
        start_point: Vector,
        directions: list[Vector]
    ) -> None:
        self.size = size
        self.max_count = max_count
        self.probability = probability
        self.start_point = start_point
        self.directions = directions

        self.reset()


    def reset(self) -> None:
        self.count = 1
        self.generation = 1

        start_square = Square(*self.start_point)

        self.grid = [[None] * self.size.x for _ in range(self.size.y)]
        self.grid[start_square.y][start_square.x] = start_square

        self.generations = [[start_square]]
        self._unreproduced_squares = [[start_square]]


    def develop(self, min_percent: float | None, max_percent: float | None) -> None:
        pass_once = False

        while min_percent or max_percent or not pass_once:
            while self._unreproduced_squares[0] and self.count <= self.max_count:
                self.output_debug_info()
                self.develop_generation()

                if max_percent:
                    if self.count / self.max_count >= max_percent:
                        break

            print()
            pass_once = True

            if max_percent:
                if self.count / self.max_count >= max_percent:
                    break
                else:
                    self.reset()

            if min_percent:
                if self.count / self.max_count >= min_percent:
                    break
                else:
                    self.reset()


    def develop_generation(self) -> None:
        current_generation = self._unreproduced_squares.pop()
        next_generation = self._next_generation(current_generation)
        self._unreproduced_squares.append(next_generation)


    def output_debug_info(self) -> None:
        print(self.generation, end='\t')
        print(datetime.now().strftime(TIME_FORMAT), end='\t')
        print(f'{self.count / self.max_count * 100 : .5f} %', end='\t')
        print(f'{self.count} / {self.max_count}')


    def _next_generation(self, current_generation: list[Square]) -> list[Square]:
        self.generation += 1

        next_generation = []
        for square in current_generation:
            neighbors = self._square_reproduce(square)
            next_generation.extend(neighbors)

        if next_generation:
            self.generations.append(next_generation)

        return next_generation


    def _square_reproduce(self, square: Square) -> list[Square]:
        self.count += 1

        y, x = square
        neighbors = []

        for direction in self.directions:
            ny = y + direction.y
            nx = x + direction.x

            if (0 <= ny <= self.size.y - 1 and
                0 <= nx <= self.size.x - 1 and
                self._able_to_reproduce() and
                self.grid[ny][nx] is None
            ):
                neighbor = Square(ny, nx)
                self.grid[ny][nx] = neighbor
                neighbors.append(neighbor)

        return neighbors


    def _able_to_reproduce(self) -> bool:
        return random() < self.probability
