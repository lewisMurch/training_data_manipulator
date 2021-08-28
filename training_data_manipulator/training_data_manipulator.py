#Created by Lewis Murch
import os
import os.path
import numpy as np
from matplotlib import image
from matplotlib import pyplot
import cv2
from PIL import Image, ImageFile, ImageDraw, ImageChops, ImageFilter, ImageEnhance


def greyscale(path, save_path):
    image = Image.open(path) #Load the image
    gs_image = image.convert(mode='L') #Convert the image to greyscale
    gs_image.save(save_path, format='jpeg') #Save the image
    #greyscale() ##example use case
    pass

def resize_aspect_preserved(size_chosen, path, save_path):
    image = Image.open(path) #Load the image
    resized_image = image.thumbnail((size_chosen, size_chosen)) #Resize the image
    image.save(save_path, format='jpeg')

    #resize_aspect_preserved(300) ##example use case
    pass

def resize_aspect_not_preserved(size_x_chosen, size_y_chosen, path, save_path):
    image = Image.open(path) #Load the image
    resized_image = image.resize((size_x_chosen, size_y_chosen)) #Resize the image
    resized_image.save(save_path, format='jpeg')

    #resize_aspect_not_preserved(43, 944) ##example use case
    pass

def flip(vertical, path, save_path):
    image = Image.open(path) #Load the image
    if vertical == False:
        hoz_flip = image.transpose(Image.FLIP_LEFT_RIGHT)
        hoz_flip.save(save_path, format='jpeg') #Saves the image
        #pyplot.imshow(hoz_flip)

    else:
        ver_flip = image.transpose(Image.FLIP_TOP_BOTTOM)
        ver_flip.save(save_path, format='jpeg')
        #pyplot.imshow(ver_flip)

    
    #pyplot.show()

    #flip(True) ##example use case
    pass

def rotate(amount, clockwise, path, save_path): #clockwise is bool, allow up to 360 degrees
    image = Image.open(path) #Load the image
    if clockwise == True:
        image_rotated = image.rotate(-amount)
        pyplot.imshow(image_rotated)
        image_rotated.save(save_path, format='jpeg') #Saves the image
    else:
        image_rotated = image.rotate(amount)
        pyplot.imshow(image_rotated)
        save_image = save(save_path, format='jpeg') #Saves the image
        image_rotated.save(save_path, format='jpeg') #Saves the image

    #rotate(45, False) ##example use case
    pass 

def crop(percent_cropped, path, save_path): #input as coords. cannot accept 100 or above!
    percent_cropped /= 2
    image = Image.open(path) #Load the image
    x=image.size[0]
    y=image.size[1]
    x_use = int(x/100 * percent_cropped)
    y_use = int(y/100 * percent_cropped)
    cropped = image.crop((x_use, y_use, x - x_use, y - y_use))
    cropped.save(save_path, format='jpeg') 
    
def blur(radius, path, save_path):
    image = Image.open(path) #Load the image
    blur_image = image.filter(ImageFilter.BoxBlur(radius))
    blur_image.save(save_path, format='jpeg') 

def gaussian_blur(radius, path, save_path):
    image = Image.open(path) #Load the image
    gauss_image = image.filter(ImageFilter.GaussianBlur(5))
    gauss_image.save(save_path, format='jpeg') 

def brightness(percent_brightness, path, save_path): 
    percent_brightness /= 100
    image = Image.open(path) #Load the image
    enhancer = ImageEnhance.Brightness(image)
    bright_image = enhancer.enhance(percent_brightness)
    bright_image.save(save_path, format='jpeg') 

def contrast(percent_contrast, path, save_path): 
    percent_contrast /= 100
    image = Image.open(path) #Load the image
    enhancer = ImageEnhance.Contrast(image)
    contrast_image = enhancer.enhance(percent_contrast)
    contrast_image.save(save_path, format='jpeg') 

def sharpness(percent_sharpness, path, save_path): 
    percent_sharpness /= 100
    image = Image.open(path) #Load the image
    enhancer = ImageEnhance.Sharpness(image)
    sharpness_image = enhancer.enhance(percent_sharpness)
    sharpness_image.save(save_path, format='jpeg') 

def colour(percent_colour, path, save_path): 
    percent_colour /= 100
    image = Image.open(path) #Load the image
    enhancer = ImageEnhance.Color(image)
    sharpness_image = enhancer.enhance(percent_colour)
    sharpness_image.save(save_path, format='jpeg') 

def gauss_noise(percent_noise, path, save_path): 
    percent_noise /= 200
    image = Image.open(path)
    image = np.asarray(image)
    row,col,ch= image.shape
    mean = 0
    var = percent_noise
    sigma = var**0.5
    gauss = np.random.normal(mean,sigma,(row,col,ch))
    gauss = gauss.reshape(row,col,ch)
    noisy = image + image * gauss 
    image = Image.fromarray((noisy).astype(np.uint8))
    image.save(save_path, format='jpeg')

def s_and_p_noise(percent_noise, path, save_path):
    percent_noise /= 200
    image = Image.open(path)
    image = np.asarray(image)
    row,col,ch = image.shape
    s_vs_p = 0.5
    amount = percent_noise
    out = np.copy(image)

    num_salt = np.ceil(amount * image.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]       
    out[tuple(coords)] = 1

    num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    out[tuple(coords)] = 0
    image = Image.fromarray((out*1).astype(np.uint8))
    image.save(save_path, format='jpeg')


file_to_extract = r"C://Users/lewis/Desktop/csgo photos2"
for file in os.listdir(file_to_extract):
    file_to_extract_img = file_to_extract + "/" + file
    img = Image.open(file_to_extract_img)
    img = img.resize((20,20))
    img.save(f"C:/Users/lewis/Desktop/mass_batch_save_test/{file}.jpeg", format='jpeg')






def hideSyntax(): #Not to be used
    #SYNTAX TO REMEMBER
    #data = image.imread('C:/Users/lewis/Desktop/csgo photos/0.jpeg')
    #print(data.dtype)
    #print(data.shape)
    #pyplot.imshow(data)
    #pyplot.show()
    #image2 = Image.open('C:/Users/lewis/Desktop/csgo photos/0.jpeg') #load the greyscale image ###this is how to open an image
    pass

def useCaseExamples():
    greyscale("C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/greyscale.jpeg")
    resize_aspect_preserved(20, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/resize_preserved.jpeg")
    resize_aspect_not_preserved(500, 60, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/resize_not_preserved.jpeg")
    flip(True, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/flip.jpeg")
    rotate(26, True, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/rotate.jpeg")
    crop(45, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/crop.jpeg")
    blur(6, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/blur.jpeg")
    gaussian_blur(6, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/gaussian_blur.jpeg")
    brightness(50, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/brightness.jpeg")
    contrast(250, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/contrast.jpeg")
    colour(300, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/colour.jpeg")
    gauss_noise(10, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/gauss_noise.jpeg")
    s_and_p_noise(5, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/s_and_p_noise.jpeg")

