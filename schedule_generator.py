# coding=utf-8


import xml.etree.ElementTree as ElTree


def write_html(body):
    fin = open('html/template.html', 'r')
    template = fin.read()
    template = template.replace("{{TABLE}}", str(body))

    fout = open('html/index.html', 'w')
    fout.write(template)

    fout.close()
    fin.close()


from ScheduleBuilder import ScheduleHtmlTableBulder

table_builder = ScheduleHtmlTableBulder()

fpath = "schedule.xml"
xmltree = ElTree.parse(fpath)
for day_elem in xmltree.iter('column'):
    day_of_week = day_elem.attrib['day']
    for cell in day_elem.iter('cell'):
        up_text = {'text': '', 'class': 'upper'}
        low_text = {'text': '', 'class': 'lower'}

        if cell.find("lesson") is None:
            up_text['class'] = '{0} {1}'.format('all', 'empty')
            table_builder.add_cell(up_text)
            continue
        xml_all_cell = cell.find("lesson[@week='all']")

        if xml_all_cell is not None:
            up_text['text'] = xml_all_cell.text
            up_text['class'] = '{0} {1}'.format(xml_all_cell.attrib['week'],
                                                xml_all_cell.attrib['type'])
            table_builder.add_cell(up_text)
        else:
            xml_up_cell = cell.find("lesson[@week='upper']")
            xml_low_cell = cell.find("lesson[@week='lower']")

            if xml_up_cell is not None:
                up_text['text'] = xml_up_cell.text
                up_text['class'] = '{0} {1}'.format('upper',
                                                    xml_up_cell.attrib['type'])
            if xml_low_cell is not None:
                low_text['text'] = xml_low_cell.text
                low_text['class'] = '{0} {1}'.format('lower',
                                                     xml_low_cell.attrib['type'])

            table_builder.add_cell(up_text, low_text)

    table_builder.new_column()

write_html(table_builder.htmltable)
print('Done!')
