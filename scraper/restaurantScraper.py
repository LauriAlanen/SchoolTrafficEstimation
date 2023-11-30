from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_element(driver, search_type, search_str):
    try:
        element = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((search_type, search_str))
        )
        return element
    
    except TimeoutException:
        print("Unable to locate element")
        return TimeoutException;


def wait_elements(driver, search_type, search_str):
    try:
        elements = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((search_type, search_str))
        )
        return elements

    except TimeoutException:
        print("Unable to locate elements")
        return TimeoutException;


def select_groups(driver):
    available_groups = wait_elements(driver, By.CLASS_NAME, "search-result-row")
    
    if (available_groups == TimeoutException):
        return 1
    
    for group in available_groups:
        group_name = wait_element(group, By.CLASS_NAME, "code")
        reserved_classes = wait_element(group, By.CLASS_NAME, "credits")
        total_classes = reserved_classes.text.split()[0]

        if (int(total_classes) > 10):
            button = wait_element(group, By.CLASS_NAME, "btn")
            button.click()

    return 0

def website_controller(driver, study_sector):
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

def get_php_session_id(driver):
    cookies = driver.get_cookies()
    return cookies[0]["value"]




    