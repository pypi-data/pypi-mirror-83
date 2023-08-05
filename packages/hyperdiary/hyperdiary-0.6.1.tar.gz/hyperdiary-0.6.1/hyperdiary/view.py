from datetime import date
from .diary import Diary


def view(diary: Diary, dt: date) -> None:
    entry = {entry.dt: entry for entry in diary.entries}[dt]
    print(dt)
    for line in entry.lines:
        print('- ' + str(line))
