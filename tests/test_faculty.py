

import unittest
from mage_web_scraper import MageWebScraper
from model import Course, Instructor

class TestFaculty(unittest.TestCase):
    
    def setUp(self):
        self.scraper = MageWebScraper()
            
    def test_ackermannn(self):
        """
        Test that the faculty Christopher Ackermann
        can be found and parsed on the MAGE faculty page.
        """
        
        faculty_name:str = 'Christopher Ackermann'
            
        faculty_src:str = self.scraper.search_instructors(faculty_name)
        self.assertIsNotNone(faculty_src,'Could not load faculty search results page')
        url:str = self.scraper.get_instructor_link_from_search_result_page(faculty_src)
        self.assertIsNotNone(url,'Could not get URL to faculty details')
        instructor:Instructor = self.scraper.parse_instructor_page(url)
        self.assertIsNotNone(instructor, "Could not parse faculty details")
            
            
        
    


if __name__ == "__main__":
    unittest.main()


