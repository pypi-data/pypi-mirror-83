import os
import io
from datetime import date
from . import diary


def nice_date(dt: date) -> str:
    return dt.strftime("%d.%m.%Y")


def diary_to_hugo(diary_instance: diary.Diary, folder: diary.Pathlike) -> None:
    content_dir = os.path.join(str(folder), 'content')
    os.makedirs(content_dir, exist_ok=True)

    for entry in diary_instance.entries:
        current = entry.dt
        month_dir = os.path.join(content_dir, 'post',
                                 '{:04d}'.format(current.year),
                                 '{:02d}'.format(current.month))
        os.makedirs(month_dir, exist_ok=True)
        with open(os.path.join(month_dir,
                               '{:02d}.md'.format(current.day)), 'w') as f:
            tags = []
            day_text = io.StringIO()
            for line in entry.lines:
                day_text.write('- ')
                for token in diary.tokenize(line):
                    if token.type == diary.TokenType.Id:
                        day_text.write('[{}](#{})'.format(token.text,
                                                          token.ref))
                    elif token.type == diary.TokenType.Text:
                        day_text.write(token.text)
                    elif token.type == diary.TokenType.Tag:
                        tags.append(token.text)
                    else:
                        raise NotImplementedError('Unknown TokenType')
                day_text.write('\n')
            f.write('+++\n')
            f.write('title = "{0}"\n'.format(nice_date(current)))
            f.write('date = "{0}"\n'.format(current.isoformat()))
            f.write('categories = ["day"]\n')
            f.write('draft = false\n')
            f.write('tags = {}\n'.format(tags))
            f.write('\n+++\n\n')
            day_text.seek(0)
            f.write(day_text.read())
            f.write('\n')
