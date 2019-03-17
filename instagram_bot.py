from selenium import webdriver
import time
from utility_methods.utility_methods import *


class InstaBot:

    def __init__(self, username, password):
        """"
        Creates an instance of IGBot class.

        Args:
            username:str: The username of the user.
            password:str: The password of the user.

        Attributes:
            driver_path:str: Path to the chromedriver.exe
            driver:str: Instance of the Selenium Webdriver (chrome 72) 
            login_url:str: Url for logging into IG.
            get_user_url:str: Url to go to a users homepage on IG.
            get_tag_url:str: Url to go to search for posts with a tag on IG.
            logged_in:bool: Boolean whether current user is logged in or not.
        """

        self.username = username
        self.password = password

        self.driver_path = './chromedriver.exe'
        self.driver = webdriver.Chrome(self.driver_path)

        self.login_url = 'https://www.instagram.com/accounts/login/'
        self.get_user_url = 'https://www.instagram.com/{}'
        self.get_tag_url = 'https://www.instagram.com/explore/tags/{}/'

        self.logged_in = False


    @insta_method
    @exception
    def login(self):
        """
        Logs a user into Instagram via the web portal
        """

        self.driver.get(self.login_url)
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)

        ts = 1
        while not self.logged_in:
            try:
                self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/button/div').click()
                self.logged_in = True
            except Exception as e:
                print(e)
                time.sleep(ts) # occasional delay in element load
                ts += 1


    @insta_method
    @exception
    def search_tag(self, tag):
        """
        Naviagtes to a search for posts with a specific tag on IG.

        Args:
            tag:str: Tag to search for
        """

        self.driver.get(self.get_tag_url.format(tag))


    @insta_method
    @exception
    def get_user(self, user):
        """
        Navigates to a users profile page

        Args:
            user:str: String user.
        """

        self.driver.get(self.get_user_url.format(user))


    @insta_method
    @exception
    def follow_user(self, user=None):
        """
        Clicks the follow button once on a user's specific profile page

        Args:
            user:str: If specified, navigates to the users profile page before clicking the follow button.
        """

        if user:
            self.get_user(user)

        # filtering follow elements for buttons
        # TODO: as of 3/17/2019, these two conditions are sufficient for profile pages
        xpath_condition = self.driver.find_elements_by_xpath("//*[contains(text(), 'Follow')]")
        class_condition = self.driver.find_elements_by_class_name('_5f5mN')

        follow_buttons = [e for e in xpath_condition if e in class_condition]

        for follow_btn in follow_elements:
            follow_btn.click()


if __name__ == '__main__':

    config_file_path = './config.ini' 
    logger_file_path = './bot.log'
    config = init_config(config_file_path)
    logger = get_logger(logger_file_path)

    bot = InstaBot(config['INSTAGRAM']['USERNAME'], config['INSTAGRAM']['PASSWORD'])
    bot.login()
    bot.follow_user('garyvee')