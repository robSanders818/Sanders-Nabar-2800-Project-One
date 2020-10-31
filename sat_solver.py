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
        self.going = False

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
    
    def go(self):
        if self.going:
            print("Already running!")
            return
        self.going = True
        self.add_four_section_constraint()
        self.add_same_class_constraint()
        self.add_same_time_constraint()

    def add_four_section_constraint(self):
        self.add_cardinality_constraint(list(self.section_ref.keys()), 4) #hard encoding a maximum of 4 classes
    
    def add_same_class_constraint(self):
        for c in list(self.class_ref.keys()):
            sections = []
            for s in list(self.section_ref.values()):
                if c == s.class_name:
                    sections.append(s.section_id)
            self.add_cardinality_constraint(sections, 1)
    
    def add_same_time_constraint(self):
        for time in range(0, 23):
            sections = []
            for s in list(self.section_ref.values()):
                if s.time == time:
                    sections.append(s.section_id)
            self.add_cardinality_constraint(sections, 1)
                    
    def solve(self):
        if not self.going:
            print("Scheduler not running! Start scheduler with go()")
            return

        if self.solver.solve():
            print("Satisfiable!")
            for section_id in self.solver.get_model():
                if section_id in self.section_ref.keys():
                    section_temp = self.section_ref[section_id]
                    print(section_temp.class_name + " at " + str(section_temp.time) + ":00, section_id: " + str(section_id))
        else:
            print("Unsatisfiable :(")

    def add_cardinality_constraint(self, variables: List[int], card: int):
        if not variables or card < 1:
            return

        var_offset = self.var_count
        self.var_count += (len(variables) * card)
        aux_var = lambda i, j : var_offset + (i * card) + j
        
        self.solver.add_clause([-variables[0], aux_var(0, 1)])
        for j in range(2, card + 1):
            self.solver.add_clause([-aux_var(0, j)])

        for i in range(1, len(variables)):
            self.solver.add_clause([ -variables[i], aux_var(i, 1) ])
            self.solver.add_clause([ -aux_var(i - 1, 1), aux_var(i, 1) ])
            self.solver.add_clause([ -aux_var(i - 1, card), -variables[i] ])
            for j in range(2, card + 1):
                self.solver.add_clause([ aux_var(i, j), -variables[i], -aux_var(i - 1, j - 1)])
                self.solver.add_clause([ aux_var(i, j), -aux_var(i - 1, j) ])

    def add_section_constraint(self, section_id :int):
        if section_id not in self.section_ref.keys():
            print("Invalid section")
            return
        self.solver.add_clause([ section_id ])
    
    def add_class_constraint(self, class_name :str):
        sections = []
        for s in list(self.section_ref.values()):
            if s.class_name == class_name:
                sections.append(s.section_id)
        self.solver.add_clause(sections)

    def add_subject_constraint(self, subject :str):
        sections = []
        for s in list(self.section_ref.values()):
            section_class = self.section_ref[s.class_name]
            if section_class.subject == subject:
                sections.append(s.section_id)
        self.solver.add_clause(sections)

    def add_nupath_constraint(self, nupath :str):
        sections = []
        for s in list(self.section_ref.values()):
            section_class = self.section_ref[s.class_name]
            if section_class.nupath == nupath:
                sections.append(s.section_id)
        self.solver.add_clause(sections)

    def add_time_constraint(self, start :int =-1, end :int =24):
        sections = []
        for s in list(self.section_ref.values()):
            if not (start <= s.time <= end):
                self.solver.add_clause([ -s.section_id ])

