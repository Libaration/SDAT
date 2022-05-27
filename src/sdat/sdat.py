from multiprocessing.connection import wait
from requests import head
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
from config import Config
from driver import Driver
import argparse
import os
import logging
from colorama import Fore, Back, Style, init
import textwrap
import pdb
init()


def main():
    # Get settings
    config = get_settings()
    # Set options
    options = Options()
    options.headless = args.headless
    is_verbose('Starting driver in headless mode....') if args.headless is True else is_verbose(
        'Starting driver in normal mode....')

    # Create driver
    driver = get_driver(options)

    # Utiliy function to wait for an element to be visible
    def waitForPresence(*argv):
        try:
            is_verbose('Waiting for page to load ' + "Timeout: " +
                       str(args.timeout) + " seconds")
            for(x) in argv:
                is_verbose('Waiting for element ' + x)
                WebDriverWait(driver, timeout=args.timeout).until(
                    EC.presence_of_element_located((By.ID, x)))

        except:
            is_verbose('Timeout reached.')
            is_verbose('Could not find county or search method dropdowns on the page. Possibly the page has changed, your network has timed out or the config.json file is incorrect.')
            is_verbose(
                'If this is a network issue, try adjusting the timeout value using the --timeout flag.')
            print('Quitting driver....')
            driver.quit()
            print('Exiting script....')
            exit()

    # Ensure the page is loaded before setting the dropdowns
    waitForPresence(config.county, config.search_method, config.submit_button)

    # Set dropdowns to select on first page
    dropdowns = {
        'county': Select(driver.find_element(By.ID, config.county)),
        'search_method': Select(driver.find_element(By.ID, config.search_method)),
        'submit_button': driver.find_element(By.ID, config.submit_button)
    }

    # Select dropdowns selections on first page
    select_first_page(dropdowns)

    # Ensure second page is loaded before entering street number and street name
    waitForPresence(config.steet_number, config.street_name,
                    config.second_page_submit_button)

    # Enter street number and street name
    text_fields = {
        'steet_number': driver.find_element(By.ID, config.steet_number),
        'street_name': driver.find_element(By.ID, config.street_name),
        'second_page_submit_button': driver.find_element(By.ID, config.second_page_submit_button)
    }
    select_second_page(text_fields)

    # Ensure final content container is loaded before getting the data
    waitForPresence(config.final_content_container)

    # Extract data from final content container
    containers = {
        'final_content_container': driver.find_element(By.ID, config.final_content_container)
    }
    scrape_data(containers, config)

    time.sleep(30)
########################################################################################################################


def scrape_data(containers, config):
    is_verbose('Scraping data...')
    print(Fore.RED + 'no parameters set to scrape atm c: so..... HERES EVERYTHING' + Style.RESET_ALL)
    time.sleep(3)
    # pdb.set_trace()
    tr_list = containers.get(
        'final_content_container').find_elements(By.TAG_NAME, 'tr')
    for tr in tr_list:
        td_list = tr.find_elements(By.TAG_NAME, 'td')
        if len(td_list) > 0:
            for td in td_list:
                print(Fore.GREEN + td.text + Style.RESET_ALL)
    exit()


def select_first_page(dropdowns):
    is_verbose('Selecting county...')
    dropdowns['county'].select_by_visible_text('BALTIMORE CITY')
    is_verbose('Selecting search method...')
    dropdowns['search_method'].select_by_visible_text('STREET ADDRESS')
    is_verbose('Submitting form...')
    dropdowns['submit_button'].click()


def select_second_page(text_fields):
    text_fields['steet_number'].send_keys(args.street_number)
    text_fields['street_name'].send_keys(args.street_name)
    is_verbose('Submitting form...')
    text_fields['second_page_submit_button'].click()


def get_settings():
    config = Config()
    is_verbose("Loading configuration file...")
    is_verbose("County ID: " + config.county)
    is_verbose("Search Method ID: " + config.search_method)
    is_verbose("Street Number ID: " + config.steet_number)
    is_verbose("Street Name ID: " + config.street_name)
    is_verbose("Submit Button ID: " + config.submit_button)
    is_verbose("Second Page Submit Button ID: " +
               config.second_page_submit_button)
    is_verbose("Final Content Container ID: " + config.final_content_container)
    is_verbose("Loaded configuration file successfully.")
    return config


def get_driver(opts):
    driver = Driver(opts)
    return driver.control


def is_verbose(message=None):
    if args.verbose == True and message is not None:
        print(Fore.GREEN + '[sdat.py] ' + Style.RESET_ALL +
              Back.BLACK + Fore.WHITE + message + Style.RESET_ALL)


if __name__ == "__main__":
    with open('logo.txt') as f:
        logo = f.readlines()
    parser = argparse.ArgumentParser(
        description=textwrap.dedent('''\
            %s''' % ''.join(logo)),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('street_number', action='store', type=int,
                        help='Street number to search for (Format: "Street Number Street Name")(Example: 920)', default=None)
    parser.add_argument('street_name', action='store', type=str,
                        help='Street name to search for (Format: "Street Number Street Name")(Example: Conkling) !!!! Do not enter street name suffixes (Avenue, Street, Lane, etc.)', default=None)
    parser.add_argument('-H', '--headless', action='store_false',
                        help='Turn off headless mode (No browser window) (Default: False)')
    parser.add_argument('-V', '--verbose', action='store_true',
                        help='Print verbose output (Prints status messages to the console) (Default: False)')
    parser.add_argument('-T', '--timeout', action='store',
                        help='Set timeout value in seconds (How long before the script gives up on loading the page) (Default 3 Seconds)', type=int, default=3)
    args = parser.parse_args()
    if args.verbose is False:
        os.environ['WDM_LOG'] = "false"
        logging.getLogger('WDM').setLevel(logging.NOTSET)
    if args.street_number and args.street_name is not None:
        main()
