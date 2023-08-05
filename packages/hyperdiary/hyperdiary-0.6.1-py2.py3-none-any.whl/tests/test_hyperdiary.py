#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from hyperdiary import parser, Diary
from hyperdiary.diary import find_ids, find_tags, tokenize, \
    BadEntryException
from hyperdiary.check import check
from hyperdiary.stats import stats
from hyperdiary.html import diary_to_html, diary_to_html_folder
from hyperdiary.tiddlywiki import diary_to_tiddlers, \
    diary_to_tiddlers_export, diary_to_tiddlywiki_export
from hyperdiary.hugo import diary_to_hugo


EXPECTED_TIDDLER_NAMES = {'2019-06-09.tid', '2019-05-01.tid', '2019-06-10.tid'}


def in_test_folder(relative_path):
    return Path(__file__).parent / relative_path


class TestHyperdiary(unittest.TestCase):

    def setUp(self):
        self.diary = Diary.discover(in_test_folder('src'))
        self.diary.load_entries()

    def test_command_line_interface(self):
        self.assertEqual('check', parser.parse_args(['check']).subcommand)

    def test_loading_of_entries(self):
        self.assertGreaterEqual(len(self.diary.entries), 3)

    def test_diary_without_expected(self):
        Diary({})

    def test_localization_loaded(self):
        loc = self.diary.localization
        self.assertEqual('Aug', loc.get_month(7))
        self.assertEqual('Mi', loc.get_day_short(2))
        self.assertEqual('3.11.2019', loc.format_date(date(2019, 11, 3)))

    def test_check(self):
        check(self.diary)

    def test_stats(self):
        self.assertGreater(len(stats(self.diary)), 3)

    def test_iteration_by_month(self):
        entries = self.diary.nested_dicts_by_year_and_month()
        self.assertIn(2019, entries)
        self.assertIn(5, entries[2019])
        self.assertIn(6, entries[2019])
        self.assertIn(date(2019, 6, 9), entries[2019][6])
        self.assertIn(date(2019, 6, 10), entries[2019][6])
        cnt = 0
        for year, year_group in self.diary.iter_entries_by_year_and_month():
            for month, month_entries in year_group:
                for entry in month_entries:
                    cnt += 1
        self.assertGreaterEqual(cnt, 3)
        self.assertEqual(cnt, len(self.diary.entries))

    def test_missing_hyperdiary_json(self):
        self.assertRaises(FileNotFoundError, Diary.discover,
                          subpath=in_test_folder('.'))

    def test_bad_entries(self):
        path = in_test_folder('src/2019/05_bad_entries.yaml')
        diary = Diary(dict(sources=[str(path)]))
        self.assertRaises(BadEntryException, diary.load_entries)

    def test_tokenization(self):
        line = '+tag A $test-line by $Jane_Doe|Jane; expect no content +hallo'
        self.assertEqual(2, len(find_tags(line)))
        self.assertEqual(2, len(find_ids(line)))
        self.assertEqual(7, len(list(tokenize(line))))
        line = '$just_an_id)'
        self.assertEqual(1, len(find_ids(line)))
        self.assertEqual(2, len(list(tokenize(line))))

    def test_html_export(self):
        with TemporaryDirectory() as folder:
            outfname = Path(folder) / 'out.html'
            diary_to_html(self.diary, str(outfname))
            self.assertTrue(outfname.exists())
            with open(str(outfname), 'r') as f:
                self.assertGreater(len(f.read()), 0)

    def test_htmlfolder_export(self):
        with TemporaryDirectory() as folder:
            diary_to_html_folder(self.diary, folder)
            folder = Path(folder)
            self.assertGreater(len(list(folder.iterdir())), 0)

    def test_tiddlers_export(self):
        with TemporaryDirectory() as folder:
            diary_to_tiddlers_export(self.diary, folder)
            folder = Path(folder)
            files = set(f.name for f in folder.iterdir())
            self.assertGreater(len(files), 0)
            for fname in EXPECTED_TIDDLER_NAMES:
                self.assertIn(fname, files)

    def test_tiddywiki_export(self):
        tiddlywiki = 'tiddlywiki_mock.html'
        with TemporaryDirectory() as folder:
            folder = Path(folder)
            tiddlywiki_path = folder / tiddlywiki
            outfname = folder / 'out.html'
            with open(str(tiddlywiki_path), 'w') as f:
                f.write('---\n---\n')  # no "storeArea"
            self.assertRaises(Exception, diary_to_tiddlywiki_export,
                              diary_instance=self.diary, file=str(outfname),
                              tiddlywiki_base_file=str(tiddlywiki_path))
            with open(str(tiddlywiki_path), 'w') as f:
                f.write('---\nid="storeArea"\n---\n')
            diary_to_tiddlywiki_export(self.diary, str(outfname),
                                       str(tiddlywiki_path))
            self.assertGreater(len(list(folder.iterdir())), 1)

    def test_tiddler_serialization(self):
        for tiddler in diary_to_tiddlers(self.diary):
            self.assertGreater(len(tiddler.to_tid()), 0)
            self.assertGreater(len(tiddler.to_div()), 0)

    def test_hugo_export(self):
        with TemporaryDirectory() as folder:
            diary_to_hugo(self.diary, folder)
            folder = Path(folder)
            self.assertGreater(len(list(folder.iterdir())), 0)
