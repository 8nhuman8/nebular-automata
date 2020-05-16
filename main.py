from PIL import Image, ImageDraw
from argparse import ArgumentParser
from colony import Colony
from utils import Vector, Color, generate_filename


if __name__ == '__main__':
    parser = ArgumentParser(description='Develop a beautiful square colony')
    parser.add_argument('width', type=int, help='The width of the image')
    parser.add_argument('height', type=int, help='The height of the image')
    parser.add_argument('-rc', '--reproduce_chance', metavar='RC', type=float, default=0.5, help='The chance the square can produce other squares')
    parser.add_argument('-mpc', '--max_population_count', metavar='MPC', type=int, help='The maximum number of squares in the image')
    parser.add_argument('-ca', '--color_accent', metavar=('R', 'G', 'B'), nargs=3, type=int, default=(255, 29, 119), help='The color of squares')
    parser.add_argument('-cb', '--color_background', metavar=('R', 'G', 'B', 'A'), nargs=4, type=int, default=(255, 255, 255, 255), help='The background color')
    parser.add_argument('-fp', '--find_percent', metavar='FP', type=float, help='The program will work until a colony is filled with a certain percentage')
    parser.add_argument('-fi', '--fade_in', action='store_true', help='The original color is white. The color of each new generation will fade into the specified color')
    parser.add_argument('-s', '--save', action='store_true', help='The generated image will be saved in the root')
    parser.add_argument('-p', '--path', type=str, help='The path by which the generated image will be saved')
    args = parser.parse_args()

    radius = Vector(args.width, args.height)
    max_population_count = args.max_population_count
    if not max_population_count:
        max_population_count = (radius.x * radius.y) // 2
    color_accent = Color(*args.color_accent, 255)
    color_background = Color(*args.color_background)

    colony = Colony(radius, max_population_count, args.reproduce_chance)
    colony.develop()

    if args.find_percent:
        while True:
            if colony.population_count / colony.max_population_count <= args.find_percent:
                colony.destroy()
                colony.develop()
            else:
                break

    image = Image.new('RGBA', (radius.x, radius.y))
    draw = ImageDraw.Draw(image)

    for x in range(radius.x + 1):
        for y in range(radius.y + 1):
            if colony.colony[x][y]:
                max_gen = colony.current_generation
                gen = colony.colony[x][y].gen

                alpha = None
                if args.fade_in:
                    alpha = round(gen / max_gen * 255)
                else:
                    alpha = round((1 - gen / max_gen) * 255)
                color_accent = color_accent._replace(a=alpha)

                draw.point([x, y], color_accent)
            else:
                draw.point([x, y], color_background)

    image_name = f'{radius.x}x{radius.y}_({colony.population_count}#{max_population_count})_{args.reproduce_chance}_{generate_filename()}.png'
    if args.save:
        if args.path:
            image.save(args.path + image_name, 'PNG')
        else:
            image.save(image_name, 'PNG')
    image.show()
