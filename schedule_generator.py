# coding=utf-8


import xml.etree.ElementTree as ElTree


def write_html(body):
    fin = open('html/template.html', 'r')
    template = fin.read()
    template = template.replace("{{TABLE}}", str(body))

    fout = open('html/ind.html', 'w')
    fout.write(template)

    fout.close()
    fin.close()


from ScheduleBuilder import ScheduleHtmlTableBulder

bldr = ScheduleHtmlTableBulder()

fpath = "schedule.xml"
xmltree = ElTree.parse(fpath)
for day_elem in xmltree.iter('column'):
    for cell in day_elem.iter('cell'):
        if cell.find("lesson") is None:
            bldr.add_big_cell()
            continue
        all_cell = cell.find("lesson[@week='all']")

        if all_cell is not None:
            bldr.add_big_cell(all_cell.text)
        else:
            up_text = ''
            low_text = ''
            up_cell = cell.find("lesson[@week='upper']")
            low_cell = cell.find("lesson[@week='lower']")

            if up_cell is not None:
                up_text = up_cell.text
            if low_cell is not None:
                low_text = low_cell.text

            bldr.add_little_cells(first_text=up_text, second_text=low_text)

    bldr.new_column()

write_html(bldr.htmltable)
