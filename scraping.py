# import packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from parsel import Selector
import csv

writer = csv.writer(open('output.csv', 'w', encoding='utf-8'))
writer.writerow(['Name', 'URL', 'Email', 'Headline'])


driver = webdriver.Chrome('./chromedriver')

# LINKEDIN

# access LinkedIn
driver.get('https://www.linkedin.com/')
sleep(1)

# Log in to LinkedIn
driver.find_element_by_xpath('//*[@id="session_key"]').click()
sleep(1)

user_input = driver.find_element_by_name('session_key')
user_input.send_keys('User input')

password_input = driver.find_element_by_name('session_password')
password_input.send_keys('User password')

password_input.send_keys(Keys.RETURN)
sleep(1)

# GOOGLE
driver.get('https://google.com')
sleep(1)

# Collect the URLs from query result
search_input = driver.find_element_by_name('q')

search_input.send_keys(
    'site:linkedin.com/in/ AND "data scientist" and "São José dos Campos"')
search_input.send_keys(Keys.RETURN)
sleep(1)

profiles_list = driver.find_elements_by_xpath('//div[@class="yuRUbf"]/a')
profiles_list = [profile.get_attribute('href') for profile in profiles_list]

for profile in profiles_list:
    try:
        driver.get(profile)
        sleep(1)

        response = Selector(text=driver.page_source)

        name = response.xpath('//title/text()').extract_first().split(" | ")[0]
        headline = driver.find_element_by_xpath(
            '//div[@class="text-body-medium break-words"]').text
        url_profile = driver.current_url

        driver.find_element_by_xpath(
            '//*[@id="top-card-text-details-contact-info"]').click()
        sleep(1)

        component_links = driver.find_elements_by_xpath(
            '//a[@href]')
        link = []
        email = None
        for component in component_links:
            if '@' in component.text and ' ' not in component.text:
                email = component.text

        writer.writerow([name, url_profile, email, headline])
    except:
        None

driver.quit()
