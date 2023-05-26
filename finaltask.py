import requests
import re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time as t
import json
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
mega_link = []


def write_to_file(data):
    file_name = "data\data9.json"

    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            existing_list = json.load(f)
        existing_list.extend(data)
        if len(existing_list) > 0:
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(existing_list, f, indent=4, separators=(',', ':'))
        else:
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, separators=(',', ':'))
    except FileNotFoundError:
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, separators=(',', ':'))


def extract_all(url):
    data = []
    # url=driver.current_url
    driver.get(url)
    t.sleep(4)
    html = driver.page_source
    soup = bs(html, "html.parser")
    titles = soup.find_all('div', {
        'class': 'sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col-12-of-24 s-list-col-right'})

    for i in titles:
        try:
            name = i.find(
                'span', {'class': 'a-size-medium a-color-base a-text-normal'}).text
            link = i.find('a', {
                'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
            # link = i.find_element(
            #     By.XPATH, "//div[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")
            ans = link.get('href')
            price = i.find(
                'span', {'class': 'a-price-whole'}).text
            rating = i.find('span', {'class': 'a-icon-alt'})
            if rating is not None:
                rating = rating.text
            else:
                rating = 'None'
            no_of_rating = i.find(
                'span', {'class': 'a-size-base s-underline-text'})
            if no_of_rating is not None:
                no_of_rating = no_of_rating.text
            else:
                no_of_rating = 'None'
            d = {"Product URL": f'https://www.amazon.in{ans}', "Product Name": name,
                 "Product Price": price, "Rating": rating, "Number of Reviews": no_of_rating}
            mega_link.append(f'https://www.amazon.in{ans}')
            driver.get(url)
            data.append(d)
        except Exception as e:
            print(e)
    write_to_file(data=data)


url5 = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%252+C283&ref=sr_pg_1"
driver = webdriver.Chrome('chromedriver')
driver.maximize_window()
driver.get(url5)

t.sleep(4)
html = driver.page_source
# print(html)
soup = bs(html, "html.parser")

titles = soup.find_all('div', {
                       'class': 'sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col-12-of-24 s-list-col-right'})
data = []  # stores data before writing
for i in titles:
    try:
        name = i.find(
            'span', {'class': 'a-size-medium a-color-base a-text-normal'}).text
        link = i.find('a', {
            'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        # link = i.find_element(
        #     By.XPATH, "//div[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")
        ans = link.get('href')
        price = i.find(
            'span', {'class': 'a-price-whole'}).text
        rating = i.find('span', {'class': 'a-icon-alt'})
        if rating is not None:
            rating = rating.text
        else:
            rating = 'None'
        no_of_rating = i.find(
            'span', {'class': 'a-size-base s-underline-text'})
        if no_of_rating is not None:
            no_of_rating = no_of_rating.text
        else:
            no_of_rating = 'None'
        d = {"Product URL": f'https://www.amazon.in{ans}', "Product Name": name,
             "Product Price": price, "Rating": rating, "Number of Reviews": no_of_rating}
        data.append(d)
        mega_link.append(f'https://www.amazon.in{ans}')
    except Exception as e:
        print(e)
write_to_file(data=data)


for i in range(1, 19):
    try:
        next_pg = driver.find_element(By.PARTIAL_LINK_TEXT, 'Next')
        next_pg.click()
        url = driver.current_url
        extract_all(url)
        t.sleep(4)
    except Exception as e:
        print("ERROR OCCURED!")
        t.sleep(10)
        ip = input("Enter y to quit an n to not ?  = > :")
        if ip == 'y':
            break
        print(driver.current_url)
t.sleep(10)
file_path = "links.txt"

# Open the file in write mode
with open(file_path, "w") as file:
    # Write each link to a new line in the file
    for link in mega_link:
        file.write(link + "\n")

print("Links saved to file:", file_path)
for i in mega_link:
    driver.get(i)
    t.sleep(4)
    try:
        discription = driver.find_element(
            By.XPATH, "//ul[@class='a-unordered-list a-vertical a-spacing-mini']").text
    except:
        pass
    manufacturer = []
    ASIN = []
    product_discription = []
    try:
        manufacturer_element = driver.find_element(
            By.XPATH, '//div[@id="detailBullets_feature_div"]//span[@class="a-list-item"][3]')
        manufacturer.append(manufacturer_element.text.strip())

    except:
        pass
    try:
        asin_element = driver.find_element(
            By.XPATH, '//div[@id="detailBullets_feature_div"]//li/span[contains(.,"ASIN")]/span[2]')
        ASIN.append(asin_element.text.strip())
    except:
        pass
    if(len(ASIN) == 0):
        try:
            asin_element = driver.find_element(
                By.XPATH, '//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(text(), "ASIN")]/following-sibling::td[1]')
            ASIN.append(asin_element.text.strip())
        except:
            pass

    if(len(manufacturer) == 0):
        try:
            mau1 = driver.find_element(
                By.XPATH, '//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(text(), "Manufacturer")]/following-sibling::td[1]')

            manufacturer.append(mau1.text.strip().replace("\u200e", ""))
        except:
            pass
    try:
        product_discr = driver.find_elements(
            By.XPATH, "//h3[@class='a-spacing-mini']")
        droduct_more = driver.find_elements(
            By.XPATH, "//p[@class='a-spacing-base']")
    except:
        pass
    for i in range(len(product_discr)):
        product_discription.append(product_discr[i].text)

    if(len(product_discription) == 0):
        try:
            description_element = driver.find_element(
                By.XPATH, '//div[@id="productDescription"]//span')
            product_discription.append(description_element.text.strip())
        except:
            pass


try:

    data = {
        "Discription": discription,
        "Manufacturer": manufacturer,
        "ASIN": ASIN,
        "Product Discription": product_discription
    }

except Exception as e:
    pass

with open("task2.json", "w") as f:
    json.dump(data, f, indent=4)

t.sleep(2)
print("all done")

driver.close()
driver.quit()
