import conversation
from datetime import datetime, date, time, timedelta


def get_task_today(task_str='сходить к врачу'):
    return conversation.Task(datetime.today().date(), task_str)


def get_task_tomorrow(task_str='сходить к врачу'):
    return conversation.Task(datetime.today().date() + timedelta(days=1), task_str)


def get_task_outdated(task_str='сходить к врачу'):
    return conversation.Task(datetime.today().date() - timedelta(days=1), task_str)


def test_get_date(name, input_datetime, result):
    a = conversation.Task(input_datetime, '')
    got = a.get_date()
    to_show = "passed" if got == result else "failed"
    print("Test get_date {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_get_task(name, input_string, result):
    a = conversation.Task(datetime.today(), input_string)
    got = a.get_task()
    to_show = "passed" if got == result else "failed"
    print("Test get_task {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_is_today(name, input_datetime, result):
    a = conversation.Task(input_datetime, '')
    got = a.is_today()
    to_show = "passed" if got == result else "failed"
    print("Test is_today {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_is_tomorrow(name, input_datetime, result):
    a = conversation.Task(input_datetime, '')
    got = a.is_tomorrow()
    to_show = "passed" if got == result else "failed"
    print("Test is_tomorrow {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_is_outdated(name, input_datetime, result):
    a = conversation.Task(input_datetime, '')
    got = a.is_outdated()
    to_show = "passed" if got == result else "failed"
    print("Test is_outdated {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_create_task(name, input_string, result):
    got = conversation.create_task(input_string)
    to_show = "passed" if got == result else "failed"
    print("Test create_task {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_add_task(name, input_task, result):
    a = conversation.TaskManager()
    a.add_task(input_task)
    got = a.tasks
    to_show = "passed" if got == result else "failed"
    print("Test add_task {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_get_all_tasks(name, input_tasks):
    a = conversation.TaskManager()
    a.tasks = input_tasks
    got = a.get_all_tasks()
    to_show = "passed" if got == input_tasks else "failed"
    print("Test get_all_tasks {} {}, got '{}', expected '{}'.".format(name, to_show, got, input_tasks))


def test_get_tasks_for_today(name, input_tasks, result):
    a = conversation.TaskManager()
    a.tasks = input_tasks
    got = a.get_tasks_for_today()
    to_show = "passed" if got == result else "failed"
    print("Test get_tasks_for_today {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_get_tasks_for_tomorrow(name, input_tasks, result):
    a = conversation.TaskManager()
    a.tasks = input_tasks
    got = a.get_tasks_for_tomorrow()
    to_show = "passed" if got == result else "failed"
    print("Test get_tasks_for_tomorrow {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_remove_outdated_tasks(name, input_tasks, result):
    a = conversation.TaskManager()
    a.tasks = input_tasks
    a.remove_outdated_tasks()
    got = a.get_all_tasks()
    to_show = "passed" if got == result else "failed"
    print("Test remove_outdated_tasks {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def run_tests_get_date():
    test_get_date("1", datetime(2018, 11, 15, 22, 50), datetime(2018, 11, 15, 22, 50))
    test_get_date("2", datetime.today().date(), datetime.today().date())


def run_tests_get_task():
    test_get_task("1", 'сходить к врачу', 'сходить к врачу')
    test_get_task("2", 'тренировка', 'тренировка')


def run_tests_is_today():
    test_is_today("1", datetime(2018, 10, 15, 22, 50), False)
    test_is_today("2", datetime.today().date(), True)
    test_is_today("3", datetime.today().date() + timedelta(days=1), False)


def run_tests_is_tomorrow():
    test_is_tomorrow("1", datetime(2018, 10, 15, 22, 50), False)
    test_is_tomorrow("2", datetime.today().date(), False)
    test_is_tomorrow("3", datetime.today().date() + timedelta(days=1), True)


def run_tests_is_outdated():
    test_is_outdated("1", datetime(2018, 10, 15, 22, 50), True)
    test_is_outdated("2", datetime.today().date(), False)
    test_is_outdated("3", datetime.today().date() + timedelta(days=1), False)


def run_tests_create_task():
    test_create_task("1", '2018/11/15 22:50', None)
    test_create_task("2", '', None)
    test_create_task("3", 'сходить к врачу', None)
    test_create_task("4", '2018/11/15 22:50 сходить к врачу',
                     conversation.Task(datetime(2018, 11, 15, 22, 50), 'сходить к врачу'))
    test_create_task("5", 'сегодня в 15:00 сходить к врачу',
                     conversation.Task(datetime.combine(date.today(), time(15, 00)), 'сходить к врачу'))


def run_tests_add_task():
    test_sample = conversation.Task(datetime(2018, 11, 15, 22, 50), ' сходить к врачу')
    test_add_task("1", test_sample, [test_sample])


def run_tests_get_all_tasks():
    test_sample = conversation.Task(datetime(2018, 11, 15, 22, 50), ' сходить к врачу')
    test_get_all_tasks("1", [test_sample])


def run_tests_get_tasks_for_today():
    test_sample_one = [get_task_today('сходить в магазин'), get_task_today('погулять'), get_task_tomorrow()]
    test_sample_two = [get_task_tomorrow(), get_task_tomorrow(), get_task_tomorrow()]
    test_get_tasks_for_today("1",  test_sample_one, [get_task_today('сходить в магазин'), get_task_today('погулять')])
    test_get_tasks_for_today("2", test_sample_two, [])


def run_tests_get_tasks_for_tommorow():
    test_sample_one = [get_task_today(), get_task_tomorrow('погулять'), get_task_tomorrow('тренировка')]
    test_sample_two = [get_task_today(), get_task_today(), get_task_today()]
    test_get_tasks_for_tomorrow("1", test_sample_one, [get_task_tomorrow('погулять'), get_task_tomorrow('тренировка')])
    test_get_tasks_for_tomorrow("2", test_sample_two, [])


def run_tests_remove_outdated_tasks():
    test_sample_one = [get_task_outdated(), get_task_today('читать'), get_task_outdated(),
                       get_task_tomorrow('тренировка')]
    test_sample_two = [get_task_tomorrow('бег'), get_task_today('приготовить обед')]
    test_remove_outdated_tasks("1", test_sample_one, [get_task_today('читать'), get_task_tomorrow('тренировка')])
    test_remove_outdated_tasks("2", test_sample_two, [get_task_tomorrow('бег'), get_task_today('приготовить обед')])


def run_tests():
    run_tests_get_date()
    run_tests_get_task()
    run_tests_is_today()
    run_tests_is_tomorrow()
    run_tests_is_outdated()
    run_tests_create_task()
    run_tests_add_task()
    run_tests_get_all_tasks()
    run_tests_get_tasks_for_today()
    run_tests_get_tasks_for_tommorow()
    run_tests_remove_outdated_tasks()


if __name__ == '__main__':
    run_tests()
