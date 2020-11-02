from unittest import TestCase
from sat_solver import ClassScheduler


class ClassSchedulerTests(TestCase):
    """
    Class performing tests for various combinations of uses for scheduler
    """
    def __init__(self) -> None:
        self.test_all()

    def test_all(self):
        self.test_five_class_constraint(ClassScheduler())
        self.test_same_time_sections(ClassScheduler())
        self.test_subject_constraints(ClassScheduler())
        self.test_nupath_constraints(ClassScheduler())
        self.test_unsat_time_constraint(ClassScheduler())
        self.test_time_with_class(ClassScheduler())
        self.test_subject_constraint_limited(ClassScheduler())
        self.test_no_time_sat(ClassScheduler())
        print('Passed all Tests')

    def test_five_class_constraint(self, c: ClassScheduler):
        c.go()
        c.add_class_constraint('CS 2500')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1')
        c.add_class_constraint('CS 1800')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1\nCS 1800 at 9:00, section_id: 7')
        c.add_class_constraint('MATH 2331')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1\nCS 1800 at 9:00, section_id: 7\nMATH 2331 at 8:00, section_id: 21')
        c.add_class_constraint('PHIL 1111')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1\nCS 1800 at 9:00, section_id: 7\nMATH 2331 at 8:00, section_id: 21\nPHIL 1111 at 15:00, section_id: 45')
        c.add_class_constraint('ECON 1116')
        self.assertTrue(c.do_solver() == 'Unsatisfiable :(')

    def test_same_time_sections(self, c: ClassScheduler):
        c.go()
        c.add_section_constraint(1)
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1')
        c.add_section_constraint(6)
        self.assertTrue(c.do_solver() == 'Unsatisfiable :(')

    def test_subject_constraints(self, c: ClassScheduler):
        c.go()
        c.add_subject_constraint('CS')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1')
        c.add_subject_constraint('PHIL')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1\nPHIL 1111 at 15:00, section_id: 45')
        c.add_subject_constraint('MATH')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1\nMATH 3400 at 13:00, section_id: 39\nPHIL 2303 at 14:00, section_id: 56')
        c.add_subject_constraint('ECON')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1\nMATH 3400 at 13:00, section_id: 39\nPHIL 2303 at 14:00, section_id: 56\nECON 1000 at 9:00, section_id: 60')
        c.add_subject_constraint('THTR')
        self.assertTrue(c.do_solver() == 'Unsatisfiable :(')

    def test_nupath_constraints(self, c: ClassScheduler):
        c.go()
        c.add_nupath_constraint('1')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1')
        c.add_nupath_constraint('2')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1\nCS 3200 at 9:00, section_id: 18')
        c.add_nupath_constraint('3')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1\nCS 3200 at 9:00, section_id: 18\nTHTR 1000 at 15:00, section_id: 80')
        c.add_nupath_constraint('4')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1\nCS 3200 at 9:00, section_id: 18\nTHTR 1000 at 15:00, section_id: 80\nTHTR 1433 at 10:00, section_id: 81')
        c.add_nupath_constraint('5')
        self.assertTrue(c.do_solver() == 'Unsatisfiable :(')

    def test_unsat_time_constraint(self, c: ClassScheduler):
        c.go()
        c.add_time_constraint(10, 16)
        self.assertTrue(c.do_solver() == 'Satisfiable!')
        c.add_section_constraint(1)
        self.assertTrue(c.do_solver() == 'Unsatisfiable :(')

    def test_time_with_class(self, c: ClassScheduler):
        c.go()
        c.add_time_constraint(10, 16)
        c.add_section_constraint(8)
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 1800 at 11:00, section_id: 8')
        c.add_section_constraint(13)
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 1800 at 11:00, section_id: 8\nCS 2800 at 15:00, section_id: 13')
        c.add_class_constraint('PHIL 1111')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 1800 at 11:00, section_id: 8\nCS 2800 at 15:00, section_id: 13\nPHIL 1111 at 10:00, section_id: 42')
        c.add_class_constraint('ECON 1000')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 1800 at 11:00, section_id: 8\nCS 2800 at 15:00, section_id: 13\nPHIL 1111 at 12:00, section_id: 43\nECON 1000 at 10:00, section_id: 61')

    def test_subject_constraint_limited(self, c: ClassScheduler):
        c.go()
        c.add_time_constraint(10, 16)
        c.add_class_constraint('CS 2500')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 11:00, section_id: 3')
        c.add_class_constraint('CS 1800')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 11:00, section_id: 3\nCS 1800 at 13:00, section_id: 9')
        c.add_class_constraint('CS 2800')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 11:00, section_id: 3\nCS 1800 at 13:00, section_id: 9\nCS 2800 at 12:00, section_id: 12')
        c.add_subject_constraint('PHIL')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 11:00, section_id: 3\nCS 1800 at 13:00, section_id: 9\nCS 2800 at 12:00, section_id: 12\nPHIL 1106 at 14:00, section_id: 59')

    def test_no_time_sat(self, c: ClassScheduler):
        c.go()
        c.add_time_constraint(10, 12)
        c.add_section_constraint(3)
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 11:00, section_id: 3')
        c.add_section_constraint(22)
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 11:00, section_id: 3\nMATH 2331 at 10:00, section_id: 22')
        c.add_section_constraint(31)
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 11:00, section_id: 3\nMATH 2331 at 10:00, section_id: 22\nMATH 4581 at 12:00, section_id: 31')
        c.add_subject_constraint('PHIL')
        self.assertTrue(c.do_solver() == 'Unsatisfiable :(')











