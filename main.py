import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "C:\\Users\\Shaharabanu's\\Application\\chromedriver.exe"
services = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=services)

# Creating a new output csv file
with open("D:/PycharmProjects/task_analyst.ai/output.csv", 'w', newline='') as new_file:
    # creating a csv writer object
    writer = csv.writer(new_file)
    fields = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of reviews', 'Description', 'ASIN',
              'Product Description', 'Manufacturer']
    writer.writerow(fields)

       ########################3######## Part 1 #################################
driver.maximize_window()
driver.get("https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1/")
no_of_page = 1

while no_of_page < 21:
    # Product sections
    print(no_of_page)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.sg-col-20-of-24.s-result-item.s-asin.sg-col-0-of-12.sg-col-16-of-20.sg-col.s-widget-spacing-small.sg-col-12-of-16")))
    time.sleep(10)
    product_divs = driver.find_elements(by=By.CSS_SELECTOR, value="div.sg-col-20-of-24.s-result-item.s-asin.sg-col-0-of-12.sg-col-16-of-20.sg-col.s-widget-spacing-small.sg-col-12-of-16")
    print(len(product_divs))
    links_array = []
    product_names_array = []
    price_array = []
    rating_array = []
    no_of_reviews_array = []

    for product_div in product_divs:
        # Product URL
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h2.a-size-mini  a")))
        product_link = product_div.find_element(by=By.CSS_SELECTOR, value="h2.a-size-mini  a").get_attribute("href")
        links_array.append(product_link)

        # Product Name
        product_name = product_div.find_element(by=By.CSS_SELECTOR, value="h2.a-size-mini  span").text
        print(product_name)
        product_names_array.append(product_name)

        # Price
        try:
            price_a = product_div.find_element(by=By.CSS_SELECTOR, value="a.a-size-base.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")
            price = price_a.find_element(by=By.CSS_SELECTOR, value="span span.a-price-whole").text
        except NoSuchElementException:
            price = product_div.find_element(by=By.CSS_SELECTOR, value="span span.a-price-whole").text
        price_array.append(price)

        # Rating
        try:
            ratings_div = product_div.find_element(by=By.CSS_SELECTOR, value="div.a-row.a-size-small")
            spans = ratings_div.find_elements(by=By.CSS_SELECTOR, value="span")
            rating = spans[0].get_attribute('aria-label')
        except NoSuchElementException:
            rating = ''
        rating_array.append(rating)

        # Reviews
        try:
            reviews = product_div.find_element(by=By.CSS_SELECTOR, value="a span.a-size-base.s-underline-text").text
            print(reviews)
        except NoSuchElementException:
            reviews = ''
        no_of_reviews_array.append(reviews)

                ########################## Part 2 ##############################

    # Hitting each product_link and obtaining the information
    description_array = []
    asin_array = []
    manufacturer_array = []
    prod_description_array = []
    for product in links_array:
        driver.get(product)

        # Description
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
             (By.ID, "feature-bullets")))
        description_list = driver.find_element(by=By.ID, value="feature-bullets")
        description_items = description_list.find_elements(by=By.TAG_NAME, value="li")
        description = ''
        for ele in description_items:
            item = ele.text
            description = description + item + ', '
        description_array.append(description)

        prod_description = ''
        asin = ''
        manufacturer = ''
        # Product Description
        try:
            details_list = driver.find_element(by=By.ID, value="detailBullets_feature_div")
        except NoSuchElementException:
            table = driver.find_element(by=By.ID, value="prodDetails")
            table_values = table.find_elements(by=By.TAG_NAME, value="tr")
            for ele in table_values:
                item = ele.find_element(by=By.TAG_NAME, value="th").text + " : " + \
                       ele.find_element(by=By.TAG_NAME, value="td").text
                prod_description = prod_description + item + '\n'

                # ASIN
                if ele.find_element(by=By.TAG_NAME, value="th").text == 'ASIN':
                    asin = 'ASIN : ' + ele.find_element(by=By.TAG_NAME, value="td").text

                # Manufacturer
                if ele.find_element(by=By.TAG_NAME, value="th").text == 'Manufacturer':
                    manufacturer = 'Manufacturer : ' + ele.find_element(by=By.TAG_NAME, value="td").text

        else:
            details_items = details_list.find_elements(by=By.TAG_NAME, value="li")
            for ele in details_items:
                item = ele.text
                prod_description = prod_description + item + ', '

                # ASIN
                if ele.find_element(by=By.CSS_SELECTOR, value="span.a-text-bold").text == "ASIN :":
                    asin = ele.text

                # Manufacturer
                if ele.find_element(by=By.CSS_SELECTOR, value="span.a-text-bold").text == "Manufacturer :":
                    manufacturer = ele.text
        prod_description_array.append(description)
        asin_array.append(asin)
        manufacturer_array.append(manufacturer)

        driver.back()

    # Writing to the csv file
    with open("D:/PycharmProjects/task_analyst.ai/output.csv", 'a', newline='') as new_file:
        writer = csv.writer(new_file)
        for i in range(len(links_array)):
            datarows = [[links_array[i], product_names_array[i], price_array[i], rating_array[i], no_of_reviews_array[i], description_array[i], asin_array[i],
                             prod_description_array[i], manufacturer_array[i]],]
            try:
                writer.writerows(datarows)
            except UnicodeEncodeError:
                pass

    # Clicking on the next page
    if no_of_page != 20:
        next_button = driver.find_element(by=By.LINK_TEXT, value="Next")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(next_button))
        next_button.click()
        no_of_page += 1

