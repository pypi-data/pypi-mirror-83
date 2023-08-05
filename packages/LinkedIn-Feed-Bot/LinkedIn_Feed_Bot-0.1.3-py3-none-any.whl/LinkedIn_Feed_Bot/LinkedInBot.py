from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
from LinkedIn_Feed_Bot.utils import write_to_element 
import itertools
import pandas as pd

class bot:
    """This is a bot that does three things: sign-in, 
    scroll through the Feed and extract data from the Feed.
    """

    def __init__(self, webdriver_path):
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(webdriver_path, options=chrome_options)
        self.driver.get('https://www.linkedin.com/')
        sleep(5)
        
    def sign_in(self, username, password, use_js = True):
        """Input your username and password in order to sign in to LinkedIn.
         No data is kept, of course. 

        Args:
            username (str)
            password (str)
            use_js (bool, optional): The use_js argument is for the user to choose 
            between native Selenium input of data or the use of js scripts to inscribe data. Defaults to True.

        Raises:
            Exception: Sometimes, if the user uses too much, LinkedIn will probably throw a captcha.
            Other than that, may be some error with the Webdriver.
        """
        if(self.driver.current_url != 'https://www.linkedin.com/'):
            raise Exception("Sorry, LinkedIn has probably thrown a captcha. Try again some other time.")
        
        write_to_element(self.driver, '//*[(@id = "session_key")]', username, use_js)
        sleep(2)
        self.driver.find_element_by_css_selector("#session_password").clear()
        sleep(0.5)
        write_to_element(self.driver, '//*[(@id = "session_password")]', password)
        sleep(1)
        self.driver.find_element_by_xpath('//*[(@id = "session_password")]').send_keys(Keys.RETURN)
        sleep(5)

    def scroll_down(self):
        sleep(1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def df_author_post(self, tags=None, authors=None):
        """Scraping in the feed on the current window the author's name and title along with each post.
        Also, we could filter by tags in the post and author's name. 

        Return: 
                Pandas.DataFrame

        Args:
            tags (list): list of tags to filter the posts. Defaults to None.
            authors (list): list of authors names. Defaults to None.
        """
        feed_boxes = self.driver.find_elements_by_css_selector('.relative.ember-view')
        
        df = pd.DataFrame(columns=('author_name', 'author_title', 'post'))

        for i, fb in enumerate(feed_boxes):
            post =  fb.find_elements_by_css_selector('div.feed-shared-update-v2__commentary')
            name =  fb.find_elements_by_css_selector('span.feed-shared-actor__title .hoverable-link-text.t-black span')
            title =  fb.find_elements_by_css_selector('span.feed-shared-actor__description')

            # The object of feed boxes, is not unique.
            # It repeat itself, so we must drop duplicates.
            df = df.drop_duplicates()
            
            # Populating our dataframe.
            # Checking if this is a regular LinkedIn post where we have the post,
            # the name and title of the author. 
            if(len(post) == len(name) == len(title) == 1):
                    # Acessing the list and retrieving the text from the webelement
                    df.loc[i] = [name[0].text, title[0].text, post[0].text]

        # The object of feed boxes, is not unique.
        # It repeat itself, so we must drop duplicates.
        df = df.drop_duplicates()
        # Filtering for the tags and authors that we wants
        if tags is not None:
            for tag in tags:
                tag = '#' + tag
                # Checking if there a tag in each post
                df = df[df.apply(lambda row: tag in row.post, axis=1)]
        if authors is not None:
            for author in authors:
                # Checking if the author name is the one selected
                df = df[df.apply(lambda row: author in row.author_name, axis = 1)]

        return(df)
    
    def quit(self):
        sleep(1)
        self.driver.close()
        self.driver.quit()