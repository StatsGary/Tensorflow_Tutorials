#Selenium helps you use this executable to automate Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from datetime import datetime as dt
from PIL import Image
import time
import os

# Download the driver from chromedriver website for relevant OS i.e. MAC, Windows, Debian, etc.
PATH = 'C:/Users/garyh/Documents/GitHub/Tensorflow_Tutorials/01_CV_Classification/chromedriver/chromedriver.exe'
wd = webdriver.Chrome(executable_path=PATH)


def get_images_from_google(wd, delay, max_images, url):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = url
	wd.get(url)

	image_urls = set()
	skips = 0
	while len(image_urls) + skips < max_images:
		scroll_down(wd)
		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					##print(f"Found {len(image_urls)}")

	return image_urls


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



if __name__ == '__main__':
    # Google search URLS
    google_urls = ['https://www.google.com/search?q=lewis+grabban&rlz=1C1CHBF_en-GBGB924GB924&sxsrf=ALiCzsZYqtC0Dr5X-fqi3qg8rqxDuI87HQ:1651752199175&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiku9q4qMj3AhUdQ0EAHa5gBkgQ_AUoAnoECAEQBA&biw=2048&bih=1004&dpr=0.94#imgrc=rRrRxw8wQ7YxWM',
                  'https://www.google.com/search?q=philip+zinckernagel&tbm=isch&ved=2ahUKEwiWwcmwzcj3AhUN0oUKHYmmCwUQ2-cCegQIABAA&oq=philipzin&gs_lcp=CgNpbWcQARgAMgYIABAKEBg6BwgjEO8DECc6BQgAEIAEOgYIABAFEB46BAgAEB5QsRBYiRRgpSNoAHAAeACAATqIAdwBkgEBNJgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=wuNzYpbYDY2klwSJza4o&bih=1004&biw=2048&rlz=1C1CHBF_en-GBGB924GB924',
                  'https://www.google.com/search?rlz=1C1CHBF_en-GBGB924GB924&sxsrf=ALiCzsbdBXzzbO-rUCgRzokBwQ3ieCg4kQ:1651763782663&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj-zJLM08j3AhWRi1wKHWriAEUQ_AUoAXoECAIQAw&q=Brennan%20Johnson&lei=SepzYuD4HdTC8gK28IPYCg&biw=1920&bih=969&dpr=1']
    
    # Labels for the players
    labels = ['lewis_grabban', 'philip_zinckernagel', 'brennan_johnson']
    player_path = 'images/train/'
    # Make the directory if it doesn't exist
    for lbl in labels:
        # Start afresh

        if os.path.exists(player_path + lbl):
            print(f'Removing detritus directory: {str(lbl)}')
            os.rmdir(player_path+lbl)

        if not os.path.exists(player_path + lbl):
            print(f'Making directory: {str(lbl)}')
            os.makedirs(player_path+lbl)

    for url_current, lbl in zip(google_urls, labels):
        urls = get_images_from_google(wd, 0, 100, url_current)
        # Once we have added our urls to empty set then 
        for i, url in enumerate(urls):
            download_image(down_path=f'images/train/{lbl}/', 
                        url=url, 
                        file_name=str(i+1)+ '.jpg',
                        verbose=True) 
    wd.quit()

