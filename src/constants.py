from pathlib import Path


# Required options
HELP_WIDTH = 'The width of the image.'
HELP_HEIGHT = 'The height of the image.'

# Basic options
HELP_START_POINT = 'The coordinate of a starting point. Default value: middle of the image.'
HELP_PROBABILTY = 'The probability that a square will multiply in a one direction. Default value: 0.51'
HELP_MAX_COUNT = 'The maximum number of squares in the image. Default value: (width * height) // 2.'
HELP_MIN_PERCENT = 'The program will work until the nebula is filled with a chosen or greater percentage.'
HELP_MAX_PERCENT = 'The program will work until the nebula is filled with a chosen percentage.'

# Multicolor options
HELP_RANDOM_COLORS = 'All colors will be chosen randomly.'
HELP_RANDOM_BACKGROUND = 'The background color will be chosen randomly.'
HELP_COLORS_NUMBER = 'The number of colors to use in the image. Default value: 3. Use with: -rc.'

# Additional options
HELP_OPAQUE = 'All colors will be opaque including background.'
HELP_FADE_IN = 'Starting color is white. The color of each new generation will fade into the specified color. Use with: -rc -cn 1'

# Image options
HELP_SAVE_IMAGE = 'The rendered image will be saved.'
HELP_PATH_IMAGE = 'The path where the image will be saved. Default path: output/'
HELP_DONT_SHOW_IMAGE = 'Do not show image in the end.'

# Video options
HELP_SAVE_VIDEO = 'The rendered video will be saved.'
HELP_PATH_VIDEO = 'The path where the video will be saved. Default path: output/'
HELP_VIDEO_SIZE = 'The size of the video in MB to which the size of the original video will be reduced using compression.'

# GIF options
HELP_SAVE_GIF = 'The rendered GIF will be saved.'
HELP_PATH_GIF ='The path where the GIF will be saved. Default path: output/'


# Formats
TIME_FORMAT = '%H:%M:%S:%f'


# Program paths
CONFIG_PATH = Path('configs/config.json')
OUTPUT_FILES_PATH = Path('output/')
TEMP_VIDEO_PATH = (OUTPUT_FILES_PATH / 'temp.mp4').as_posix()
