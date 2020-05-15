from PIL import Image, ImageDraw
from colony import Colony
from utils import Vector, Color, generate_filename


RADIUS = Vector(100, 100)
MAX_POPULATION_COUNT = (RADIUS.x * RADIUS.y) // 2
REPRODUCE_CHANCE = 0.5

COLOR_ACCENT = Color(255, 29, 119, 255)
COLOR_BACKGROUND = Color(255, 255, 255, 255)


colony = Colony(RADIUS, MAX_POPULATION_COUNT, REPRODUCE_CHANCE)
colony.develop_colony()


image = Image.new('RGBA', (RADIUS.x, RADIUS.y))
draw = ImageDraw.Draw(image)

for x in range(RADIUS.x + 1):
    for y in range(RADIUS.y + 1):
        if colony.colony[x][y]:
            max_gen = colony.current_generation
            gen = colony.colony[x][y].gen

            alpha = round((1 - gen / max_gen) * 255)
            COLOR_ACCENT = COLOR_ACCENT._replace(a=alpha)

            draw.point([x, y], COLOR_ACCENT)
        else:
            draw.point([x, y], COLOR_BACKGROUND)


IMAGE_PATH = 'img/'
IMAGE_NAME = f'{RADIUS.x}x{RADIUS.y}_({colony.population_count}#{MAX_POPULATION_COUNT})_{REPRODUCE_CHANCE}_{generate_filename()}.png'


image.save(IMAGE_PATH + IMAGE_NAME, 'PNG')
image.show()
