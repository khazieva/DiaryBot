from datetime import datetime, date, time, timedelta
import Time


class Task():
    def __init__(self, task_date, task):
        assert isinstance(task_date, datetime) or isinstance(task_date, date)
        self.date = task_date
        self.task = task

    def __eq__(self, other):
        return self.date == other.date and self.task == other.task

    def __str__(self):
        return 'Когда: {}. Задача: {}.'.format(self.date, self.task)

    def __get_date_object(self):
        if isinstance(self.date, datetime):
            return self.date.date()
        else:
            return self.date

    def get_date(self):
        return self.date

    def get_task(self):
        return self.task

    def is_today(self):
        return self.__get_date_object() == datetime.today().date()

    def is_tomorrow(self):
        return self.__get_date_object() == datetime.today().date() + timedelta(days=1)

    def is_outdated(self):
        return self.__get_date_object() < datetime.today().date()


class TaskManager():
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        assert isinstance(task, Task)
        self.tasks.append(task)

    def get_all_tasks(self):
        return self.tasks

    def get_tasks_for_today(self):
        task_today = []
        for task in self.tasks:
            if task.is_today():
                task_today.append(task)
        return task_today

    def get_tasks_for_tomorrow(self):
        task_tomorrow = []
        for task in self.tasks:
            if task.is_tomorrow():
                task_tomorrow.append(task)
        return task_tomorrow

    def remove_outdated_tasks(self):
        actual_tasks = []
        for task in self.tasks:
            if not task.is_outdated():
                actual_tasks.append(task)
        self.tasks = actual_tasks


def create_task(input_string):
    parsed_input_string = Time.Time().parse(input_string)
    if not parsed_input_string:
        return None
    if not parsed_input_string[0] or not parsed_input_string[1]:
        return None
    task_object = Task(parsed_input_string[0], parsed_input_string[1])
    return task_object
