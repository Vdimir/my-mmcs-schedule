# coding=utf-8


import xml.etree.ElementTree as ElTree
import itertools

# http://www.decalage.info/python/html
import HTML


def write_html(body):
    fin = open('html/template.html', 'r')
    template = fin.read()
    template = template.replace("{{TABLE}}", str(body))

    fout = open('html/ind.html', 'w')
    fout.write(template)

    fout.close()
    fin.close()


def pairwise(iterable):
    """s -> (s0,s1), (s2,s3), (s4, s5), ..."""
    a = iter(iterable)
    return itertools.izip(a, a)


def text_to_tablecell(text=None, big=False):
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


# table_data = [
#         [HTML.TableCell('test colspan', attribs={'rowspan':2}), 'foo ','other cell'],
#
#         ['First name',   'Age'],
#         ['Smith',       'John',         30],
#         ['Carpenter',   'Jack',         47],
#      ]
fisrst_col = [
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
htmltable = HTML.Table(header_row=header_row, attribs={'class': 'table table-bordered'}, style='', border=0)
for c in fisrst_col:
    htmltable.rows.append([
        HTML.TableCell(c.replace('\n', '<br>'), attribs={'rowspan': 2, 'class': 'time'})
    ])
    htmltable.rows.append([])

fpath = "schedule.xml"

tree = ElTree.parse(fpath)
root = tree.getroot()

for elem in tree.iter('column'):
    for table_rows, cell in itertools.izip_longest(pairwise(htmltable.rows), elem.iter('cell')):
        up_row, low_row = table_rows
        if (cell is None) or (cell.find("lesson") is None):
            up_row.append(text_to_tablecell(big=True))
            continue
        all_cell = cell.find("lesson[@week='all']")
        if all_cell is not None:
            up_row.append(text_to_tablecell(all_cell.text, big=True))
        else:
            up_cell = cell.find("lesson[@week='upper']")
            low_cell = cell.find("lesson[@week='lower']")
            if up_cell is not None:
                up_row.append(text_to_tablecell(up_cell.text))
            else:
                up_row.append(text_to_tablecell())

            if low_cell is not None:
                low_row.append(text_to_tablecell(low_cell.text))
            else:
                low_row.append(text_to_tablecell())

write_html(htmltable)
