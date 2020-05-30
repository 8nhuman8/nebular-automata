from apscheduler.schedulers.blocking import BlockingScheduler

from json import load

from constants import BOT_CONFIG_PATH, SCHEDULER_CONFIG_PATH
from telegram_bot import send_random_image


if __name__ == '__main__':
    with open(BOT_CONFIG_PATH, 'r') as json_bot_file, \
         open(SCHEDULER_CONFIG_PATH, 'r') as json_scheduler_file:
        bot_config = load(json_bot_file)
        scheduler_config = load(json_scheduler_file)

    scheduler = BlockingScheduler()
    if scheduler_config['start_date']:
        scheduler.add_job(
            send_random_image,
            args=[bot_config, True],
            trigger='interval',
            seconds=scheduler_config['seconds'],
            minutes=scheduler_config['minutes'],
            hours=scheduler_config['hours'],
            days=scheduler_config['days'],
            weeks=scheduler_config['weeks'],
            start_date=scheduler_config['start_date'],
            end_date=scheduler_config['end_date']
        )
    else:
        scheduler.add_job(
            send_random_image,
            args=[bot_config, True],
            trigger='interval',
            seconds=scheduler_config['seconds'],
            minutes=scheduler_config['minutes'],
            hours=scheduler_config['hours'],
            days=scheduler_config['days'],
            weeks=scheduler_config['weeks']
        )
    scheduler.start()
