from requests import head
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class Driver:
    def __init__(self, opts):
        self.options = opts
        self.control = self.new_driver()

    def new_driver(self):
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=self.options)
        driver.get(
            "https://sdat.dat.maryland.gov/RealProperty/Pages/default.aspx")
        return driver
