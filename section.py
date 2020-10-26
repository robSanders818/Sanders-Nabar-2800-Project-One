class Section:
    """ Definition of Section of a class
            section_id: int = Identifier of section
            class_id: int = id of ccorresponding class
            class_subject: string = subject of class
            time: int = starting time of section
     """

    def __init__(self, section_id, class_id, class_subject, time):
        self.section_id = section_id
        self.class_id = class_id
        self.class_subject = class_subject
        self.time = time
