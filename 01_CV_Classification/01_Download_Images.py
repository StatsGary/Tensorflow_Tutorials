#Selenium helps you use this executable to automate Chrome
from selenium import webdriver
import requests
import io
from PIL import Image
PATH = 'C:/Users/garyh/Documents/GitHub/Tensorflow_Tutorials/01_CV_Classification/chromedriver/chromedriver.exe'
wd = webdriver.Chrome(PATH)
# This bit controls chrome
img_url = 'https://i2-prod.nottinghampost.com/incoming/article2613604.ece/ALTERNATES/s1200c/0_Nottingham-Forest-striker-Lewis-Grabban-in-action-against-Preston-North-End.jpg'

def download_image(down_path, url, file_name, image_type='JPEG',
                   verbose=True):
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
        print('Hell yeah!')


#Use function 
download_image("", img_url, 'test.jpg')

    

