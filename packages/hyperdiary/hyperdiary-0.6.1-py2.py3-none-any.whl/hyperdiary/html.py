import os
from datetime import timedelta, date
from collections import defaultdict
from typing import Iterable, Dict, Union, Callable, Optional  # noqa: F401
from . import diary
from .localization import Localization
from .simplepath import AbsolutePath, RelativePath
from .htmltags import article, header, head, h1, h4, ul, li, a, span, div, \
    footer, meta, link, style, html, body, title, HTMLElement, HTMLContent


def wrap_page(body_content: HTMLContent, page_title: str = None,
              encoding: str = 'utf-8', css_references: Iterable[str] = [],
              inline_css: str = None) -> html:
    h = head(
            meta(charset=encoding),
            meta(name='viewport',
                 content='width=device-width, initial-scale=1')
        )
    if page_title:
        h.append(title(page_title))
    for css in css_references:
        h.append(link(href=css, rel="stylesheet"))
    if inline_css:
        h.append(style(inline_css))
    return html(h, body(body_content))


def day_to_html(current: date, entry: Iterable[str],
                localization: Localization,
                link_to_id_fn: Callable[[Optional[str]], str] = None) \
        -> HTMLElement:
    day = article(_class='card', _id=str(path_for_date(current)))(
                header(h4(localization.format_date(current)))
            )
    day_list = day.subelement(ul())
    for e in entry:
        if isinstance(e, str):
            eli = li()
            if link_to_id_fn:
                tags_to_print = []
                for token in diary.tokenize(e):
                    if token.type == diary.TokenType.Id:
                        eli.append(a(token.text,
                                     href=link_to_id_fn(token.ref)))
                    elif token.type == diary.TokenType.Text:
                        eli.append(span(token.text))
                    elif token.type == diary.TokenType.Tag:
                        tags_to_print.append(token)
                    else:
                        raise NotImplementedError('Unknown TokenType')
                for tag in tags_to_print:
                    eli.append(' ')
                    eli.append(span(tag.text, _class='tag'))
            else:
                eli.append(e)
            day_list.append(eli)
    return day


def wrap_html_page(content: HTMLContent, title: str = None, level: int = 0) \
        -> html:
    return wrap_page(
        div(content, _class='content'),
        page_title=title,
        css_references=[('../'*level) + 'assets/css/picnic.min.css'],
        inline_css='.content { max-width: 800px; margin: auto; '
                   'font-family: lato, sans-serif;}'
                   '.tag { background-color: #ffeeaa;}'
    )


def diary_to_html(diary_instance: diary.Diary, fname: str) -> None:
    entries = diary_instance.entries

    content = div(h1('Entries'))
    entries_html = content.subelement(div())

    for entry in entries:
        entries_html.append(day_to_html(entry.dt, entry.lines,
                                        diary_instance.localization,
                                        lambda ref: '#'))

    wrap_html_page(content, title='Diary').write(fname)


def diary_to_html_folder(diary_instance: diary.Diary, folder: str) -> None:
    root_path = AbsolutePath('/')
    entries_path = AbsolutePath('/entries')
    ids_path = AbsolutePath('/ids')

    loc = diary_instance.localization

    def folder_from_path(p: AbsolutePath) -> str:
        return os.path.join(folder, str(p - root_path))

    entries_ul = ul()

    identifiers = defaultdict(list)  # type: Dict[diary.Token, list]

    for year, year_group in diary_instance.iter_entries_by_year_and_month():
        year_path = entries_path + rel_path(year)
        year_ul = ul()

        for month, month_entries in year_group:
            s_month = '{:02d}'.format(month)
            month_path = year_path + rel_path(s_month)
            month_html = div(h1('{} {}'.format(loc.get_month(month-1), year)))
            month_ul = month_html.subelement(ul())

            for entry in month_entries:
                current = entry.dt
                s_day = '{:02d}'.format(current.day)
                day_path = month_path + rel_path(s_day)
                day_folder = folder_from_path(day_path)
                os.makedirs(day_folder, exist_ok=True)

                def link_to_id_fn(sid: Optional[str]) -> str:
                    assert sid is not None, \
                        'Got invalid identifier {}'.format(sid)
                    return str(ids_path + rel_path(sid) - day_path)

                day_html = day_to_html(current, entry.lines,
                                       diary_instance.localization,
                                       link_to_id_fn)

                foot = div(_class='flex four')
                day_html.append(footer(foot))
                yesterday = current - timedelta(days=1)
                foot.append(div(a('Yesterday ({})'.format(yesterday),
                                href=str(path_for_date(yesterday) - day_path)))
                            )

                tomorrow = current + timedelta(days=1)
                foot.append(div(a('Tomorrow ({})'.format(tomorrow),
                                  href=str(path_for_date(tomorrow) -
                                           day_path)),
                                _class='off-fourth'))

                index_path = os.path.join(day_folder, 'index.html')
                wrap_html_page(day_html, level=4).write(index_path)
                append_li_a(month_ul, str(current), str(day_path - month_path))

                for dt, e in entry.iter_lines():
                    for identifier in diary.find_ids(e):
                        identifiers[identifier].append(dt)

            index_path = os.path.join(folder_from_path(month_path),
                                      'index.html')
            wrap_html_page(month_html, level=3).write(index_path)
            append_li_a(year_ul, loc.get_month(month-1), s_month)

        index_path = os.path.join(folder_from_path(year_path), 'index.html')
        wrap_html_page(year_ul, level=2).write(index_path)
        append_li_a(entries_ul, str(year), str(year))

    index_path = os.path.join(folder_from_path(entries_path), 'index.html')
    wrap_html_page(entries_ul, level=1).write(index_path)

    ids_ul = ul()
    for identifier, days in sorted(identifiers.items()):
        assert identifier.ref is not None, \
            '{} has broken ref'.format(identifier)
        id_path = ids_path + rel_path(identifier.ref)
        id_folder = folder_from_path(id_path)
        os.makedirs(id_folder, exist_ok=True)
        append_li_a(ids_ul, identifier.text, str(id_path - ids_path))
        identifier_ul = ul()
        for day in days:
            append_li_a(identifier_ul, str(day), str(path_for_date(day) -
                                                     id_path))
        index_path = os.path.join(id_folder, 'index.html')
        wrap_html_page(identifier_ul, level=2).write(index_path)
    index_path = os.path.join(folder_from_path(ids_path), 'index.html')
    wrap_html_page(ids_ul, level=1).write(index_path)
    import shutil
    shutil.rmtree(os.path.join(folder, 'assets'), ignore_errors=True)
    shutil.copytree(os.path.join(os.path.dirname(__file__), 'assets'),
                    os.path.join(folder, 'assets'))


def rel_path(spath: Union[date, str, int]) -> RelativePath:
    return RelativePath(str(spath))


def path_for_date(dt: date) -> AbsolutePath:
    return AbsolutePath('/entries/{}/{:02d}/{:02d}'.format(dt.year,
                                                           dt.month,
                                                           dt.day))


def append_li_a(ul: HTMLElement, text: str, href: str) -> None:
    ul.append(li(a(text, href=href)))
