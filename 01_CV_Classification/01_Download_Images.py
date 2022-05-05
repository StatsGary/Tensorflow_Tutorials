#Selenium helps you use this executable to automate Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from datetime import datetime as dt
from PIL import Image
import time

# Download the driver from chromedriver website for relevant OS i.e. MAC, Windows, Debian, etc.
PATH = 'C:/Users/garyh/Documents/GitHub/Tensorflow_Tutorials/01_CV_Classification/chromedriver/chromedriver.exe'
wd = webdriver.Chrome(PATH)


def get_google_images(wd, delay, max_images, url):
    def scroll_down(wd):
        wd.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(delay)

    url = url
    wd.get(url)

    image_urls = set()
    while len(image_urls) < max_images:
        scroll_down(wd)
        thumbnails = wd.find_elements(By.CLASS_NAME, 'Q4LuWd')
        # Loop through urls until at max images
        for img in thumbnails[len(image_urls): max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, 'n3VNCb')

            # Get the larger image, as we are dealing with URLS at the moment






def download_image(down_path, url, file_name, image_type='JPEG',
                   verbose=True):
    try:
        time = dt.now()
        curr_time = time.strftime('%H:%M:%S')
        #Content of the image will be a url
        img_content = requests.get(url).content
        #Get the bytes IO of the image
        img_file = io.BytesIO(img_content)
        #Stores the file in memory and convert to image file using Pillow
        image = Image.open(img_file)
        file_pth = down_path + file_name

        with open(file_pth, 'wb') as file:
            image.save(file, image_type)

        if verbose == True:
            print(f'The image: {file_pth} downloaded successfully at {curr_time}.')
    except Exception as e:
        print(f'Unable to download image from Google Photos due to\n: {str(e)}')

url = 'https://www.google.com/search?q=lewis+grabban&rlz=1C1CHBF_en-GBGB924GB924&sxsrf=ALiCzsZYqtC0Dr5X-fqi3qg8rqxDuI87HQ:1651752199175&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiku9q4qMj3AhUdQ0EAHa5gBkgQ_AUoAnoECAEQBA&biw=2048&bih=1004&dpr=0.94#imgrc=rRrRxw8wQ7YxWM'
get_google_images(wd, 2, 10, url)