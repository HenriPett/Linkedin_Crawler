# import packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from parsel import Selector
import csv


def build_query(location_inputs, niche_inputs, position_inputs, other_inputs):
    base_query = 'site:linkedin.com/in/'

    if location_inputs:
        for i, location in enumerate(location_inputs):
            if i == 0:
                base_query += ' AND ('
                base_query += location.strip()
            else:
                base_query += ' OR ' + location.strip()
        base_query += ')'

    if niche_inputs:
        for i, niche in enumerate(niche_inputs):
            if i == 0:
                base_query += ' AND ('
                base_query += niche.strip()
            else:
                base_query += ' OR ' + niche.strip()
        base_query += ')'

    if position_inputs:
        for i, position in enumerate(position_inputs):
            if i == 0:
                base_query += ' AND ('
                base_query += position.strip()
            else:
                base_query += ' OR ' + position.strip()
        base_query += ')'

    if other_inputs:
        for i, other in enumerate(other_inputs):
            if i == 0:
                base_query += ' AND ('
                base_query += other.strip()
            else:
                base_query += ' OR ' + other.strip()
        base_query += ')'

    return base_query


writer = csv.writer(open('output.csv', 'w', encoding='utf-8'))
writer.writerow(['Name', 'URL', 'Email', 'Headline'])


location_inputs = []
niche_inputs = []
position_inputs = []
other_inputs = []

while True:
    input_keyword = input(
        '\nEnter the keyword for location (or type "continue" to go forward): ')

    if input_keyword == 'continue':
        break
    location_inputs.append(input_keyword)

while True:
    input_keyword = input(
        '\nEnter the keyword for niche (or type "continue" to go forward): ')

    if input_keyword == 'continue':
        break
    niche_inputs.append(input_keyword)

while True:
    input_keyword = input(
        '\nEnter the keyword for position (or type "continue" to go forward): ')

    if input_keyword == 'continue':
        break
    position_inputs.append(input_keyword)

while True:
    input_keyword = input(
        '\nEnter the keyword for other (or type "search" to start the script): ')

    if input_keyword == 'search':
        break
    other_inputs.append(input_keyword)


query = build_query(location_inputs, niche_inputs,
                    position_inputs, other_inputs)

print(f'Query: {query}')

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

urls = []
# Collect the URLs from query result
for i in range(10):
    search_input = driver.find_element_by_name('q')

    search_input.send_keys(query)

    search_input.send_keys(Keys.RETURN)
    sleep(1)

    profiles_list = driver.find_elements_by_xpath('//div[@class="yuRUbf"]/a')
    profiles_list = [profile.get_attribute(
        'href') for profile in profiles_list]
    urls.append(profiles_list)

    sleep(1)
    driver.find_element_by_xpath('//a[@id="pnnext"]').click()

flatten_urls = [item for sublist in urls for item in sublist]

for profile in flatten_urls:
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
