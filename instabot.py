from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


class InstagramBot:
    def __init__(self, email, password):
        """ Initialise the bot with the browser, username and password """
        self.browser_profile = webdriver.ChromeOptions()
        self.browser_profile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browser_profile)
        self.email = email
        self.password = password

    def sign_in(self):
        """ Signs into instagram using email and password """
        self.browser.get('https://www.instagram.com/accounts/login/')
        email_input = self.browser.find_elements_by_css_selector('form input')[0]
        password_input = self.browser.find_elements_by_css_selector('form input')[1]
        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(2)

    def follow_with_username(self, username):
        """ Follows the specified user. If you already its follower, it just notifies you that are already a follower """
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        follow_button = self.browser.find_element_by_css_selector('button')
        if follow_button.text != 'Following':
            follow_button.click()
            time.sleep(2)
            print("You are now following "+username)
        else:
            print("You are already following this user")
    
    def unfollow_with_username(self, username):
        """ Unfollows the specified user. If you are a follower of that user, it notifies that you are not following this user """
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        follow_button = self.browser.find_element_by_css_selector('button')
        if follow_button.text == 'Following':
            follow_button.click()
            time.sleep(2)
            confirm_button = self.browser.find_element_by_xpath('//button[text() = "Unfollow"]')
            confirm_button.click()
        else:
            print("You are not following this user")
    
    def get_user_followers(self, username, max_followers):
        """ Prints the user profile link of the followers depending upon the specified followers count of the specified user """
        try:
            self.browser.get('https://www.instagram.com/' + username)
            followers_link = self.browser.find_element_by_css_selector('ul li a')
            followers_link.click()
            time.sleep(2)
            followers_list = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')

            followers_list.click()
            
            followers = []
            for user in followers_list.find_elements_by_css_selector('li'):
                user_link = user.find_element_by_css_selector('a').get_attribute('href')
                print(user_link)
                followers.append(user_link)
                if len(followers) == max_followers:
                    break
            return followers
        except NoSuchElementException as err:
            print("NoSuchElementException exception :: "+str(err))
            return []
        except Exception as err:
            print("Exception:: "+str(err))
            return []

    def close_browser(self):
        """ Closes the browser """
        self.browser.close()

bot = InstagramBot('USERNAME','PASSWORD')
bot.sign_in()
bot.follow_with_username('zuck')
bot.unfollow_with_username('zuck')
bot.get_user_followers('zuck',10)
bot.close_browser()