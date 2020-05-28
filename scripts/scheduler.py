from apscheduler.schedulers.blocking import BlockingScheduler

from json import load

from constants import BOT_CONFIG_PATH
from telegram_bot import send_random_image


if __name__ == '__main__':
    config = None
    with open(BOT_CONFIG_PATH, 'r') as json_file:
        config = load(json_file)

    scheduler = BlockingScheduler()
    if config['scheduler']['start_date']:
        scheduler.add_job(
            send_random_image,
            args=[config, True],
            trigger='interval',
            seconds=config['scheduler']['seconds'],
            minutes=config['scheduler']['minutes'],
            hours=config['scheduler']['hours'],
            days=config['scheduler']['days'],
            weeks=config['scheduler']['weeks'],
            start_date=config['scheduler']['start_date'],
            end_date=config['scheduler']['end_date']
        )
    else:
        scheduler.add_job(
            send_random_image,
            args=[config, True],
            trigger='interval',
            seconds=config['scheduler']['seconds'],
            minutes=config['scheduler']['minutes'],
            hours=config['scheduler']['hours'],
            days=config['scheduler']['days'],
            weeks=config['scheduler']['weeks']
        )
    scheduler.start()
