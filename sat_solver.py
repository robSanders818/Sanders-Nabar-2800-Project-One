from typing import List
from pysat.solvers import Glucose3

from class_data import ClassData
from section import Section

class ClassScheduler:
    def __init__(self):
        self.var_count = 0
        self.class_ref = {}
        self.section_ref = {}
        self.solver = Glucose3()

        with open('classes.csv', encoding='utf-8-sig') as classes_file:
            classes_list = [line.split(',') for line in classes_file]
            for class_desc in classes_list:
                class_temp = ClassData(class_desc[0], class_desc[1], class_desc[2][:-1])
                self.class_ref[class_temp.subject + " " + class_temp.class_id] = class_temp
        with open('sections.csv', encoding='utf-8-sig') as sections_file:
            sections_list = [line.split(',') for line in sections_file]
            for sections_desc in sections_list:
                section_temp = Section(int(sections_desc[0]), sections_desc[2] + " " + sections_desc[1], int(sections_desc[3][:-1]))
                self.section_ref[section_temp.section_id] = section_temp
                self.var_count += 1
