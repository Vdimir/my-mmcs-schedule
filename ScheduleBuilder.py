# coding=utf-8

# http://www.decalage.info/python/html
import HTML

import xml.etree.ElementTree as ElTree
import itertools

first_col = [
    """8:00
8:45
-
8:50
9:35""",

    """9:50
10:35
-
10:40
11:25""",

    """11:55
12:40
-
12:45
13:30""",

    """13:45
14:30
-
14:35
15:20""",

    """15:50
16:35
-
16:40
17:25"""]
header_row = ['', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']


def pairwise(iterable):
    """s -> (s0,s1), (s2,s3), (s4, s5), ..."""
    a = iter(iterable)
    return itertools.izip(a, a)


def translate_title(text):
    translate_dic = {'HC': 'Гуманитарный курс',
                     'DataBase': 'Базы данных',
                     'Choise': 'Курс по выбору',
                     'CHM': 'Численные методы',
                     'TVIMS': 'Тер Вер',
                     'SC': 'С/К',
                     'SC1': 'С/К',
                     'SC2': 'С/К',
                     'OBJ': 'БЖД'}
    if text not in translate_dic:
        return text
    return translate_dic[text]


class ScheduleHtmlTableBulder:
    def __init__(self):
        self.htmltable = HTML.Table(header_row=header_row,
                                    attribs={'class': 'table table-bordered'},
                                    style='',
                                    border=0)
        self.create_empty_htmltable()
        self.row_iter = self._get_row_iter()

    def _get_row_iter(self):
        # return iter(pairwise(self.htmltable.rows))
        return pairwise(self.htmltable.rows)

    def new_column(self):
        while True:
            try:
                self.add_big_cell()
            except StopIteration:
                break
        self.row_iter = self._get_row_iter()

    def _get_sub_rows(self):
        return self.row_iter.next()

    def add_big_cell(self, text=''):
        up_row, low_row = self._get_sub_rows()
        up_row.append(self.convert_text_to_tablecell(text, big=True))

    def add_little_cells(self, first_text='', second_text=''):
        up_row, low_row = self._get_sub_rows()
        up_row.append(self.convert_text_to_tablecell(first_text))
        low_row.append(self.convert_text_to_tablecell(second_text))

    def create_empty_htmltable(self):
        for c in first_col:
            self.htmltable.rows.append([
                HTML.TableCell(c.replace('\n', '<br>'), attribs={'rowspan': 2, 'class': 'time'})
            ])
            self.htmltable.rows.append([])

    def convert_text_to_tablecell(self, text=None, big=False):
        if text is None:
            text_str = ''
        else:
            text_str = str(text)
        text_str = translate_title(text_str)
        attrs = {}
        if big:
            attrs['rowspan'] = 2
        attrs['class'] = 'text-center col-md-2'
        return HTML.TableCell(text_str, attribs=attrs)

    def get_res(self):
        return self.htmltable
