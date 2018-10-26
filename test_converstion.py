import converstion
from datetime import datetime, date, time


def test_get_date(name, input_datetime, result):
    a = converstion.Task(input_datetime, '')
    got = a.get_date()
    to_show = "passed" if got == result else "failed"
    print("Test get_date {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_get_task(name, input_string, result):
    a = converstion.Task(datetime.today(), input_string)
    got = a.get_task()
    to_show = "passed" if got == result else "failed"
    print("Test get_task {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_create_task(name, input_string, result):
    got = converstion.create_task(input_string)
    to_show = "passed" if got == result else "failed"
    print("Test create_task {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_add_task(name, input_task, result):
    a = converstion.TaskManager()
    a.add_task(input_task)
    got = a.tasks
    to_show = "passed" if got == result else "failed"
    print("Test add_task {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_get_all_tasks(name, input_tasks):
    a = converstion.TaskManager()
    a.tasks = input_tasks
    got = a.get_all_tasks()
    to_show = "passed" if got == input_tasks else "failed"
    print("Test get_all_tasks {} {}, got '{}', expected '{}'.".format(name, to_show, got, input_tasks))


def run_tests_get_date():
    test_get_date("1", datetime(2018, 11, 15, 22, 50), datetime(2018, 11, 15, 22, 50))
    test_get_date("2", datetime.today().date(), datetime.today().date())


def run_tests_get_task():
    test_get_task("1", 'сходить к врачу', 'сходить к врачу')
    test_get_task("2", 'тренировка', 'тренировка')


def run_tests_create_task():
    test_create_task("1", '2018/11/15 22:50', None)
    test_create_task("2", '', None)
    test_create_task("3", 'сходить к врачу', None)
    test_create_task("4", '2018/11/15 22:50 сходить к врачу',
                     converstion.Task(datetime(2018, 11, 15, 22, 50), ' сходить к врачу'))
    test_create_task("5", 'сегодня в 15:00 сходить к врачу',
                     converstion.Task(datetime.combine(date.today(), time(15, 00)), ' сходить к врачу'))


def run_tests_add_task():
    test_sample = converstion.Task(datetime(2018, 11, 15, 22, 50), ' сходить к врачу')
    test_add_task("1", test_sample, [test_sample])


def run_tests_get_all_tasks():
    test_sample = converstion.Task(datetime(2018, 11, 15, 22, 50), ' сходить к врачу')
    test_get_all_tasks("1", [test_sample])


def run_tests():
    run_tests_get_date()
    run_tests_get_task()
    run_tests_create_task()
    run_tests_add_task()
    run_tests_get_all_tasks()


if __name__ == '__main__':
    run_tests()
