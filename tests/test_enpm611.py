

import unittest
from mage_web_scraper import MageWebScraper
from model import Course, Instructor

class TestEnpm611(unittest.TestCase):
    
    def setUp(self):
        self.scraper = MageWebScraper()

    def test_enpm611(self):
        """
        Runs through an end-to-end scenario that searches for a
        course on the Schedule of Classes page and then verifies
        that the instructor for each section exist on the MAGE faculty page.
        """
        
        pass
            

if __name__ == "__main__":
    unittest.main()


