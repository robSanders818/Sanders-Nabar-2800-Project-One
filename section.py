class Section:
    """ Definition of Section of a class
            section_id: int = Identifier of section
            class_name: str = Class subject + id, used to uniquely identify corresponding Class             
            time: int = starting time of section
     """

    def __init__(self, section_id: int, class_name :str, time :int) -> None:
        self.section_id = section_id
        self.class_name = class_name
        self.time = time
