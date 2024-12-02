

import unittest
from mage_web_scraper import MageWebScraper
from model import Course, Instructor

class TestScheduleOfClasses(unittest.TestCase):
    
    def setUp(self):
        self.scraper = MageWebScraper()

    def test_enpm611_fall_2024(self):
        """
        Checks whether the course ENPM611 can
        be found on the Schedule of Classes web page
        for the Fall 2024 semester.
        """
        
        course_id:str = 'ENPM611'
        year:int = 2024
        term:str = 'Fall'
        
        soc_src:str = self.scraper.get_schedule_of_classes_page(course_id,year,term)
        self.assertIsNotNone(soc_src,'Schedule of Classes page could not be loaded')
        course:Course = self.scraper.get_course_info_from_schedule_of_classes_page(soc_src, course_id)
        self.assertIsNotNone(course,'Could not parse course info')
            

if __name__ == "__main__":
    unittest.main()


