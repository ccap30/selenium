# Selenium Testing

[Selenium](https://www.selenium.dev) is a framework for testing web-based user interfaces. It provides capabilities to mimic user interactions in a web browser. The [Selenium Python Library](https://selenium-python.readthedocs.io) can be used to navigate web pages via Python and combine that with unit tests.

This repository uses Selenium to test pages related to Maryland Applied Graduate Engineering (MAGE). As MAGE, you would be interested in making sure that students have a consistent and reliable experience in searching for courses and finding more information about instructors. This repository implements tests to verify various aspects of course information that is posted on the [Schedule of Classes](https://app.testudo.umd.edu/soc) and the [Faculty](https://mage.umd.edu/clark/facultydir) pages.

The logic to navigate web pages using Selenium is implemented in the `mage_web_scraper.py` module. The module contains functions that perform different actions on the web site:

**Schedule of Classes**

- `get_schedule_of_classes_page(...)`: opens up the [Schedule of Classes](https://app.testudo.umd.edu/soc) page and selects the specified course, term, and year. It returns the page source, whcih can be parsed by the next method.
- `get_course_info_from_schedule_of_classes_page(...)`: takes the page source (from above) and parses the information for the specified course. It returns a `Course` object with the parsed information.

**Faculty**

- `search_instructors(...)`: opens up the [Faculty](https://mage.umd.edu/clark/facultydir) page and searches for the specified instructor. It returns the page source of the search result page.
- `get_instructor_link_from_search_result_page(...)`: given the page source of the search results page (from above) finds the URL of the specified instructor's details page.
- `parse_instructor_page(...)`: visits the URL of the instructor and parses the information into an `Instructor` object.

These are all utility functions that can be used for implementing test scenarios. The modules `test_schedule_of_classses.py` and `test_faculty.py` already implement tests that use these functions.

# Getting Started

As with every other repository, fork this repository, set up the virtual environment, and install all the dependencies:

```bash
git clone git@github.com:enpm611/selenium
cd selenium
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Now, you can run the test cases by simply executing:

```bash
pytest
```

This will open the Chrome web-browser and navigate through the web pages as defined by the existing test cases.

Note, if you don't have Chrome installed, you don't have to run the tests locally. This repository specifies a GitHub Action in `.github/workflows/ui-tests.yaml` that executes the tests when you push to the repository. You can inspect the output of the GitHub Action run to see if all the tests passed.

*Detail that should not matter to you (but is worth mentioning): Selenium tests can only be run in [headless mode](https://www.browserstack.com/guide/selenium-headless-browser-testing) within GitHub Actions. That means that a browser window is not opened but the Selenium execution is "invisible". In `mage_web_scraper.py`, we check if the environment variable `HEADLESS` has been set and if so, it runs in headless mode. The GitHub Action sets that variable to `true` to ensure it always runs in headless mode as a GitHub Action. But it will run in a browser window when you execute it locally, unless you explicitly set that environment variable.*

# Exercises

Now that you are all set up, you can expand on the current implementation and add new capabilities. You can work on any of the exercises in any order you would like. If you feel you're up to it, you can try the advanced exercise.

(1) :green_circle: *EASY* | Write a test case that checks that `ENPM670` in `Spring` `2025` has exactly two sections. *For this, you will add a new function to test function to an existing module (e.g., `test_schedule_of_classes.py`) or a new module. The scraper already has functions to read the information about section for a specific course. Your test just needs to make sure that the total number of section for that course is `2`.*

(2) :green_circle: *EASY* | Write a test case that checks that every section of `ENPM664` in `Spring` `2025` has a location or is specified as `ONLINE`. *Similar to the above test, retrieve the sections for the course and iterate over the sections. Then assert that the section `location` is not set to `TBD`.*

(3) :thinking: *DOABLE* | Write a test that verifies that `ENPM611` does not have more than `10` open seats for `Spring` `2025`. *A slight extension of the previous exercise that sums up all the `open_count` for the course sections. It then asserts that the sum is not greater than `10`.*

(4) :thinking: *DOABLE* | Write a test that checks that for `ENPM611` in `Fall` `2024`, every instructor has a bio on the faculty page. *You will have to interact with both the [Schedule of Classes](https://app.testudo.umd.edu/soc) and the [Faculty](https://mage.umd.edu/clark/facultydir) pages. First, you need to get section information from the [Schedule of Classes](https://app.testudo.umd.edu/soc) page and then search for the instructor of each section on the [Faculty](https://mage.umd.edu/clark/facultydir) page.*

(5) :fire: *ADVANCED* | Extend scraper to extract the course description and write a test that checks that it exists. *You will have to identify what `DIV` the course description is in and how to read it via Selenium. Then, add a `description` field to the `Course` object and set it in `mage_web_scraper.py`. Finally, write a test case that checks for the property not to be `None`.*
