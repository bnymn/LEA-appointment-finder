import os
import time
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from typing import Callable
from typing import Literal
from typing import TypeVar
from typing import Union

D = TypeVar("D", bound=Union[WebDriver, WebElement])
T = TypeVar("T")

class BerlinTerminMachen:
    browser_window_width = 1280
    """The width of the browser window. This configuration will affect the size of the screenshot,
    visibility of the elements in the screenshot."""

    browser_window_height = 2048
    """The height of the browser window. This configuration will affect the size of the screenshot,
    visibility of the elements in the screenshot."""

    appointment_url = "https://otv.verwalt-berlin.de/ams/TerminBuchen?lang=en"

    timeout_for_wait_in_seconds = 60

    def __init__(self):
        options = Options()
        options.add_argument("--headless")  # Run headless
        options.add_argument("--use_subprocess")
        options.add_argument("--no-sandbox")  # Bypass OS security model
        options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        options.add_argument("--disable-extensions")
        options.add_argument("--remote-debugging-port=9222")  # This is important!
        
        self.driver = uc.Chrome(options=options, driver_executable_path='/usr/bin/chromedriver')
        self.driver.set_window_size(BerlinTerminMachen.browser_window_width, BerlinTerminMachen.browser_window_height)

        self.actions = ActionChains(self.driver)
        
        self.wait = WebDriverWait(self.driver, BerlinTerminMachen.timeout_for_wait_in_seconds)
        
        self.timestamp = int(time.time())
        
        self.directory = f"./output/{self.timestamp}"
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
        self.artifact_prefix = f"{self.directory}/{self.timestamp}"

        self.artifact_counter = 0

    def __del__(self):
        self._take_screenshot("final")
        self.driver.quit()

    def visit_appointment_page(self):
        self.driver.get(BerlinTerminMachen.appointment_url)

    def click_book_appointment(self):
        book_appointment_link = self.driver.find_element(By.LINK_TEXT, "Book Appointment")
        self._click_to_element(book_appointment_link)

    def wait_until_appointment_agreement_page_to_load(self):
        self._wait_until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "span#xi-txt-1 h1 span"), "Appointment agreement"),
            "appointment_agreement_page_to_load"
        )

    def click_consent_checkbox(self):
        checkbox = self.driver.find_element(By.ID, "xi-cb-1")
        self._click_to_element(checkbox)

    def click_next_button_to_move_service_selection(self):
        self._click_application_form_proceed_button()

    def wait_until_service_selection_page_is_loaded(self):
        self._wait_until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#xi-fs-19 legend"), "Information about the concern"),
            "service_selection_page_is_loaded"
        )

    def select_citizenship(self):
        self._select_option_by_text(
            self.driver.find_element(By.ID, "xi-sel-400"),
            "Turkey"
        )

    def wait_until_number_of_applicants_is_visible(self):
        self._wait_until(
            EC.visibility_of_element_located((By.ID, "xi-div-32")),
            "number_of_applicants_is_visible"
        )
    
    def select_number_of_applicants(self):
        self._select_option_by_text(
            self.driver.find_element(By.ID, "xi-sel-422"),
            "two people"
        )
    
    def wait_until_residency_in_berlin_is_visible(self):
        self._wait_until(
            EC.visibility_of_element_located((By.ID, "xi-sel-427")),
            "residency_in_berlin_is_visible"
        )
    
    def select_residency_in_berlin(self):
        self._select_option_by_text(
            self.driver.find_element(By.ID, "xi-sel-427"),
            "yes"
        )
    
    def wait_until_citizenship_of_family_member_is_visible(self):
        self._wait_until(
            EC.visibility_of_element_located((By.ID, "xi-sel-428")),
            "citizenship_of_family_member_is_visible"
        )
    
    def select_citizenship_of_family_member(self):
        self._select_option_by_text(
            self.driver.find_element(By.ID, "xi-sel-428"),
            "Turkey"
        )

    def wait_until_parent_services_are_visible(self):
        self._wait_until(
            EC.visibility_of_element_located((By.XPATH, "//label[p[contains(text(), 'Extend a residence title')]]")),
            "services_are_visible"
        )
    
    def click_the_parent_service(self):
        link = self.driver.find_element(By.XPATH, "//label[p[contains(text(), 'Extend a residence title')]]")
        self._click_to_element(link)
    
    def wait_until_service_category_is_visible(self):
        self._wait_until(
            EC.visibility_of_element_located((By.XPATH, "//label[p[contains(text(), 'Family reasons')]]")),
            "service_category_is_visible"
        )
    
    def click_to_service_category(self):
        link = self.driver.find_element(By.XPATH, "//label[p[contains(text(), 'Family reasons')]]")
        self._click_to_element(link)
    
    def wait_until_services_are_visible(self):
        self._wait_until(
            EC.visibility_of_element_located((By.XPATH, "//label[contains(text(), 'Residence permit for spouses and children of holders of an EU Blue Card (sect. 29-32)')]")),
            "services_are_visible"
        )
    
    def click_to_the_service(self):
        link = self.driver.find_element(By.XPATH, "//label[contains(text(), 'Residence permit for spouses and children of holders of an EU Blue Card (sect. 29-32)')]")
        self._click_to_element(link)

    def wait_until_loading_is_done(self, description: str = "loading_is_done"):
        self._wait_until(
            EC.invisibility_of_element((By.CLASS_NAME, "loading")),
            description
        )

    def click_next_button_to_move_date_selection(self):
        self._click_application_form_proceed_button()

    def wait_until_date_selection_is_visible(self):
        self._wait_until(
            EC.visibility_of_element_located((By.XPATH, "//legend[normalize-space() = 'Appointment selection']")),
            "date_selection_is_visible"
        )
        raise Exception("Available date not found")
    
    def save_source_code_of_date_selection_page(self):
        self._save_source_code_to_file("data_selection_source_code")
    
    def rename_artifact_folder_as_found(self):
        os.rename(self.directory, f"{self.directory}_found")

    def _wait_until(self, method: Callable[[D], Union[Literal[False], T]], description: str):
        try:
            self.wait.until(method)
            message = f"{description}_success"
            print(message)
            self._take_screenshot(message)
        except TimeoutException:
            message = f"{description}_failed"
            print(message)
            self._take_screenshot(message)

    def _take_screenshot(self, description: str):
        filename = self._get_artifact_filename(f"{description}.png")
        self.driver.save_screenshot(filename)

    def _click_to_element(self, element: WebElement):
        self.actions.move_to_element(element).click().perform()
        time.sleep(2)
    
    def _select_option_by_text(self, element: WebElement, text: str):
        select = Select(element)
        select.select_by_visible_text(text)
        time.sleep(2)
    
    def _click_application_form_proceed_button(self):
        button = self.driver.find_element(By.ID, "applicationForm:managedForm:proceed")
        self._click_to_element(button)

    def _save_source_code_to_file(self, description: str):
        source_code = self.driver.page_source
        filename = self._get_artifact_filename(f"{description}.html")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(source_code)
    
    def _get_artifact_filename(self, filename: str):
        filename = f"{self.artifact_prefix}_{self.artifact_counter}_{filename}"
        self.artifact_counter += 1
        return filename
    
app = BerlinTerminMachen()
app.visit_appointment_page()
app.click_book_appointment()

app.wait_until_appointment_agreement_page_to_load()
app.click_consent_checkbox()
app.click_next_button_to_move_service_selection()

app.wait_until_service_selection_page_is_loaded()
app.select_citizenship()

app.wait_until_number_of_applicants_is_visible()
app.select_number_of_applicants()

app.wait_until_residency_in_berlin_is_visible()
app.select_residency_in_berlin()

app.wait_until_citizenship_of_family_member_is_visible()
app.select_citizenship_of_family_member()

app.wait_until_parent_services_are_visible()
app.click_the_parent_service()

app.wait_until_service_category_is_visible()
app.click_to_service_category()

app.wait_until_services_are_visible()
app.click_to_the_service()

app.wait_until_loading_is_done()
app.click_next_button_to_move_date_selection()

app.wait_until_date_selection_is_visible()
app.save_source_code_of_date_selection_page()
app.rename_artifact_folder_as_found()
