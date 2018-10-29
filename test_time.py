from Time import Time
from datetime import datetime, timedelta, date, time


def test_parse_raw_date(name, input_string, result):
    a = Time()
    got = a.parse_raw_date(input_string)
    to_show = "passed" if got == result else "failed"
    print("Test parse_raw_date {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_parse_string(name, input_string, result):
    a = Time()
    got = a.parse_string(input_string)
    to_show = "passed" if got == result else "failed"
    print("Test parse_string {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def test_parse(name, input_string, result):
    a = Time()
    got = a.parse(input_string)
    to_show = "passed" if got == result else "failed"
    print("Test parse {} {}, got '{}', expected '{}'.".format(name, to_show, got, result))


def run_tests_parse_raw_date():
    test_parse_raw_date("1", '', None)
    test_parse_raw_date("2", 'dxfcgvjhbkjnlk', None)
    test_parse_raw_date("3", 'dfgj/gh/rt fg:gj', None)
    test_parse_raw_date("4", '34567890', None)
    test_parse_raw_date("5", '2018/11/15 22:50', datetime(2018, 11, 15, 22, 50))
    test_parse_raw_date("6", '2017/12/13 22:64', None)
    test_parse_raw_date("7", '2017/12/13 26:04', None)
    test_parse_raw_date("8", '2017/12/76 22:34', None)


def run_tests_parse_string():
    test_parse_string("1", '', None)
    test_parse_string("2", 'zxdgfchgvjhbkjn', None)
    test_parse_string("3", 'сегодня', datetime.today().date())
    test_parse_string("4", 'завтра', datetime.today().date() + timedelta(days=1))
    test_parse_string("5", 'послезавтра', datetime.today().date() + timedelta(days=2))
    test_parse_string("6", 'через неделю', datetime.today().date() + timedelta(days=7))
    test_parse_string("7", 'сегодня в 18:00', datetime.combine(date.today(), time(18, 00)))
    test_parse_string("8", 'завтра в 15:00', datetime.combine(date.today() + timedelta(days=1), time(15, 00)))
    test_parse_string("9", 'послезавтра в 17:15',
                      datetime.combine(date.today() + timedelta(days=2), time(17, 15)))
    test_parse_string("10", 'через неделю в 20:20',
                      datetime.combine(date.today() + timedelta(days=7), time(20, 20)))


def run_tests_parse():
    test_parse("1", '', None)
    test_parse("2", 'zxdgfchgvjhbkjn', None)
    test_parse("3", '2018/11/15 22:50 ', (datetime(2018, 11, 15, 22, 50), ''))
    test_parse("4", 'завтра в 15:00 ', (datetime.combine(date.today() + timedelta(days=1), time(15, 00)), ''))
    test_parse("5", 'сегодня ', (datetime.today().date(), ''))
    test_parse("6", 'сегодня в 15:00 сходить к врачу',
               (datetime.combine(date.today(), time(15, 00)), 'сходить к врачу'))


def run_tests():
    run_tests_parse_raw_date()
    run_tests_parse_string()
    run_tests_parse()


if __name__ == '__main__':
    run_tests()
