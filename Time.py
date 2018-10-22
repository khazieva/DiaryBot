import re
from datetime import datetime, timedelta, date, time


class Time():
    def __init__(self, input_string):
        self.input_string = input_string
        self.reg_date = re.compile(r'\d{4}/\d{1,2}/\d{1,2} \d{2}:\d{2}')
        self.reg_word = re.compile(r'[а-я ]* в \d{2}:\d{2}')
        self.days_and_shift = {
            'сегодня': timedelta(days=0),
            'завтра': timedelta(days=1),
            'послезавтра': timedelta(days=2),
            'через неделю': timedelta(days=7)
        }

    def parse_raw_date(self):
        try:
            result = datetime.strptime(self.input_string, "%Y/%m/%d %H:%M")
        except ValueError:
            return None
        return result

    def input_word_and_time(self, word, time):
        time_to_add = datetime.strptime(time, "%H:%M").time()
        if word not in self.days_and_shift:
            return None
        date_to_add = date.today() + self.days_and_shift[word]
        return datetime.combine(date_to_add, time_to_add)

    def input_word(self, word):
        today_date = datetime.today().date()
        if word not in self.days_and_shift:
            return None
        result = today_date + self.days_and_shift[word]
        return result

    def parse_string(self):
        if ':' in self.input_string:
            input_list = self.input_string.split(' в ')
            word = input_list[0]
            time = input_list[1]
            result = self.input_word_and_time(word, time)
        else:
            word = self.input_string
            result = self.input_word(word)
        return result

    def parse(self):
        if self.reg_date.match(self.input_string):
            result = self.parse_raw_date()
        elif self.reg_word.match(self.input_string) \
                or self.input_string in self.days_and_shift:
            result = self.parse_string()
        else:
            result = None
        return result


def test_parse_raw_date(name, input_string, result):
    a = Time(input_string)
    got = a.parse_raw_date()
    to_show = "passed" if got == result else "failed"
    print("Test parse_raw_date {} {}, got {}, expected {}.".format(name, to_show, got, result))


def test_parse_string(name, input_string, result):
    a = Time(input_string)
    got = a.parse_string()
    to_show = "passed" if got == result else "failed"
    print("Test parse_string {} {}, got {}, expected {}.".format(name, to_show, got, result))


def test_parse(name, input_string, result):
    a = Time(input_string)
    got = a.parse()
    to_show = "passed" if got == result else "failed"
    print("Test parse {} {}, got {}, expected {}.".format(name, to_show, got, result))


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
    test_parse("3", '2018/11/15 22:50', datetime(2018, 11, 15, 22, 50))
    test_parse("4", 'завтра в 15:00', datetime.combine(date.today() + timedelta(days=1), time(15, 00)))
    test_parse("5", 'сегодня', datetime.today().date())


def run_tests():
    run_tests_parse_raw_date()
    run_tests_parse_string()
    run_tests_parse()


if __name__ == '__main__':
    run_tests()