from typing import List
from pysat.solvers import Glucose3

from class_data import ClassData
from section import Section

class ClassScheduler:
    """
    A ClassScheduler is an object in which a user can specify constraints on the class sections they would like to take.
    It can determine if there is an assignment of class sections that satisfies these constraints, and if there is, it can provide one such assignment.
    """
    def __init__(self) -> None:
        """
        Initializes a ClassScheduler object.
        """
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
        print("Use help() for help operating the scheduler")

    def solve(self) -> None:
        """
        Helper Function for do_solver()
        Useful for tests
        """
        print(self.do_solver())

    def do_solver(self) -> str:
        """
        Determines whether or not there is a satisfiable assignment of sections given the current constraints.
        If there is, it will be printed out.
        """

        if not self.going:
            return "Scheduler not running! Start scheduler with go()"
        solve_string = ""

        if self.solver.solve():
            solve_string += "Satisfiable!"
            for section_id in self.solver.get_model():
                if section_id in self.section_ref.keys():
                    section_temp = self.section_ref[section_id]
                    solve_string += "\n" + section_temp.class_name + " at " + str(section_temp.time) + ":00, section_id: " + str(section_id)
        else:
            solve_string += "Unsatisfiable :("
        return solve_string
    
    def go(self) -> None:
        """
        Starts the ClassScheduler and adds constraints on the number of sections, sections in the same class, and sections occuring at the same time.
        """

        if self.going:
            print("Already running!")
            return
        self.going = True
        self.__add_four_section_constraint()
        self.__add_same_class_constraint()
        self.__add_same_time_constraint()

    def __add_four_section_constraint(self) -> None:
        """
        Limits total sections to 4.
        """

        self.__add_cardinality_constraint(list(self.section_ref.keys()), 4) #hard encoding a maximum of 4 classes
    
    def __add_same_class_constraint(self) -> None:
        """
        Prevents students from taking multiple sections of the same class.
        """

        for c in list(self.class_ref.keys()):
            sections = []
            for s in list(self.section_ref.values()):
                if c == s.class_name:
                    sections.append(s.section_id)
            self.__add_cardinality_constraint(sections, 1)
    
    def __add_same_time_constraint(self) -> None:
        """
        Prevents students from taking multiple sections at the same time.
        """

        for time in range(0, 23):
            sections = []
            for s in list(self.section_ref.values()):
                if s.time == time:
                    sections.append(s.section_id)
            self.__add_cardinality_constraint(sections, 1)
                    


    def __add_cardinality_constraint(self, variables: List[int], card: int) -> None:
        """
        Adds constraints that limit the number of true variables in "variables" to "card" using sequential counter encoding.
        """

        if not variables or card < 1:
            return

        var_offset = self.var_count
        # we need len(variables) * card new variables such that each new variable s(i, j) represents
        # if the count of the first i true variables >= j
        self.var_count += (len(variables) * card)
        aux_var = lambda i, j : var_offset + (i * card) + j
        
        # CNF representation of var(1)-> s(1, 1)
        # If var(1) is true, the count has reached 1 by var(1)
        self.solver.add_clause([-variables[0], aux_var(0, 1)])
        for j in range(2, card + 1):
            # ~s(1, j) for j=[2, card]
            # The count cannot be higher than 1 yet
            self.solver.add_clause([-aux_var(0, j)])

        for i in range(1, len(variables)):
            # CNF representation of (var(i) v s(i-1, 1)) -> s(i, 1)
            # If var(i) is true or s(i-1, 1) is true, the count must have reached 1
            self.solver.add_clause([ -variables[i], aux_var(i, 1) ])
            self.solver.add_clause([ -aux_var(i - 1, 1), aux_var(i, 1) ])
            # CNF representaion of s(i-1, card) -> ~var(i)
            # If the count has reached card at var(i-1), var(i) cannot be true 
            self.solver.add_clause([ -aux_var(i - 1, card), -variables[i] ])
            for j in range(2, card + 1):
                # CNF representation of ((var(i) ^ s(i-1, j-1)) v s(i-1, j)) -> s(i, j) for j=[2, card]
                # If the count at var(i-1) has reached j or the count at var(i-1) has reached j-1 and var(i) is true,
                # then the count at var(i) must have reached j
                self.solver.add_clause([ aux_var(i, j), -variables[i], -aux_var(i - 1, j - 1)])
                self.solver.add_clause([ aux_var(i, j), -aux_var(i - 1, j) ])

    def add_section_constraint(self, section_id :int) -> None:
        """
        Adds a requirement for a particular section to be taken, identified by its section_id.
        """

        if not self.going:
            print("Scheduler not running! Start scheduler with go()")
            return

        if section_id not in self.section_ref.keys():
            print("Invalid section")
            return
        self.solver.add_clause([ section_id ])
    
    def add_class_constraint(self, class_name :str) -> None:
        """
        Adds a requirement for a particular class to be taken, identified by its class_name (ex. "CS 2800").
        """

        if not self.going:
            print("Scheduler not running! Start scheduler with go()")
            return
		
        if class_name not in self.class_ref.keys():
            print("Invalid class")
            return

        sections = []
        for s in list(self.section_ref.values()):
            if s.class_name == class_name:
                sections.append(s.section_id)
        self.solver.add_clause(sections)

    def add_subject_constraint(self, subject :str) -> None:
        """
        Adds a requirement for a particular subject to be taken.
        """

        if not self.going:
            print("Scheduler not running! Start scheduler with go()")
            return

        if subject not in [c.split(' ')[0] for c in self.class_ref.keys()]:
            print("Invalid subject")
            return

        sections = []
        for s in list(self.section_ref.values()):
            section_class = self.class_ref[s.class_name]
            if section_class.subject == subject:
                sections.append(s.section_id)
        self.solver.add_clause(sections)

    def add_nupath_constraint(self, nupath :str) -> None:
        """
        Adds a requirement for a particular NUPath requirement to be fulfilled.
        """

        if not self.going:
            print("Scheduler not running! Start scheduler with go()")
            return

        if nupath not in {"1", "2", "3", "4", "5"}: #hardcoded for now
            print("Invalid NUPath")
            return

        sections = []
        for s in list(self.section_ref.values()):
            section_class = self.class_ref[s.class_name]
            if section_class.nupath == nupath:
                sections.append(s.section_id)
        self.solver.add_clause(sections)

    def add_time_constraint(self, start :int =-1, end :int =24) -> None:
        """
        Adds a requirement for all classes to be within a given time range (inclusive on both ends)..
        The user may choose to exclude the start or the end of the range.
        """

        if not self.going:
            print("Scheduler not running! Start scheduler with go()")
            return

        if start < -1 or end > 24:
            print("Invalid time range")
            return

        sections = []
        for s in list(self.section_ref.values()):
            if not (start <= s.time <= end):
                self.solver.add_clause([ -s.section_id ])

    def help(self):
        """
        Provides a list of usable commands.
        """

        help_string = """go()- Starts the scheduler\nsolve()- Produces a satisfiable assignment of sections, if there is one\nadd_section_constraint(section_id :int)- Adds a requirement for a paricular section to be taken identified by its section_id\nadd_class_constraint(section_id :int)- Adds a requirement for a particular class to be taken (should be in format "CS 2800")\nadd_nupath_constraint(nupath :str)- Adds a requirement for a particular NUPath requirement (integer) to be fulfilled\nadd_time_constraint(start :int, end :int)- Adds a requirement for all classes to be withing a given time range. Either parameter may be excluded\nhelp()- Provides a list of usable commands"""
        print(help_string)
