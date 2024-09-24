from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from urllib.parse import quote_plus
import os
from helper_func import download_image
from pathlib import Path

def download_google_images(query:str, download_folder:str, quantity: int) -> int:
    
    total_downloaded_images = 0
    
    # Making Search Query
    search_query = quote_plus(query)
    Google_Search_URL = f"https://www.google.com/search?q={search_query}&udm=2"
    
    # Making Download Folder Ready
    try:
        if not os.path.exists(download_folder):
            os.mkdir(download_folder)
    except:
        print(f"Couldn't open Download Folder({download_folder})")
        return 0
    
    # Making Quantity Ready
    if quantity > 300:
        quantity = 300
    
    # Setting up Chrome Driver
    options = ChromeOptions()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(Google_Search_URL)
    
    # Downloading Images One by One
    for i in range(1, quantity + 1):
        
        try:
            div = driver.find_element(By.XPATH, f'//*[@id="rso"]/div/div/div[1]/div/div/div[{i}]')
        except NoSuchElementException as e:
            print(f"Couldn't get image {i}")
            continue

        classes = div.get_attribute("class").split(" ")
        if "BA0zte" in classes:
            print(f"Couldn't get image {i}")
            continue 
        
        div.click()
        
        print(f"Image {i} Loading...")
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img[2]'))
            )
            print(f"Image {i} Loaded")
        except TimeoutException as e:
            print(f"Image {i} couldn't load. Downloading low quality image")
        
        try:
            img = driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img[1]')
        except NoSuchElementException as e:
            print(f"Could't get image {i}'s URL")
            continue
        res = download_image(img.get_attribute('src'), download_folder, i)
        
        if res:
            total_downloaded_images += 1
    
    driver.quit()
    
    return total_downloaded_images
    
if __name__ == '__main__':
    print("------ Welcome to Google Images Downloader by Maulik ------")
    while True:
        search_query = input("Enter Image Search Query (e to exit) : ")
        if search_query == 'e':
            break
        quantity = int(input("Enter Quantity (must be INT, max=300) : "))
        
        default_download_folder = os.path.join(
            str(Path.home()) , 
            "Downloads" ,
            search_query.replace(" ", "_") + f"_{quantity}_images"
        )
        
        download_folder = input(f"Enter download folder (blank to download in {default_download_folder}) : ")
        
        if not download_folder:
            download_folder = default_download_folder
                
        total_downloaded_images = download_google_images(search_query, download_folder, quantity)
        
        print("--------------------------------------------------------------------------------")
        print(f"{total_downloaded_images} Images downloaded to {download_folder}")
        print("--------------------------------------------------------------------------------")
    