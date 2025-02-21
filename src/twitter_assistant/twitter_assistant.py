"""
twitter assistant
"""
import logging
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# config
CONFIG = {'username': '',
          'password': '',
          'sleep_short': 1,
          'sleep_mid': 3,
          'sleep_long': 5,
          'webdriver_wait': 3,
          'search_query': '',
          'nuke_query': '',
          'ffprofile_folder': r'',
          'ffbinary': r'',
          'debug': False,
          'log_format': '%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s'}

TARGETS =  {'login': 'https://x.com/i/flow/login'}

# css selectors
SELECTORS = {'username_login_field': 'input[autocomplete="username"]',
             'login_next_button': 'button[role="button"]',
             'password_login_field': 'input[name="password"]',
             'login_button': 'button[data-testid="LoginForm_Login_Button"]',
             'home_nav_item': 'a[href="/home"]',
             'explore_nav_item': 'a[href="/explore"]',
             'home_nav': 'nav[aria-live="polite"]',
             'foryou_nav_item': 'div[role="presentation"]',
             'communities_nav_item': 'a[href*="/communities"]',
             'search_field': 'input[data-testid="SearchBox_Search_Input"]',
             'timeline': 'div[aria-label*="Timeline:"]',
             'nuke_button': 'a.nuke-button',
             'nuke_confirm': 'button[value="true"]'}

SEARCH_QUERIES = {'racism': 'white excellence'}

NUKE_QUERIES = {
    'foryou': 'home'
}

# init logger
def init_logger():
    # init log formatter
    logFormatter = logging.Formatter(CONFIG['log_format'])
    # get root logger
    rootLogger = logging.getLogger()
    # init std logger
    stdLogger = logging.StreamHandler()
    stdLogger.setFormatter(logFormatter)
    # add std log handler
    rootLogger.addHandler(stdLogger)
    # set default log level
    rootLogger.setLevel(logging.INFO)
    log('logger initialized')

# log
def log(msg, level = logging.INFO):
    # log if enabled
    if CONFIG['debug']:
        match level:
            case logging.INFO:
                logging.info(msg)
            case logging.DEBUG:
                logging.debug(msg)
            case logging.WARN:
                logging.warning(msg)
            case logging.ERROR:
                logging.error(msg)

# firefox webdriver singleton
class ffdriver(object):
    # singleton
    _instance = None
    # new
    def __new__(cls):
        if cls._instance is None:
            log('creating web driver')
            # setup firefox profile
            options = Options()
            # set browser binary option
            if CONFIG['ffbinary'] != '':
                ffbinary = CONFIG['ffbinary']
                log('setting browser binary: %s' %ffbinary)
                options.binary_location = ffbinary
            # set browser profile option
            if CONFIG['ffprofile_folder'] != '':
                ffprofile_folder = CONFIG['ffprofile_folder']
                log('setting browser profile: %s' %ffprofile_folder)
                options.profile = FirefoxProfile(ffprofile_folder)
            # create webdriver with options
            cls._instance = webdriver.Firefox(options)
            # wet webdriver implicitly wait
            # todo: need better wait strategy
            cls._instance.implicitly_wait(CONFIG['webdriver_wait'])
        return cls._instance

# find element(s) by css selector
def find_elem(driver, css_selector, multi=False):
    if not multi:
        return driver.find_element(By.CSS_SELECTOR, css_selector)
    else:
        return driver.find_elements(By.CSS_SELECTOR, css_selector)

# login to website
def login():
    # get driver
    driver = ffdriver()
    # open webpage
    driver.get(TARGETS['login'])
    # sleep let load
    time.sleep(CONFIG['sleep_mid'])
    ## login
    # find username input field and populate it
    username_input = find_elem(driver, SELECTORS['username_login_field'])
    username_input.send_keys(CONFIG['username'])
    # find and press next button
    buttons = find_elem(driver, SELECTORS['login_next_button'], True)
    next_button = buttons[2]
    next_button.click()
    # sleep let load
    time.sleep(CONFIG['sleep_long'])
    # find password input field and populate it
    password_input = find_elem(driver, SELECTORS['password_login_field'])
    password_input.send_keys(CONFIG['password'])
    # find login button and press it
    login_button = find_elem(driver, SELECTORS['login_button'])
    login_button.click()

def close():
    log('close')
    # get driver
    driver = ffdriver()
    # quit
    log('quitting web driver')
    driver.quit()
    # close logger
    log('shutting down logger')
    logging.shutdown()

def navigate(page):
    log('navigate to %s' %page)
    # get driver
    driver = ffdriver()
    match page:
        case 'foryou':
            # find home link
            home_link = find_elem(driver, SELECTORS['home_nav_item'])
            home_link.click()
            # find for you and click
            home_nav = find_elem(driver, SELECTORS['home_nav'])
            home_nav.find_element(By.CSS_SELECTOR, SELECTORS['foryou_nav_item']).click()
        case 'explore':
            # find explore link
            explore_link = find_elem(driver, SELECTORS['explore_nav_item'])
            explore_link.click()
        case 'communities':
            # find communities link
            communities_link = find_elem(driver, SELECTORS['communities_nav_item'])
            communities_link.click()

def search(query):
    log('search: %s' %query)
    # get driver
    driver = ffdriver()
    # find and populate search field
    search_input = find_elem(driver, SELECTORS['search_field'])
    search_input.send_keys(query)
    search_input.send_keys(Keys.ENTER)

def skip_search_garbage(timeline):
    log('skip search garbage')
    # get driver
    driver = ffdriver()
    # get through top garbage
    for x in range(0, 5):
        log('traversing garbage')
        timeline.send_keys('j')
        time.sleep(CONFIG['sleep_short'])
        # get active element dom attribute
        attr = driver.switch_to.active_element.get_dom_attribute('data-testid')
        # check for other than none
        if attr != None:
            log('found another tweet')
            # break loop once we find a tweet
            return attr
    log('no more tweets found')
    return None
    
def navigate_block_search_timeline():
    log('navigate block search timeline')
    # get driver
    driver = ffdriver()
    # track user links
    user_hrefs = set()
    # track dom attributes
    attr = ''
    # find html element to traverse by key strokes
    timeline = driver.find_element(By.TAG_NAME, 'html')
    # sleep let load
    time.sleep(CONFIG['sleep_mid'])
    ## navigate
    # skip garbage
    attr = skip_search_garbage(timeline)
    # start going through tweets
    while attr == 'tweet':
        # get user link
        href = driver.switch_to.active_element.find_element(By.TAG_NAME, 'a').get_dom_attribute('href')
        # check if we already blocked the account
        if href not in user_hrefs:
            log('blocking account %s' %href)
            # block account
            driver.switch_to.active_element.send_keys('x')
            time.sleep(CONFIG['sleep_short'])
            driver.switch_to.active_element.send_keys(Keys.ENTER)
            time.sleep(CONFIG['sleep_short'])
            # track account
            user_hrefs.add(href)
        else:
            log('already blocked %s' %href)
        # traverse
        attr = skip_search_garbage(timeline)
        # sleep let load
        time.sleep(CONFIG['sleep_short'])

# poll nuke processing
def pollNukeProcsesing():
    log('poll nuke processing...')
    # init return
    stillProcessing = True
    # get driver
    driver = ffdriver()
    # poll for processing
    while stillProcessing:
        try:
            # try to select element
            driver.switch_to.active_element.find_element(By.CSS_SELECTOR, 'div#processing')
        except:
            # break loop, set return
            stillProcessing = False
        else:
            # log, sleep
            log('...processing...')
            time.sleep(1)
    return stillProcessing

# navigate and nuke a timeline
def navigate_nuke_timeline():
    log('navigate nuke timeline')
    # get driver
    driver = ffdriver()
    # track dom attributes
    attr = ''
    # find html element to traverse by key strokes
    timeline = driver.find_element(By.TAG_NAME, 'html')
    # sleep let load
    time.sleep(CONFIG['sleep_mid'])
    ## navigate
    # skip garbage
    attr = skip_search_garbage(timeline)
    # start going through tweets
    while attr == 'tweet':
        # get username
        username = driver.switch_to.active_element.find_element(By.TAG_NAME, 'a').get_dom_attribute('href').split('/')[1]
        # init nuke_button
        nuke_button = None
        # try to select nuke button
        try:
            # get user link
            nuke_button = driver.switch_to.active_element.find_element(By.CSS_SELECTOR, SELECTORS['nuke_button'])
            # block account
        except:
            # log
            log('skipping white listed account: %s' %username)
        else:
            # log
            log('attempting to nuke: %s' %username)
            # nuke
            nuke_button.click()
            # confirm nuke
            driver.switch_to.active_element.find_element(By.CSS_SELECTOR, SELECTORS['nuke_confirm']).click()
            # poll nuke processing
            pollNukeProcsesing()
        finally:
            # traverse
            attr = skip_search_garbage(timeline)
            # sleep let load
            time.sleep(CONFIG['sleep_short'])

# test nuke button blocking
def test_nuke_button_blocking():
    log('test nuke button blocking')
    # navigate to for you
    navigate('foryou')
    navigate_nuke_timeline()

# test blocking in search results
def test_blocking_in_search_results():
    log('test blocking in search results')
    #navigate, search, block
    navigate('explore')
    search(CONFIG['search_query'])
    navigate_block_search_timeline()

# test blocking in communities section
def test_blocking_in_communities():
    log('test blocking in communities')
    # navigate, search, block
    navigate('communities')
    navigate_block_search_timeline()

# use driver to add cookies
def add_cookie(name, value):
    log('add cookie %s' %name)
    # get driver
    driver = ffdriver()
    # add cookie
    driver.add_cookie({'name': name,
                       'value': value,
                       'domain': '.x.com',
                       'path': '/',
                       'expires': 365,
                       'sameSite': 'None',
                       'secure': True})
    
# set cookies
def set_cookies():
    log('set cookies')
    ID = 'v7:777777777777777777'
    S = 'bye+bye+hands+and+feet!!!!!!!'
    # set cookies
    add_cookie('guest_id', ID)
    add_cookie('guest_id_marketing', ID)
    add_cookie('guest_id_ads', ID)
    add_cookie('personalization_id', S)

# init cmdline argument parser
def init_cmdline_parser():
    # create parser
    parser = argparse.ArgumentParser(
        prog='twitter assistant!',
        description='assist in the twittering...',
        epilog='from yassghn, with love <333, :D')
    # set options
    parser.add_argument('-s', '--search', metavar='[QUERY]', type=str, help='add search query')
    parser.add_argument('-nb', '--nuke-button', metavar='[QUERY]', help='use nuke button to block')
    parser.add_argument('-v', '--verbose', action='store_true', help='turn on verbose logging')
    # return parser 
    return parser

# parse cmdline options
def parse_cmdline_options(parser):
    # parse cmdline arguments
    args = parser.parse_args()
    ## parse args
    # check search string
    if args.search is not None:
        # check if search string is correct
        if args.search in SEARCH_QUERIES.keys():
            CONFIG['search_query'] = SEARCH_QUERIES[args.search]
        # error
        else:
            log('query error', logging.ERROR)
            print('ERROR: incorrect query value')
            print('query value must be one of...')
            print(list(SEARCH_QUERIES.keys()))
            # return exit code
            return 1
    # check search string
    if args.nuke_button is not None:
        # check if search string is correct
        if args.nuke_button in NUKE_QUERIES.keys():
            CONFIG['nuke_query'] = NUKE_QUERIES[args.nuke_button]
        # error
        else:
            log('query error', logging.ERROR)
            print('ERROR: incorrect query value')
            print('query value must be one of...')
            print(list(NUKE_QUERIES.keys()))
            # return exit code
            return 1
    # check verbose
    if args.verbose is True:
        # init logger
        init_logger()
        # enable logging
        CONFIG['debug'] = True
    return 0

# set default config options
def set_default_config():
    log('set default config')
    # check if search query was set from cmdline
    if CONFIG['search_query'] == '':
        # set default search query
        CONFIG['search_query'] = SEARCH_QUERIES['racism']

# prep assistance
def preassist():
    # get commandline parser
    parser = init_cmdline_parser()
    # try to parse cmdline arguments
    if parse_cmdline_options(parser) == 1:
        # return exit code
        return 1
    log('--preassist--')
    log('done parsing commandline')
    # set default config options after cmdline
    set_default_config()

# let the assistant assist
def assist():
    log('--assist--')
    # login
    login()
    # set cookies
    set_cookies()
    # test blocking
    if CONFIG['nuke_query'] != '':
        test_nuke_button_blocking()
    test_blocking_in_search_results()
    test_blocking_in_communities()

# wrap up assisting
def postassist():
    log('--postassist--')
    # close webdriver
    close()

def main():
    """start"""
    print('twitter assistant!')
    # prep assistance
    if preassist() == 1:
        # return exit code
        return 1
    # let the assistant assist
    assist()
    # wrap up assisting
    postassist()
    # return success
    return 0