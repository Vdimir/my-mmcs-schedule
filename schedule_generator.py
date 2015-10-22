# coding=utf-8


import xml.etree.ElementTree as ElTree
from ScheduleBuilder import ScheduleHtmlTableBulder


def write_html(body):
    fin = open('template.html', 'r')
    template_str = fin.read()
    template_str = template_str.replace("{{TABLE}}", str(body))

    fout = open('html/index.html', 'w')
    fout.write(template_str)
    fout.close()

    fin.close()


def getCourceNames(courseNamesXml):
    res = {}
    for nameAlias in courseNamesXml.iter('alias'):
        original_name = nameAlias.find('from').text
        replace_name = nameAlias.find('to').text
        res[original_name] = replace_name
    return res


def getLessonTime(lessonTimeXml):
    res = []
    for lessonTime in lessonTimeXml.iter('lesson'):
        start_time = lessonTime.find('start').text
        end_time = lessonTime.find('end').text
        res.append('{0}\n\n-\n\n{1}'.format(start_time, end_time))
    return res


def getMainTable(tableXml, table_builder):
    for day_elem in tableXml.iter('column'):
        # day_of_week = day_elem.attrib['day']
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


def main():
    xmltree = ElTree.parse("schedule.xml")

    course_names = getCourceNames(xmltree.find('courcenames'))
    lesson_times = getLessonTime(xmltree.find('lessontime'))

    table_builder = ScheduleHtmlTableBulder(course_names, lesson_times)

    getMainTable(xmltree.find('table'), table_builder)

    write_html(table_builder.htmltable)
    print('Done!')


if __name__ == '__main__':
    main()
