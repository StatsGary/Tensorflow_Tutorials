#Selenium helps you use this executable to automate Chrome
from multiprocessing.sharedctypes import Value
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
    google_urls = [
                   'https://www.google.com/search?q=brice+samba&tbm=isch&ved=2ahUKEwinwYCZ3cj3AhVOyRoKHVjuC5UQ2-cCegQIABAA&oq=brice+samba&gs_lcp=CgNpbWcQAzIHCCMQ7wMQJzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBAgAEB4yBAgAEBgyBAgAEBgyBAgAEBgyBAgAEBg6CAgAELEDEIMBOggIABCABBCxAzoHCAAQsQMQQzoECAAQQzoECAAQAzoGCAAQCBAeULQIWOYXYP4ZaABwAHgAgAFKiAGBBpIBAjEymAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=V_RzYue5Ls6Sa9jcr6gJ&bih=969&biw=1920&rlz=1C1CHBF_en-GBGB924GB924',
                   'https://www.google.com/search?q=keinan+davis+footballer&tbm=isch&ved=2ahUKEwjn7dqj3cj3AhUBdBoKHXxWCAMQ2-cCegQIABAA&oq=keinan+davis+footballer&gs_lcp=CgNpbWcQAzIECAAQGDoHCCMQ7wMQJzoFCAAQgAQ6BAgAEB46CAgAELEDEIMBOgsIABCABBCxAxCDAToICAAQgAQQsQM6BAgAEEM6BwgAELEDEEM6BggAEAUQHjoGCAAQCBAeUO8JWO4qYOAraABwAHgAgAFViAH8C5IBAjI0mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=bvRzYuf-DIHoafysoRg&bih=969&biw=1920&rlz=1C1CHBF_en-GBGB924GB924',
                   'https://www.google.com/search?q=ethan+horvath+football&tbm=isch&ved=2ahUKEwixt9HN3cj3AhVJ3RoKHdoiAeoQ2-cCegQIABAA&oq=ethan+horvath+football&gs_lcp=CgNpbWcQAzoHCCMQ7wMQJzoECAAQQzoFCAAQgAQ6BAgAEB46BAgAEBhQiQRYgQ9gxRBoAHAAeACAAVeIAeUEkgECMTCYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=xvRzYrG8CMm6a9rFhNAO&bih=969&biw=1920&rlz=1C1CHBF_en-GBGB924GB924',
                   'https://www.google.com/search?q=steve+cook+forest&tbm=isch&ved=2ahUKEwiXipXR3cj3AhVKexoKHYg2BjcQ2-cCegQIABAA&oq=steve+cook+&gs_lcp=CgNpbWcQARgAMgcIIxDvAxAnMgQIABADMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6CAgAEIAEELEDOggIABCxAxCDAToECAAQQzoLCAAQgAQQsQMQgwFQ3gZYhhJgkSJoAHAAeACAAbMBiAGFB5IBBDExLjGYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=zfRzYtfvIMr2aYjtmLgD&bih=969&biw=1920&rlz=1C1CHBF_en-GBGB924GB924',
                   'https://www.google.com/search?q=joe+worrall&tbm=isch&ved=2ahUKEwiLhJna3cj3AhXW44UKHYvcCjIQ2-cCegQIABAA&oq=joe+worrall&gs_lcp=CgNpbWcQAzIHCCMQ7wMQJzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBAgAEEMyBQgAEIAEMgUIABCABDIECAAQGDIECAAQGDoICAAQsQMQgwE6CwgAEIAEELEDEIMBOggIABCABBCxAzoKCAAQsQMQgwEQQzoHCAAQsQMQQ1DcZ1jXdWDPeWgBcAB4AIABkAGIAY8HkgEEMTEuMZgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=4PRzYouUHdbHlwSLuauQAw&bih=969&biw=1920&rlz=1C1CHBF_en-GBGB924GB924',
                   'https://www.google.com/search?q=ryan+yates&tbm=isch&ved=2ahUKEwje3vni3cj3AhXa0oUKHfW4D5kQ2-cCegQIABAA&oq=ryan+yates&gs_lcp=CgNpbWcQAzIHCCMQ7wMQJzIFCAAQgAQyBQgAEIAEMgYIABAFEB4yBAgAEBgyBAgAEBgyBAgAEBgyBAgAEBgyBAgAEBgyBAgAEBg6BAgAEEM6CAgAELEDEIMBOgsIABCABBCxAxCDAToICAAQgAQQsQM6CggjEO8DEOoCECc6CggAELEDEIMBEEM6BwgAELEDEENQpghYlBdgwxhoAXAAeACAAViIAbgGkgECMTKYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCsABAQ&sclient=img&ei=8vRzYt6dM9qllwT18b7ICQ&bih=969&biw=1920&rlz=1C1CHBF_en-GBGB924GB924',
                   'https://www.google.com/search?q=jack+colback+footballer&tbm=isch&ved=2ahUKEwiGi83s3cj3AhUDpBoKHTQKDzcQ2-cCegQIABAA&oq=jack+colback+footballer&gs_lcp=CgNpbWcQAzIECAAQGDoHCCMQ7wMQJzoFCAAQgAQ6BggAEAcQHjoECAAQQzoICAAQsQMQgwE6CwgAEIAEELEDEIMBOggIABCABBCxAzoGCAAQBRAeOgQIABAeOgYIABAIEB5QowhY0iRgpSVoAHAAeACAAZgBiAGxDZIBBDIzLjGYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=B_VzYsbrBIPIarSUvLgD&bih=969&biw=1920&rlz=1C1CHBF_en-GBGB924GB924',
                   'https://www.google.com/search?q=scott+mckenna&tbm=isch&ved=2ahUKEwj-mJD53cj3AhUQQhoKHQpnDfMQ2-cCegQIABAA&oq=scott+&gs_lcp=CgNpbWcQARgAMgcIIxDvAxAnMgQIABBDMgcIABCxAxBDMgQIABBDMgQIABBDMgcIABCxAxBDMggIABCxAxCDATILCAAQgAQQsQMQgwEyCAgAEIAEELEDMgsIABCABBCxAxCDAToECAAQAzoFCAAQgARQ6QRYwgtghxZoAHAAeACAAUuIAd0DkgEBN5gBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=IfVzYr6EFZCEaYrOtZgP&bih=969&biw=1920&rlz=1C1CHBF_en-GBGB924GB924',
                   'https://www.google.com/search?q=cafu+forest&tbm=isch&ved=2ahUKEwi7xdeN3sj3AhUE4hoKHcHTCO8Q2-cCegQIABAA&oq=cafu+forest&gs_lcp=CgNpbWcQAzIFCAAQgAQyBggAEAgQHjoECAAQQzoECAAQHjoECAAQGFAAWKIHYKUJaABwAHgAgAFZiAHSA5IBATeYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=TPVzYrvvG4TEa8Gno_gO&bih=969&biw=1920&rlz=1C1CHBF_en-GBGB924GB924',
                   'https://www.google.com/search?q=max+lowe+footballer&tbm=isch&ved=2ahUKEwjpj4aQ3sj3AhUL_BoKHSF6CmwQ2-cCegQIABAA&oq=max+lowe+footballer&gs_lcp=CgNpbWcQAzIECAAQGDoHCCMQ7wMQJzoGCAAQCBAeOgsIABCABBCxAxCDAToFCAAQgAQ6BAgAEAM6CAgAELEDEIMBOggIABCABBCxAzoECAAQQzoHCAAQsQMQQzoGCAAQBRAeOgQIABAeUKMIWLsiYJgjaABwAHgAgAGdAYgB9wqSAQQxOS4xmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=UfVzYqmjGYv4a6H0qeAG&bih=969&biw=1920&rlz=1C1CHBF_en-GBGB924GB924',
                   'https://www.google.com/search?q=joe+lolley&rlz=1C1CHBF_en-GBGB924GB924&hl=en&sxsrf=ALiCzsYdA_zTQwIGhtfmL__WXkmGyvR7aQ:1651766657726&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjduIqn3sj3AhULJMAKHZ8hCoYQ_AUoAnoECAEQBA&biw=1920&bih=969&dpr=1',
                   'https://www.google.com/search?q=alex+mighten&tbm=isch&ved=2ahUKEwi73fyn3sj3AhUD-4UKHSjyBpAQ2-cCegQIABAA&oq=alex&gs_lcp=CgNpbWcQARgAMgcIIxDvAxAnMgcIIxDvAxAnMgoIABCxAxCDARBDMgQIABBDMgQIABBDMgQIABBDMggIABCABBCxAzIECAAQQzIICAAQgAQQsQMyCAgAEIAEELEDOgUIABCABDoECAAQGDoLCAAQgAQQsQMQgwE6CAgAELEDEIMBOgcIABCxAxBDUKIHWJwLYLwUaABwAHgAgAFLiAHIApIBATWYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=g_VzYvuPJIP2lwSo5JuACQ&bih=969&biw=1920&rlz=1C1CHBF_en-GBGB924GB924&hl=en'
    ]
    
    # Labels for the players
    labels = [
        'brice_samba','keinan_davis', 'ethan_horvath', 'steve_cook', 'joe_worrall',
        'ryan_yates', 'jack_colback', 'scott_mckenna', 'cafu', 'max_lowe',
        'joe_lolley', 'alex_mighten'
    ]

    # Check the length of the lists
    if len(google_urls) != len(labels):
        raise ValueError('The length of the url list does not match the labels list.')

    player_path = 'images/nottingham_forest/'
    # Make the directory if it doesn't exist
    for lbl in labels:
        if not os.path.exists(player_path + lbl):
            print(f'Making directory: {str(lbl)}')
            os.makedirs(player_path+lbl)

    for url_current, lbl in zip(google_urls, labels):
        urls = get_images_from_google(wd, 0, 100, url_current)
        # Once we have added our urls to empty set then 
        for i, url in enumerate(urls):
            download_image(down_path=f'images/nottingham_forest/{lbl}/', 
                        url=url, 
                        file_name=str(i+1)+ '.jpg',
                        verbose=True) 
    wd.quit()

