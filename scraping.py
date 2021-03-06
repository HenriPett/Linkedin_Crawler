import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from parsel import Selector
import csv


def google_search_links(query):
    url = f"https://google-search3.p.rapidapi.com/api/v1/search/q={query}&num=100"

    headers = {
        "X-User-Agent": "desktop",
        "X-Proxy-Location": "EU",
        "X-RapidAPI-Host": "google-search3.p.rapidapi.com",
        "X-RapidAPI-Key": "0a68164619msh1832650cb7cdbd6p1d6bb4jsn84ef60bd80a6"
    }

    r = requests.request("GET", url, headers=headers)

    responses = r.json().get('results')

    links = [response.get('link') for response in responses]

    return links


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

    return base_query.replace(' ', '%20')


writer = csv.writer(open('output.csv', 'w', encoding='utf-8'))
writer.writerow(['Name', 'URL', 'Email', 'Headline'])


location_inputs = []
niche_inputs = []
position_inputs = []
other_inputs = []

linkedin_user = input(
    '\nEnter your LinkedIn user or e-mail: ')

linkedin_password = input(
    '\nEnter your LinkedIn password: ')

while True:
    input_keyword = input(
        '\nEnter the keyword for location (or type "continue" to go forward): ')

    if input_keyword == 'continue':
        break
    location_inputs.append(input_keyword.capitalize())

while True:
    input_keyword = input(
        '\nEnter the keyword for niche (or type "continue" to go forward): ')

    if input_keyword == 'continue':
        break
    niche_inputs.append(input_keyword.capitalize())

while True:
    input_keyword = input(
        '\nEnter the keyword for position (or type "continue" to go forward): ')

    if input_keyword == 'continue':
        break
    position_inputs.append(input_keyword.capitalize())

while True:
    input_keyword = input(
        '\nEnter the keyword for other (or type "search" to start the script): ')

    if input_keyword == 'search':
        break
    other_inputs.append(input_keyword.capitalize())


query = build_query(location_inputs, niche_inputs,
                    position_inputs, other_inputs)

print(f'Query: {query}')

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(1024, 600)
driver.maximize_window()
# LINKEDIN

# access LinkedIn
driver.get('https://www.linkedin.com/')
sleep(2)

# Log in to LinkedIn
driver.find_element_by_xpath('//*[@id="session_key"]').click()
sleep(2)

user_input = driver.find_element_by_name('session_key')
user_input.send_keys(linkedin_user)

sleep(2)
password_input = driver.find_element_by_name('session_password')
password_input.send_keys(linkedin_password)

password_input.send_keys(Keys.RETURN)

# GOOGLE

# Collect the URLs from query result
print('Collecting URLs...')
urls = google_search_links(query)
print('Done!')

for profile in urls:
    try:
        print(f'Collectinig data from {profile}')

        driver.get(profile)

        response = Selector(text=driver.page_source)

        name = response.xpath('//title/text()').extract_first().split(" | ")[0]
        headline = driver.find_element_by_xpath(
            '//div[@class="text-body-medium break-words"]').text
        url_profile = driver.current_url

        sleep(5)

        driver.find_element_by_xpath(
            '//*[@id="top-card-text-details-contact-info"]').click()
        sleep(5)

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
