from section import Section


class ClassData:
    """ Definition of a Class
            class_id: str = identifier of the class
            subject: str = subject of the class
            nupath: str = corresponding nupath requirement
    """

    def __init__(self, class_id: str, subject: str, nupath: str) -> None:
        """
        Initializes a ClassData object.
        """
        self.class_id = class_id
        self.subject = subject
        self.nupath = nupath
