from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MAX_RETRIES = 3
WAIT_TIMEOUT = 10

def wait_element(driver, search_type, search_str):
    for attempt in range(MAX_RETRIES):
        try:
            element = WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((search_type, search_str))
            )
            return element
        
        except (TimeoutException, StaleElementReferenceException):
            print("Unable to locate element, retrying...")

            if(attempt == MAX_RETRIES):
                print(F"Tried {MAX_RETRIES}, but unable to locate element")
                raise 

def wait_elements(driver, search_type, search_str):
    for attempt in range(MAX_RETRIES):
        try:
            elements = WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.presence_of_all_elements_located((search_type, search_str))
            )
            
            return elements
        
        except (TimeoutException, StaleElementReferenceException):
            print("Unable to locate element, retrying...")  

            if(attempt == MAX_RETRIES):
                print(F"Tried {MAX_RETRIES}, but unable to locate elements")
                raise

# Tässä on bugi
def select_available_groups(driver):
    available_groups = wait_elements(driver, By.CLASS_NAME, "search-result-row")
    
    if not available_groups:
        return 1
    
    for group in available_groups:
        try:
            #group_name = wait_element(group, By.CLASS_NAME, "code")
            reserved_classes = wait_element(group, By.CLASS_NAME, "credits")
            total_classes = reserved_classes.text.split()[0]

            if (int(total_classes) > 10):
                button = wait_element(group, By.CLASS_NAME, "btn")
                button.click()
        
        except (StaleElementReferenceException, AttributeError):
            print("Unable to locate element trying again...")
            available_groups = wait_element(driver, By.CLASS_NAME, "search-result-row")
            continue

    return 0

def search_groups(driver, study_sector):
    try:
        form = wait_element(driver, By.CLASS_NAME, "form-control")
        form.send_keys(study_sector)

        select_group_search = wait_element(driver, By.CSS_SELECTOR, ".btn-group-toggle > label:nth-child(2)")
        select_group_search.click()
        
    except TimeoutException:
        print("Cant locate elements")
        exit(TimeoutException)


def create_driver(url):
    options = ChromeOptions()
    options.accept_insecure_certs = True
    options.add_argument("--headless") #enabled if you want to run without gui

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    return driver

def get_php_session_cookie(driver):
    cookies = driver.get_cookies()
    return cookies[0]["value"]
    