# Program descripton
DESCRIPTION = ('Creates a beautiful nebula. Percentages show the duration '
               'of further program execution in ideal conditions! In fact, '
               'probability can take its toll.')

# Basic options
HELP_STARTING_POINT = "The coordinate of a starting point. By default it's in the middle."
HELP_REPRODUCE_CHANCE = "The chance the square can produce other squares. By default it's 0.51"
HELP_MAX_COUNT = 'The maximum number of squares in the image. By default, this is half of all pixels in the future image.'

# Multicolor options
HELP_RANDOM_COLORS = 'All colors will be random.'
HELP_RANDOM_BACKGROUND = 'Background color will be random'
HELP_OPAQUE = 'All colors will be opaque.'
HELP_COLORS_NUMBER = "How many colors will be used. By default it's 3. Must be used with '--random-colors' argument."

# Additional options
HELP_MIN_PERCENT = 'The program will work until nebula is filled with a certain or greater percentage.'
HELP_MAX_PERCENT = 'The program will work until a nebula is filled with a certain percentage.'
HELP_FADE_IN = 'The original color is white. The color of each new generation will fade into the specified color.'
HELP_QUADRATIC = 'Each square will be surrounded not only on each side, but also on each corner.'

# System options
HELP_SAVE = 'The generated image will be saved in the root if no path is specified.'
HELP_PATH = 'The path by which the generated image will be saved. Write the path without quotes, separating the directories with the usual single slash.'
HELP_DONT_SHOW_IMAGE = 'Do not show image after execution.'

# Notification messages
NOTIFICATION_MSG_BEFORE_RENDERING = '\nNow the data will be processed and converted to a graphical representation.\nIt can take some time.\n'

# Formats
IMAGE_FORMAT = '.png'
VIDEO_CODEC = 'avc1'
VIDEO_FORMAT = '.mp4'

# Program paths
COLORS_CONFIG_PATH = 'configs/colors_config.json'
OUTPUT_PATH = 'output/'

# Other
TARGET_VIDEO_MB_SIZE = 5
VIDEO_FRAMERATE = 60.0
