from .diary import Diary


def check(diary: Diary) -> None:
    dates_found = set()
    dates_available = {entry.dt for entry in diary.entries}
    for dtrange in diary.expected:
        for dt in dtrange:
            if dt not in dates_available:
                raise Exception('Missing entry {}'.format(dt))
            dates_found.add(dt)

    print('OK found {} days'.format(len(dates_found)))
