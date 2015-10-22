# coding=utf-8

# http://www.decalage.info/python/html
import HTML

import itertools


header_row = [HTML.TableCell('', attribs={'class': 'time-col'}),
              HTML.TableCell('Mon', attribs={'class': 'day-of-week day-mon'}),
              HTML.TableCell('Tue', attribs={'class': 'day-of-week day-tue'}),
              HTML.TableCell('Wed', attribs={'class': 'day-of-week day-wed'}),
              HTML.TableCell('Thu', attribs={'class': 'day-of-week day-thu'}),
              HTML.TableCell('Fri', attribs={'class': 'day-of-week day-fri'}),
              HTML.TableCell('Sat', attribs={'class': 'day-of-week day-sat'})]


def pairwise(iterable):
    """s -> (s0,s1), (s2,s3), (s4, s5), ..."""
    a = iter(iterable)
    return itertools.izip(a, a)


class ScheduleHtmlTableBulder:
    def __init__(self, translate_dic, first_col):
        self.first_col = first_col
        self.translate_dic = translate_dic
        self.htmltable = HTML.Table(header_row=header_row,
                                    # attribs={'class': 'table table-bordered'},
                                    style='',
                                    border=0)
        self._initialize_empty_htmltable()
        self._clear_row_iter()

    def new_column(self):
        while True:
            try:
                self._append_empty_cell()
            except StopIteration:
                break
        self._clear_row_iter()

    def add_cell(self, new_up_row, new_low_row=None):
        current_up_row, current_low_row = self._get_sub_rows()
        if new_low_row is None:
            current_up_row.append(
                self.convert_text_to_tablecell(new_up_row['text'], html_class=new_up_row['class'], big=True))
        else:
            current_up_row.append(self.convert_text_to_tablecell(new_up_row['text'], html_class=new_up_row['class']))
            current_low_row.append(self.convert_text_to_tablecell(new_low_row['text'], html_class=new_low_row['class']))

    def translate_title(self, text):
        if text not in self.translate_dic:
            return text
        return self.translate_dic[text].encode('utf-8')

    def convert_text_to_tablecell(self, text='', html_class='', big=False):
        text_str = self.translate_title(text)
        attrs = {}
        if big:
            attrs['rowspan'] = 2
        attrs['class'] = html_class
        return HTML.TableCell(text_str, attribs=attrs)

    # private

    def _clear_row_iter(self):
        self.row_iter = pairwise(self.htmltable.rows)

    def _get_sub_rows(self):
        return self.row_iter.next()

    def _append_empty_cell(self):
        current_up_row, _ = self._get_sub_rows()
        current_up_row.append(self.convert_text_to_tablecell(html_class='all', big=True))

    def _initialize_empty_htmltable(self):
        for c in self.first_col:
            self.htmltable.rows.append([
                HTML.TableCell(c.replace('\n', '<br>'), attribs={'rowspan': 2, 'class': 'time-col'})
            ])
            self.htmltable.rows.append([])
