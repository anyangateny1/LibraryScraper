from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def scrapeLibrary(bookName):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("window-size=1920,1080")
    options.add_experimental_option(

        "prefs", {"profile.managed_default_content_settings.images": 2}
    )

    driver = webdriver.Chrome(options=options)
    driver.get("https://onecard.network/client/en_AU/playford/")
    driver.implicitly_wait(5)

    ActionChains(driver).send_keys(bookName, Keys.ENTER).perform()
    driver.implicitly_wait(5)

    restrictToBooks = driver.find_elements(By.LINK_TEXT, "Books")
    
    if restrictToBooks:
        restrictToBooks = driver.find_element(By.LINK_TEXT, "Books").click()
    else:
        driver.close()
        return {"error": f"{bookName} does not exist as a book."}

    column1 = driver.find_element(By.ID, "results_cell0")
    bookTitle = column1.find_element(By.CLASS_NAME, "displayDetailLink").text

    if bookName.lower() in bookTitle.lower():
        bookPicture = driver.find_elements(By.CLASS_NAME, "stupid_ie_div")
        if bookPicture:
            driver.find_element(By.CLASS_NAME, "stupid_ie_div").click()
        else:
            driver.close()
            return {"error": "Book title does not match any books in SA Libraries."}
    else:
        driver.close()
        return {"error": "Book title does not match any books in SA Libraries."}

    driver.implicitly_wait(100)
    area = driver.find_element(By.ID, "tabs-1")
    location = area.find_element(By.CLASS_NAME, "asyncFieldLIBRARY").text
    status = area.find_element(By.CLASS_NAME, "asyncFieldSD_ITEM_STATUS").text

    driver.close()
    
    return {"title": bookTitle, "location": location, "status": status}
