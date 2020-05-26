DESCRIPTION = ('Creates a beautiful nebula. Percentages show the duration '
               'of further program execution in ideal conditions! In fact, '
               'probability can take its toll.')

HELP_REPRODUCE_CHANCE = 'The chance the square can produce other squares.'
HELP_MAX_COUNT = ('The maximum number of squares in the image. By '
                  'default, this is half of all pixels in the future image.')
HELP_COLOR_ACCENT1 = ('The first or (primary if multicolor mode is not enabled) '
                      'color of squares. Color components must be specified '
                      'between 0 and 255. The The default color is aqua')
HELP_COLOR_BACKGROUND = ('The background color. Color components must be '
                         'specified between 0 and 255. The default color is white.')
HELP_RANDOM_COLORS = 'Accent colors will be random.'

HELP_MULTICOLOR = 'Enables multicolor mode.'
HELP_COLOR_ACCENT2 = ('The second color of squares if multicolor mode is '
                      'enabled. Color components must be specified between 0 '
                      'and 255. The The default color is (r, g, b): (255, 29, 119, 255).')

HELP_MIN_PERCENT = ('The program will work until nebula is filled '
                    'with a certain or greater percentage.')
HELP_MAX_PERCENT = ('The program will work until a nebula '
                    'is filled with a certain percentage.')
HELP_FADE_IN = ('The original color is white. The color of each '
                'new generation will fade into the specified color.')
HELP_QUADRATIC = ('Each square will be surrounded not only '
                  'on each side, but also on each corner.')
HELP_OPAQUE = 'All colors will be opaque.'

HELP_SAVE = 'The generated image will be saved in the root if no path is specified.'
HELP_PATH = ('The path by which the generated image will be saved. Write the path '
             'without quotes, separating the directories with the usual single slash.')
HELP_SHOW_IMAGE = 'Show image after execution.'

COLORS_METAVAR = ('R', 'G', 'B', 'A')


NOTIFICATION_MSG_BEFORE_RENDERING = ('Now the data will be processed and converted to a '
                                     'graphical representation.\nIt can take some time.\n')


TELEGRAM_IMAGES_SAVE_PATH = './telegram_images/'
TELERGAM_IMAGE_PREFIX = '_telegram_'
BOT_CONFIG_PATH = './configs/bot_config.json'
COLORS_CONFIG_PATH = './configs/colors_config.json'
