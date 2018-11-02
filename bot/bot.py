import Time
import test_time
import test_conversation
import conversation
from datetime import datetime, date
import time
import threading
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import sys


# Логирование.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


task_managers = dict()


class ReminderHandler():
    def __init__(self):
        self.actual_date = date.today()
        self.today_reminder_sent = False
        self.tomorrow_reminder_sent = False

    # Метод для отправки напоминаний.
    def update(self, updater):
        hour = datetime.now().hour

        # Проверяем, сменился ли день.
        if date.today() > self.actual_date:
            self.actual_date = date.today()
            self.today_reminder_sent = False
            self.tomorrow_reminder_sent = False
            filter_tasks()

        # Проверяем, нужно ли отправить напоминание о сегодняшних задачах.
        if self.today_reminder_sent is False and hour >= 9:
            self.today_reminder_sent = True
            for chat_id in task_managers.keys():
                send_today_tasks(updater, chat_id)

        # Проверяем, нужно ли отправить напоминание о завтрашних задачах.
        if self.tomorrow_reminder_sent is False and hour >= 20:
            self.tomorrow_reminder_sent = True
            for chat_id in task_managers.keys():
                send_tomorrow_tasks(updater, chat_id)


def start(bot, update):
    task_managers[update.effective_chat.id] = conversation.TaskManager()
    update.message.reply_text("Привет!")


# Функция для ответа на сообщение.
def reply_message(bot, update):
    task = conversation.create_task(update.message.text.lower())
    if task is None:
        update.message.reply_text('Не могу распознать задачу.')
    else:
        task_managers[update.effective_chat.id].add_task(task)
        update.message.reply_text('Задача {} добавлена.'.format(task.get_task()))


# Функция для вывода всех задач.
def tasks(bot, update):
    tasks_list = task_managers[update.effective_chat.id].get_all_tasks()
    all_tasks = '\n'.join(map(str, tasks_list))
    update.message.reply_text(all_tasks if len(all_tasks) > 0 else "Нет запланированных задач.")


# Функция для вывода задач на сегодня.
def tasks_for_today(bot, update):
    tasks_list = task_managers[update.effective_chat.id].get_tasks_for_today()
    today_tasks = '\n'.join(map(str, tasks_list))
    update.message.reply_text(today_tasks if len(today_tasks) > 0 else "На сегодня ничего не запланировано.")


# Функция для вывода задач на завтра.
def tasks_for_tomorrow(bot, update):
    tasks_list = task_managers[update.effective_chat.id].get_tasks_for_tomorrow()
    tomorrow_tasks = '\n'.join(map(str, tasks_list))
    update.message.reply_text(tomorrow_tasks if len(tomorrow_tasks) > 0 else "На завтра ничего не запланировано.")


# Функция для отправки задач на сегодня.
def send_today_tasks(updater, chat_id):
    tasks_list = task_managers[chat_id].get_tasks_for_today()
    today_tasks = '\n'.join(map(str, tasks_list))
    updater.bot.send_message(chat_id, today_tasks if len(today_tasks) > 0 else "На сегодня ничего не запланировано.")


# Функция для отправки задач на завтра.
def send_tomorrow_tasks(updater, chat_id):
    tasks_list = task_managers[chat_id].get_tasks_for_tomorrow()
    tomorrow_tasks = '\n'.join(map(str, tasks_list))
    updater.bot.send_message(chat_id, tomorrow_tasks if len(tomorrow_tasks) > 0 else
                             "На завтра ничего не запланировано.")


# Функция для удаления просроченных задач.
def filter_tasks():
    for task_manager in task_managers.values():
        task_manager.remove_outdated_tasks()


# Функция для обновления.
def run_updater(updater):
    reminder_handler = ReminderHandler()
    while True:
        reminder_handler.update(updater)
        time.sleep(60)


# Функция для запуска потока обновления данных.
def start_updater(updater):
    t = threading.Thread(target=run_updater, args=(updater,))
    t.daemon = True
    t.start()


# Функция для удобного отображения ошибок.
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


# Функция для вывода подсказки по использованию.
def show_help():
    print('Использование бота: python bot.py --token [your_token]\n'
          'Запуск тестов: python bot.py --test')


def bot_help(bot, update):
    update.message.reply_text('Доступные команды:\n''/start - начало работы с ботом;\n'
                              '/help - вывод доступных команд;\n''/задачи - вывод всех запланированных задач;\n'
                              '/сегодня - вывод задач на сегодня;\n''/завтра - вывод задач на завтра.\n')


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
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", bot_help))
    dp.add_handler(CommandHandler("задачи", tasks))
    dp.add_handler(CommandHandler("сегодня", tasks_for_today))
    dp.add_handler(CommandHandler("завтра", tasks_for_tomorrow))
    dp.add_error_handler(error)

    start_updater(updater)

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
