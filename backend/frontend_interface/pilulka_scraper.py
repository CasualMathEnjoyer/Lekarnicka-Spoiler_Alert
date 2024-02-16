from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# This script takes EAN code and tries to find in the database of pilulka


try:
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)

    url = 'https://www.pilulka.cz/'
    driver.get(url)
except Exception as e:
    print(f"Failed to get the driver : {e}")

def get_name_from_EAN(EAN=str()):
    try:
        box = driver.find_element(By.TAG_NAME, "input")
        box.send_keys(EAN)
        box.send_keys(Keys.RETURN)
        driver.implicitly_wait(0.1)

        drug = driver.find_element(By.CLASS_NAME, "product__name")
        name = drug.get_attribute("title")
        print(name)
        return name
    except Exception as e:
        print(f"Exception occured: {e}")
        return None

if __name__ == "__main__":
    get_name_from_EAN('5099151006554')