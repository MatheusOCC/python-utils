from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class WebDriverFactory:
    '''
    Factory for automatically identifying the driver for the specific browser on the .exe given path.
    '''

    @staticmethod
    def create_driver(webdriver_exe):
        if 'edgedriver' in webdriver_exe:
            options = EdgeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            print(f"Initializing Edge in path: {webdriver_exe}")
            return webdriver.Edge(service=EdgeService(executable_path=webdriver_exe), options=options)
        elif 'chromedriver' in webdriver_exe:
            options = ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            print(f"Initializing Chrome in path: {webdriver_exe}")
            return webdriver.Chrome(service=ChromeService(executable_path=webdriver_exe), options=options)
        elif 'geckodriver' in webdriver_exe:
            options = FirefoxOptions()
            options.add_argument('--log-level=3')
            print(f"Initializing Firefox in path: {webdriver_exe}")
            return webdriver.Firefox(service=FirefoxService(executable_path=webdriver_exe), options=options)
        else:
            raise ValueError("WebDriver Não Suportado")
        

class SeleniumAutomation:
    '''
    Easier to write code using selenium webdriver.
    Implements basic interactive functions with browser elements.
    '''

    def __init__(self, webdriver_exe, url):
        self.driver = WebDriverFactory.create_driver(webdriver_exe)
        self.driver.get(url)
        self.driver.maximize_window()
    
    def go_to_page_top(self):
        self.driver.execute_script("window.scrollBy(0,0)","")
    
    def go_to_element(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element(By.XPATH, element)).perform()

    def wait_element(self, element, go_to_element=False, timeout=2):
        if go_to_element:
            self.go_to_element(element)
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, element)))
        
    def read_element(self, element, go_to_element=False, timeout=2):
        if go_to_element:
            self.go_to_element(element)
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, element))).text
    
    def write_element(self, element, input, go_to_element=False, timeout=2):
        if go_to_element:
            self.go_to_element(element)
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, element))).send_keys(input)
        
    def click_element(self, element, go_to_element=False, timeout=2):
        if go_to_element:
            self.go_to_element(element)
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, element))).click()
        
    def clear_element(self, element, go_to_element=False, timeout=2):
        if go_to_element:
            self.go_to_element(element)
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, element))).clear()

    def back(self):
        self.driver.back()

    def quit(self):
        self.driver.quit()
