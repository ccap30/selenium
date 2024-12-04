

import unittest
from mage_web_scraper import MageWebScraper
from model import Course, Instructor

class TestScheduleOfClasses(unittest.TestCase):
    
    def setUp(self):
        self.scraper = MageWebScraper()
    
    def get_course_and_assert(self, course_id, year, term):
        soc_src:str = self.scraper.get_schedule_of_classes_page(course_id, term, year)
        self.assertIsNotNone(soc_src, 'Schedule of Classes page could not be loaded')
        course:Course = self.scraper.get_course_info_from_schedule_of_classes_page(soc_src, course_id)
        self.assertIsNotNone(course, 'Could not parse course info')
        return course
    
    def get_faculty_and_assert(self, instructor):
        faculty_src:str = self.scraper.search_instructors(instructor)
        self.assertIsNotNone(faculty_src, 'Could not load faculty search results page')
        url:str = self.scraper.get_instructor_link_from_search_result_page(faculty_src)
        self.assertIsNotNone(url, 'Could not get URL to faculty details')
        instructor:Instructor = self.scraper.parse_instructor_page(url)
        self.assertIsNotNone(instructor, 'Could not parse faculty details')

    def test_enpm611_fall_2024(self):
        """
        Checks whether the course ENPM611 can
        be found on the Schedule of Classes web page
        for the Fall 2024 semester.
        """

        _ = self.get_course_and_assert('ENPM611', 'Fall', 2024)
    
    def test_enpm670_spring_2025_two_sections(self):
        """
        Checks whether the course ENPM670 can
        be found on the Schedule of Classes web page
        for the Spring 2025 semester and has two sections.
        """

        course = self.get_course_and_assert('ENPM670', 'Spring', 2025)

        self.assertEqual(len(course.sections), 2)

    def test_enpm664_spring_2025_has_location(self):
        """
        Checks whether the course ENPM664 can
        be found on the Schedule of Classes web page
        for the Spring 2025 semester and has a location (or is online).
        """

        course = self.get_course_and_assert('ENPM664', 'Spring', 2025)

        self.assertIsNotNone(course.sections)
        self.assertNotEqual(len(course.sections), 0)
        for section in course.sections:
            self.assertNotIn(section.room, ["TBA", "TBD"])

    def test_enpm611_spring_2025_fewer_than_10_seats(self):
        """
        Checks whether the course ENPM611 can
        be found on the Schedule of Classes web page
        for the Spring 2025 semester and has a fewer than 10 seats.
        """

        course = self.get_course_and_assert('ENPM611', 'Spring', 2025)

        self.assertIsNotNone(course.sections)
        self.assertNotEqual(len(course.sections), 0)
        total_seats:int = 0
        for section in course.sections:
            self.assertIsNotNone(section.open_count)
            total_seats += section.open_count
        
        self.assertLess(total_seats, 10)


    def test_enpm611_fall_2024_professors_match(self):
        """
        Checks whether the course ENPM611 can
        be found on the Schedule of Classes web page
        for the Spring 2025 semester and has a fewer than 10 seats.
        """

        course = self.get_course_and_assert('ENPM611', 'Fall', 2024)

        self.assertIsNotNone(course.sections)
        self.assertNotEqual(len(course.sections), 0)
        seen:set = set()
        for section in course.sections:
            instructor:Instructor = section.instructor
            self.assertIsNotNone(instructor)
            if instructor not in seen:
                seen.add(instructor)
                _ = self.get_faculty_and_assert(instructor)
    
    def test_enpm612_spring_2025_has_description(self):
        """
        Checks whether the course ENPM612 can
        be found on the Schedule of Classes web page
        for the Spring 2025 semester and has a course description.
        """
        course = self.get_course_and_assert('ENPM611', 'Fall', 2024)
        self.assertIsNotNone(course.description)


if __name__ == "__main__":
    unittest.main()


