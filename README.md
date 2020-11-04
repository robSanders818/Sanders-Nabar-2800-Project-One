# Midterm Project: Class Scheduler Satisfiability Problem
## Ohm Nabar and Robert Sanders
### Installation Instructions:

To install the sat solver library, you must use a unix based system with python3 and pip3 installed. Then run the command
"pip3 install python-sat".  This should enable the sat solver library to
work correctly.  For more help see 
> https://pysathq.github.io/installation.html
  
<br>To install testing library, in directory, use 
> "python3 -m pip install pytest"

### Execution Instructions:

run python3, then import the ClassScheduler with, create an instance of the class_scheduler, then run go() on
the instance as follows:
> "from sat_solver import ClassScheduler; c = ClassScheduler(); c.go()"

Then call any of the following functions to add constraints:
- add_section_constraint(section_id: int)
- add_class_constraint(class_name: str)
- add_subject_constraint(subject: str)
- add_nupath_constraint(nupath: str)
- add_time_constraint(start: int = -1, end: int = 24)

### Project Structure:
- Project Report: [Project_Report.pdf](Project_Report.pdf)

- Sat Solver executable: [sat_solver.py](sat_solver.py)

- ClassDiagram: [ClassDiagram.pdf](ClassDiagram.pdf)

- ClassData Class: [class_data.py](class_data.py)

- Section Class: [section.py](section.py)

- Testing Harness: [class_scheduler_tests.py](class_scheduler_tests.py)

- Class Data: [classes.csv](classes.csv)

- Section Data: [sections.csv](sections.csv)
