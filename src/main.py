# @sales_dep_report_bot

from dotenv import load_dotenv
load_dotenv()

import os

import logging
import datetime
import pytz

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from reports.utils import load_data
from reports import hanging_workflows, conversion_funnel, new_paying_users


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def report(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job

    date = datetime.date.today()
    data = load_data()

    hanging_img = open(hanging_workflows.get_plot(data, date), 'rb')
    funnel_img = open(conversion_funnel.get_plot(data, date), 'rb')
    new_paying_count = new_paying_users.get_report(data, date)

    context.bot.send_photo(job.context, photo=hanging_img, caption=f'Бизнес процессы, {date}')
    context.bot.send_photo(job.context, photo=funnel_img, caption=f'Конверсия, {date}')
    context.bot.send_message(job.context, text=f'На {date} новых платных пользователей: {new_paying_count}')


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def start(update: Update, context: CallbackContext) -> None:
    """Оправляет приветствие и инструкции дл начала работы"""
    update.message.reply_text('Отчет отдела продажа. Для начала работы введите /init')


def init(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    remove_job_if_exists(str(chat_id), context)
    time = datetime.time(hour=13, minute=50, tzinfo=pytz.timezone('Europe/Moscow'))
    context.job_queue.run_daily(report, time, context=chat_id, name=str(chat_id))

    update.message.reply_text('Отчет будет выслан в 08:45 (МСК), ежедневно')


def main() -> None:
    updater = Updater(os.getenv('BOT_TOKEN'))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler('init', init))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
