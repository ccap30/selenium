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
    
class Course:
    id:str = None
    sections:List[Section] = []
    
class Instructor:
    name:str = None
    title:str = None
    department:str = None
    email:str = None
    bio:str = None
    