from collections import OrderedDict
from typing import Dict
from .diary import find_tags, find_ids, Diary


def stats(diary: Diary) -> Dict[str, int]:
    output = OrderedDict()  # type: Dict[str, int]
    output['# Days'] = len(diary.entries)
    output['# Lines'] = sum(len(entry.lines) for entry in diary.entries)
    output['# Taggings'] = sum(len(list(find_tags(l)))
                               for d, l in diary.iter_lines())
    output['# Identifications'] = sum(len(list(find_ids(l)))
                                      for d, l in diary.iter_lines())

    for key, val in output.items():
        print('{:.<20}{:.>5}'.format(key, val))

    return output
