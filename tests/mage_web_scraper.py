
from typing import List,Set,Dict,Tuple
import os
import urllib.parse
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from model import Course, Section, Instructor

    
class MageWebScraper:
    """
    Uses Selenium to open up a Chrome browser and perform
    the actions necessary to scrape content from the web page.
    """
    
    def __init__(self):
        options = Options()
        # Only run in headless mode if HEADLESS is specified
        if os.environ.get('HEADLESS') is not None:
            options.add_argument('--headless=new')
        self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Firefox(options=options)
        

    def get_schedule_of_classes_page(self,course:str='ENPM611', year:int=2024, term:str='Fall') -> str:
        """
        Navigates to the Schedule of Classes page and fills out
        the form to search for the right semester. It then clicks
        the search button and waits for the search results to appear.
        Returns the source of the search result page.
        """
        
        # Navigate to the Schedule of Classes base page
        self.driver.get("https://app.testudo.umd.edu/soc")
        
        # Fill out the search form and search
        
        # Select year and term from dropdown
        select = Select(self.driver.find_element(By.ID,'term-id-input'))
        try:
            select.select_by_visible_text(f'{term.title()} {year}')
        except Exception as e:
            print(f"Error selecting semester: {e}")
            return None
        # Enter course into search field
        course_field = self.driver.find_element(By.ID,'course-id-input')
        course_field.send_keys(course)
        # Click the search button to search
        self.driver.find_element(By.ID, 'search-button').click()
        
        # Wait for the page to load
        try:
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "courses-container")))
        except Exception as e:
            print(f"ERROR: {e}")
            
        # Return the page's source code
        return self.driver.page_source
        
        
    def get_course_info_from_schedule_of_classes_page(self, page_source:str, course_id:str='ENPM611') -> Course:
        """
        Parses the page source that is passed in and finds the specified
        course. It then parses the course information into a Course object
        and returns it.
        """
        
        # Parse the page with bs4
        soup = BeautifulSoup(page_source, "html.parser")
        # Iterate over all the DIVs for courses
        for res_div in soup.find_all("div", class_="course"):
            div_course_id = res_div.find("div", class_='course-id').text
            # If this is the DIV for the course we are looking for...
            if div_course_id == course_id:
                # ... we are parsing it
                course = Course()
                for section_div in res_div.find_all("div", class_="section"):
                    section = Section()
                    section.id = res_div.find("span", class_='section-id').text.strip()
                    section.instructor = res_div.find("span", class_='section-instructor').text.strip()
                    section.total_count = int(res_div.find("span", class_='total-seats-count').text.strip())
                    section.open_count = int(res_div.find("span", class_='open-seats-count').text.strip())
                    section.waitlist_count = int(res_div.find("span", class_='waitlist-count').text.strip())
                    section.room = res_div.find("span", class_='class-building').text.strip()
                    course.sections.append(section)
                return course
            
        # If we couldn't find the course
        return None


    def search_instructors(self, instructor_name:str) -> str:
        """
        Searches the MAGE faculty directory for the provided
        name. Returns the page source of the search result page.
        """
        
        # Open a web page
        url = "https://mage.umd.edu/clark/facultydir"
        self.driver.get(url)
            
        search_bar = self.driver.find_element(By.NAME,'filter')
        search_bar.send_keys(instructor_name.split(' ')[-1])
        search_bar.send_keys(Keys.ENTER)
        
        try:
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, "news--grid")))
        except Exception as e:
            print(f"ERROR: {e}")
            
        return self.driver.page_source
        
        
    def get_instructor_link_from_search_result_page(self, page_src:str) -> str:
        """
        Returns the link of the first search result of the faculty
        search result page. This might not be accurate if
        there are multiple search results.
        """
        
        soup = BeautifulSoup(page_src, "html.parser")
        for res_div in soup.find_all("div", class_="block-first"):
            link = 'https://mage.umd.edu' + res_div.find("a").attrs.get('href')
            return link
        # If there are no search results
        return None
    
    
    def parse_instructor_page(self, url:str) -> Instructor:
        """
        Takes a link to the details page for an instructor
        and parses it into a Instructor object, which
        is then returned.
        """
            
        self.driver.get(url)
        
        try:
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, "faculty_overview")))
        except Exception as e:
            print(f"ERROR: {e}")
        
        instructor_soup = BeautifulSoup(self.driver.page_source, "html.parser")
        
        # Find web page elements and use it to construct the Instructor object
        instructor = Instructor()
        instructor.title = instructor_soup.find("div", id='faculty_title').text.strip()
        instructor.department = instructor_soup.find("div", id='faculty_department').text.strip()
        instructor.email = instructor_soup.find("div", id='faculty_email').text.strip()
        instructor.bio = instructor_soup.find("div", id='faculty_overview').text.strip()
        return instructor
            
    