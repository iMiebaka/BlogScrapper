import time
from decouple import config
from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class LinkedInBlogScraper:
    def __init__(self, email, password):
        # Initialize Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.email = email
        self.password = password

    def login(self):
        """Logs into LinkedIn."""
        self.driver.get("https://www.linkedin.com/login")
        time.sleep(2)

        email_input = self.driver.find_element(By.ID, "username")
        email_input.send_keys(self.email)
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)

        time.sleep(5) 


    

    def scrape_articles(self, url_path: str) -> tuple[list, int]:
        """Scrapes articles from the search results."""
        
        articles = []
        blogs_found = 0
        self.driver.get(url_path)
        post_elements = self.driver.find_elements(By.CLASS_NAME, 'search-results__search-feed-update')

        for post_element in post_elements:
            try:
                feed_result = post_element.find_element(By.CLASS_NAME, 'feed-shared-update-v2__description')
                # feed_result = post_element.find_element(By.CLASS_NAME, 'update-components-text relative update-components-update-v2__commentary')
            except common.exceptions.NoSuchElementException:
                continue
            blog_text = feed_result.text
            if "blog" in blog_text.lower() or "article" in blog_text.lower():
                blogs_found += 1
                try:
                    # Check for the presence of an <a> tag
                    link_elements = feed_result.find_elements(By.TAG_NAME, "a")
                    for link_element in link_elements:
                        blog_link = link_element.get_attribute("href")

                        # Filter out hashtags
                        if "https://www.linkedin.com/feed/hashtag" not in blog_link:
                            articles.append(blog_link)
                except common.exceptions.NoSuchElementException:
                    print("No link found in the blog element.")

                    
        return articles, blogs_found,  len(post_elements)

    def close(self):
        """Closes the browser."""
        self.driver.quit()

