from typing import List
from datetime import date

MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November',
             'December']

DAYS_SHORT_EN = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


class Localization:
    def __init__(self,
                 months: List[str] = MONTHS_EN,
                 days_short: List[str] = DAYS_SHORT_EN,
                 date_fmt: str = '%Y-%m-%d') \
            -> None:
        assert len(months) == 12
        self.months = months
        assert len(days_short) == 7
        self.days_short = days_short
        self.date_fmt = date_fmt

    def get_month(self, i: int) -> str:
        '''Get the localized name of month i (zero-based index).
           >>> l = Localization()
           >>> l.get_month(0)
           'January'
           >>> l.get_month(11)
           'December'
           >>> l.get_month(12)
           Traceback (most recent call last):
           ...
           AssertionError
           >>> Localization(months=['Just January'])
           Traceback (most recent call last):
           ...
           AssertionError
           >>> l2 = Localization(months=list('123456789ond'))
           >>> l2.get_month(3)
           '4'
           >>> l2.get_month(10)
           'n'
        '''
        assert i >= 0
        assert i < 12
        return self.months[i]

    def get_day_short(self, i: int) -> str:
        '''Get the localized name of day i (zero-based index starting Monday).
           >>> l = Localization()
           >>> l.get_day_short(0)
           'Mon'
           >>> l.get_day_short(6)
           'Sun'
           >>> l.get_day_short(7)
           Traceback (most recent call last):
           ...
           AssertionError
           >>> Localization(days_short=['Just Mon'])
           Traceback (most recent call last):
           ...
           AssertionError
           >>> l2 = Localization(days_short=list('1234567'))
           >>> l2.get_day_short(3)
           '4'
           >>> l2.get_day_short(6)
           '7'
        '''
        assert i >= 0
        assert i < 7
        return self.days_short[i]

    def format_date(self, dt: date) -> str:
        '''Format to localized string.
           >>> l = Localization()
           >>> l.format_date(date(2019, 11, 3))
           '2019-11-03'
           >>> l = Localization(date_fmt='%d.%m.%Y')
           >>> l.format_date(date(2019, 11, 3))
           '03.11.2019'
        '''
        return dt.strftime(self.date_fmt)
