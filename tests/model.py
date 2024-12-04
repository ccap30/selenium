"""
Data model for handling business objects.
"""


from typing import List

class Section:
    id:str = None
    room:str = None
    instructor:str = None
    total_count:int = 0
    open_count:int = 0
    waitlist_count:int = 0

    def clear(self):
        self.id = None
        self.room = None
        self.instructor = None
        self.total_count = 0
        self.open_count = 0
        self.waitlist_count = 0
    
class Course:
    id:str = None
    description:str = None
    sections:List[Section] = []

    def clear(self):
        self.id = None
        self.description = None
        self.sections.clear()
    
class Instructor:
    name:str = None
    title:str = None
    department:str = None
    email:str = None
    bio:str = None

    def clear(self):
        self.name = None
        self.title = None
        self.department = None
        self.email = None
        self.bio = None