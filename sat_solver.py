from typing import List

from class_data import ClassData
from section import Section


def sat_solver():
    classes = {}
    sections = []
    with open('classes.csv', encoding='utf-8-sig') as classes_file:
        classes_list = [line.split(',') for line in classes_file]
        for class_desc in classes_list:
            classes[ClassData(class_desc[0], class_desc[1], class_desc[2][:-1])] = []
    with open('sections.csv', encoding='utf-8-sig') as sections_file:
        sections_list = [line.split(',') for line in sections_file]
        for sections_desc in sections_list:
            sections.append(Section(sections_desc[0], sections_desc[1], sections_desc[2], int(sections_desc[3][:-1])))

    classes = init_class_sections(classes, sections)


def init_class_sections(classes: dict, sections: List[Section]):
    for section in sections:
        for class_desc, class_sections in classes.items():
            if class_desc.section_in_class(section):
                class_sections.append(section)
                break
    return classes


if __name__ == '__main__':
    sat_solver()