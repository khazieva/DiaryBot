import Time
import test_time
import test_conversation
import conversation
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import sys


# Логирование.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


TaskManager_object = conversation.TaskManager()


# Функция для ответа на сообщение.
def reply_message(bot, update):
    task = conversation.create_task(update.message.text)
    if task is None:
        update.message.reply_text('Не могу распознать задачу.')
    else:
        TaskManager_object.add_task(task)
        update.message.reply_text('Задача {} добавлена'.format(task.get_task()))


# Функция для вывода всех задач.
def tasks(bot, update):
    tasks_list = TaskManager_object.get_all_tasks()
    all_tasks = '\n'.join(map(str, tasks_list))
    update.message.reply_text(all_tasks if len(all_tasks) > 0 else "Нет запланированных задач")


# Функция для удобного отображения ошибок.
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


# Функция для вывода подсказки по использованию.
def show_help():
    print('Использование бота: python bot.py --token [your_token]\n'
          'Запуск тестов: python bot.py --test')


# Функция для получения токена.
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

    dp.add_handler(MessageHandler(Filters.text, reply_message))
    dp.add_handler(CommandHandler("задачи", tasks))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
        exit()

    if sys.argv[1] == '--test':
        test_time.run_tests()
        test_conversation.run_tests()
    elif sys.argv[1] == '--token':
        token = get_token(sys.argv[1:])
        main(token)
    else:
        exit()
