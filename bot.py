import Time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import sys


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def show_datetime(bot, update):
    date = Time.Time(update.message.text)
    parsed_date = date.parse()
    if parsed_date is None:
        update.message.reply_text('Не могу распознать дату.')
    else:
        update.message.reply_text(str(parsed_date))


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def show_help():
    print('Использование бота: python bot.py --token [your_token]\n\
Запуск тестов: python bot.py --test')


def get_token(list_of_args):
    if len(list_of_args) == 2:
        token = list_of_args[1]
    else:
        show_help()
        exit()
    return token


def main(token):
    updater = Updater(token)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, show_datetime))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    if sys.argv[1] == '--test':
        Time.run_tests()
    elif sys.argv[1] == '--token':
        token = get_token(sys.argv[1:])
        main(token)
    else:
        exit()
