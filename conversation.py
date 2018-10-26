from datetime import datetime, date, time
import Time


class Task():
    def __init__(self, date, task):
        self.date = date
        self.task = task

    def __eq__(self, other):
        return self.date == other.date and self.task == other.task

    def __str__(self):
        return 'Когда: {}. Задача: {}.'.format(self.date, self.task)

    def get_date(self):
        return self.date

    def get_task(self):
        return self.task


class TaskManager():
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def get_all_tasks(self):
        return self.tasks


def create_task(input_string):
    parsed_input_string = Time.Time().parse(input_string)
    if not parsed_input_string:
        return None
    if not parsed_input_string[0] or not parsed_input_string[1]:
        return None
    task_object = Task(parsed_input_string[0], parsed_input_string[1])
    return task_object
