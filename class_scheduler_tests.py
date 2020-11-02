from unittest import TestCase
from sat_solver import ClassScheduler

class ClassSchedulerTests(TestCase):
    def __init__(self) -> None:
        self.test_all()

    def test_all(self):
        self.test_five_class_constraint(ClassScheduler())
        print('Passed all Tests')

    def test_five_class_constraint(self, c: ClassScheduler):
        c.go()
        c.add_class_constraint('CS 2500')
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1')
        c.add_class_constraint('CS 1800')
        c.solve()
        self.assertTrue(c.do_solver() == 'Satisfiable!\nCS 2500 at 7:00, section_id: 1\nCS 1800 at 9:00, section_id: 7')
