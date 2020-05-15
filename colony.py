from random import random
from collections import deque
from utils import Square, Vector
 

class Colony:
    def __init__(self, radius, max_population_count, reproduce_chance):
        self.radius = radius
        self.starting_point = Vector(self.radius.x // 2, self.radius.y // 2)

        self.max_population_count = max_population_count
        self.reproduce_chance = reproduce_chance

        self.population_count = 1
        self.current_generation = 1

        self.colony = [[None for y in range(self.radius.y + 1)] for x in range(self.radius.x + 1)]
        self.not_reproduced_squares = deque()


    def __able_to_reproduce__(self):
        return random() < self.reproduce_chance


    def __output_execution_percentage__(self):
        print(round(self.population_count / self.max_population_count * 100, 2), '%', sep='', end='\t')
        print(f'({self.population_count} / {self.max_population_count})')


    def __square_reproduce__(self, square, generation):
        self.population_count += 1

        x = square.x
        y = square.y

        right = Vector(x + 1, y)
        up = Vector(x, y + 1)
        left = Vector(x - 1, y)
        bottom = Vector(x, y - 1)

        neighboring_coordinates = [right, up, left, bottom]
        neighboring_squares = []

        # 'nc' stands for 'neighboring coordinate'
        for nc in neighboring_coordinates:
            if (
                nc.x <= self.radius.x
                and nc.x >= 0
                and nc.y <= self.radius.y
                and nc.y >= 0
                and self.__able_to_reproduce__()
            ):
                if not self.colony[nc.x][nc.y]:
                    self.colony[nc.x][nc.y] = Square(nc.x, nc.y, generation)
                    neighboring_squares.append(self.colony[nc.x][nc.y])

        return neighboring_squares


    def __get_next_generation__(self, current_generation_squares):
        self.current_generation += 1

        next_generation_squares = []
        for square in current_generation_squares:
            next_generation_squares.extend(self.__square_reproduce__(square, self.current_generation))
        return next_generation_squares


    def develop_colony(self):
        starting_square = Square(self.starting_point.x, self.starting_point.y, self.current_generation)
        self.colony[starting_square.x][starting_square.y] = starting_square
        self.not_reproduced_squares.append([starting_square])

        while (self.not_reproduced_squares != deque([[]])) and (self.population_count <= self.max_population_count):
            self.__output_execution_percentage__()
            current_generation_squares = self.not_reproduced_squares.popleft()
            self.not_reproduced_squares.append(self.__get_next_generation__(current_generation_squares))
