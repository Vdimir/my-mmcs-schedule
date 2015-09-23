# coding=utf-8

# http://www.decalage.info/python/html
import HTML

import xml.etree.ElementTree as ElTree
import itertools
import static_data

first_col = static_data.lesson_times

header_row = [HTML.TableCell('', attribs={'class': ''}),
              HTML.TableCell('Mon', attribs={'class': 'day-of-week day_mon'}),
              HTML.TableCell('Tue', attribs={'class': 'day-of-week day_tue'}),
              HTML.TableCell('Wrd', attribs={'class': 'day-of-week day_wed'}),
              HTML.TableCell('Thu', attribs={'class': 'day-of-week day_thu'}),
              HTML.TableCell('Fri', attribs={'class': 'day-of-week day_fri'}),
              HTML.TableCell('Sat', attribs={'class': 'day-of-week day_sat'})]


def pairwise(iterable):
    """s -> (s0,s1), (s2,s3), (s4, s5), ..."""
    a = iter(iterable)
    return itertools.izip(a, a)


def translate_title(text):
    translate_dic = static_data.course_names
    if text not in translate_dic:
        return text
    return translate_dic[text]


def convert_text_to_tablecell(text='', html_class='', big=False):
    text_str = translate_title(text)
    attrs = {}
    if big:
        attrs['rowspan'] = 2
    attrs['class'] = 'text-center col-md-2' + ' ' + html_class
    return HTML.TableCell(text_str, attribs=attrs)


class ScheduleHtmlTableBulder:
    def __init__(self):
        self.htmltable = HTML.Table(header_row=header_row,
                                    attribs={'class': 'table table-bordered'},
                                    style='',
                                    border=0)
        self._initialize_empty_htmltable()
        self._clear_row_iter()

    def add_cell(self, new_up_row, new_low_row=None):
        current_up_row, current_low_row = self._get_sub_rows()
        if new_low_row is None:
            current_up_row.append(
                convert_text_to_tablecell(new_up_row['text'], html_class=new_up_row['class'], big=True))
        else:
            current_up_row.append(convert_text_to_tablecell(new_up_row['text'], html_class=new_up_row['class']))
            current_low_row.append(convert_text_to_tablecell(new_low_row['text'], html_class=new_low_row['class']))

    def _clear_row_iter(self):
        self.row_iter = pairwise(self.htmltable.rows)

    def _get_sub_rows(self):
        return self.row_iter.next()

    def _append_empty_cell(self):
        current_up_row, _ = self._get_sub_rows()
        current_up_row.append(convert_text_to_tablecell(html_class='all', big=True))

    def _initialize_empty_htmltable(self):
        for c in first_col:
            self.htmltable.rows.append([
                HTML.TableCell(c.replace('\n', '<br>'), attribs={'rowspan': 2, 'class': 'time'})
            ])
            self.htmltable.rows.append([])

    def new_column(self):
        while True:
            try:
                self._append_empty_cell()
            except StopIteration:
                break
        self._clear_row_iter()
