#Created by Lewis Murch
import os
import os.path
import numpy as np
from matplotlib import image
from matplotlib import pyplot
import cv2
from PIL import Image, ImageFile, ImageDraw, ImageChops, ImageFilter, ImageEnhance

gs, rap, ranp, flip, rot, crop, blur, gauss_blur, bright, contrast, sharp, colour, guass_noise, s_a_p = False, False, False, False, False, False, False, False, False, False, False, False, False, False
rename_files_bool = False

def greyscale_pic(path, save_path):
    image = Image.open(path) #Load the image
    gs_image = image.convert(mode='L') #Convert the image to greyscale
    gs_image.save(save_path + "greyscale.jpeg", format='jpeg') 

def resize_aspect_preserved_pic(size_chosen, path, save_path):
    image = Image.open(path) #Load the image
    resized_image = image.thumbnail((size_chosen, size_chosen)) #Resize the image
    image.save(save_path + "preserved_aspect.jpeg", format='jpeg') 

def resize_aspect_not_preserved_pic(size_x_chosen, size_y_chosen, path, save_path):
    image = Image.open(path) #Load the image
    resized_image = image.resize((size_x_chosen, size_y_chosen)) #Resize the image
    resized_image.save(save_path + "not_preserved_aspect.jpeg", format='jpeg') 

def flip_pic(vertical, path, save_path):
    image = Image.open(path) #Load the image
    if vertical == False:
        hoz_flip = image.transpose(Image.FLIP_LEFT_RIGHT)
        hoz_flip.save(save_path + "hoz_flip.jpeg", format='jpeg') 
    else:
        ver_flip = image.transpose(Image.FLIP_TOP_BOTTOM)
        ver_flip.save(save_path + "ver_flip.jpeg", format='jpeg') 
        
def rotate_pic(amount, clockwise, path, save_path): #clockwise is bool, allow up to 360 degrees
    image = Image.open(path) #Load the image
    if clockwise == True:
        image_rotated = image.rotate(-amount)
        pyplot.imshow(image_rotated)
        image_rotated.save(save_path + "rotated.jpeg", format='jpeg') 
    else:
        image_rotated = image.rotate(amount)
        pyplot.imshow(image_rotated)
        image_rotated.save(save_path + "rotated.jpeg", format='jpeg') 

def crop_pic(percent_cropped, path, save_path): #input as coords. cannot accept 100 or above!
    percent_cropped /= 2
    image = Image.open(path) #Load the image
    x=image.size[0]
    y=image.size[1]
    x_use = int(x/100 * percent_cropped)
    y_use = int(y/100 * percent_cropped)
    cropped = image.crop((x_use, y_use, x - x_use, y - y_use))
    cropped.save(save_path + "crop.jpeg", format='jpeg') 
    
def blur_pic(radius, path, save_path):
    image = Image.open(path) #Load the image
    blur_image = image.filter(ImageFilter.BoxBlur(radius))
    blur_image.save(save_path + "blur.jpeg", format='jpeg') 

def gaussian_blur_pic(radius, path, save_path):
    image = Image.open(path) #Load the image
    gauss_image = image.filter(ImageFilter.GaussianBlur(5))
    gauss_image.save(save_path + "guass_blur.jpeg", format='jpeg') 

def brightness_pic(percent_brightness, path, save_path): 
    percent_brightness /= 100
    image = Image.open(path) #Load the image
    enhancer = ImageEnhance.Brightness(image)
    bright_image = enhancer.enhance(percent_brightness)
    bright_image.save(save_path + "brightness.jpeg", format='jpeg') 

def contrast_pic(percent_contrast, path, save_path): 
    percent_contrast /= 100
    image = Image.open(path) #Load the image
    enhancer = ImageEnhance.Contrast(image)
    contrast_image = enhancer.enhance(percent_contrast)
    contrast_image.save(save_path + "contrast.jpeg", format='jpeg') 

def sharpness_pic(percent_sharpness, path, save_path): 
    percent_sharpness /= 100
    image = Image.open(path) #Load the image
    enhancer = ImageEnhance.Sharpness(image)
    sharpness_image = enhancer.enhance(percent_sharpness)
    sharpness_image.save(save_path + "sharpness.jpeg", format='jpeg') 

def colour_pic(percent_colour, path, save_path): 
    percent_colour /= 100
    image = Image.open(path) #Load the image
    enhancer = ImageEnhance.Color(image)
    sharpness_image = enhancer.enhance(percent_colour)
    sharpness_image.save(save_path + "colour.jpeg", format='jpeg') 

def gauss_noise_pic(percent_noise, path, save_path): 
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
    image.save(save_path + "guass_noise.jpeg", format='jpeg') 

def s_and_p_noise_pic(percent_noise, path, save_path):
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
    image.save(save_path + "s_and_p_noise.jpeg", format='jpeg') 

def rename_pictures_pic(path):
    files = os.listdir(path)

    for index, file in enumerate(files):
        os.rename(os.path.join(path, file), os.path.join(path, 'image_'.join([str(index), '.jpg'])))



def set_requirments():
    print("Enter 1 for yes, and 0 for no to the following questions: \n")
    global gs
    use_gs = int(input("Use greyscale tool?: \n"))
    if use_gs == 1:
        gs = True
    elif use_gs == 0:
        gs = False
    else:
        print("error selecting greyscale tool")

    use_rap = int(input("Resize the image keeping the aspect ratio the same?: \n"))
    global rap
    if use_rap == 1:
        rap = True
    elif use_rap == 0:
        rap = False
    else:
        print("error selecting aspect ratio resize")

    use_ranp = int(input("Resize the image controlling both axis?: \n"))
    global ranp
    if use_ranp == 1:
        ranp = True
    elif use_ranp == 0:
        ranp = False
    else:
        print("error selecting resize (not aspect locked) tool")

    use_flip = int(input("Use flip?: \n"))
    global flip
    if use_flip == 1:
        flip = True
    elif use_flip == 0:
        flip = False
    else:
        print("error selecting flip tool")

    use_rot = int(input("Use rotation tool?: \n"))
    global rot
    if use_rot == 1:
        rot = True
    elif use_rot == 0:
        rot = False
    else:
        print("error selecting rotation tool")

    use_crop = int(input("Use crop tool?: \n"))
    global crop
    if use_crop == 1:
        crop = True
    elif use_crop == 0:
        crop = False
    else:
        print("error selecting crop tool")

    use_blur = int(input("Use blur tool?: \n"))
    global blur
    if use_blur == 1:
        blur = True
    elif use_blur == 0:
        blur = False
    else:
        print("error selecting blur tool")

    use_gauss_blur = int(input("Use gaussian blur tool?: \n"))
    global gauss_blur
    if use_gauss_blur == 1:
        gauss_blur = True
    elif use_gauss_blur == 0:
        gauss_blur = False
    else:
        print("error selecting gaussian blur tool")

    use_bright = int(input("Use brightness tool?: \n"))
    global bright
    if use_bright == 1:
        bright = True
    elif use_bright == 0:
        bright = False
    else:
        print("error selecting brightness tool")

    use_contrast = int(input("Use contrast tool?: \n"))
    global contrast
    if use_contrast == 1:
        contrast = True
    elif use_contrast == 0:
        contrast = False
    else:
        print("error selecting contrast tool")

    use_sharp = int(input("Use sharpness tool?: \n"))
    global sharp
    if use_sharp == 1:
        sharp = True
    elif use_sharp == 0:
        sharp = False
    else:
        print("error selecting sharpness tool")

    use_colour = int(input("Use colour tool?: \n"))
    global colour
    if use_colour == 1:
        colour = True
    elif use_colour == 0:
        colour = False
    else:
        print("error selecting colour tool")

    use_guass_noise = int(input("Use gaussian noise tool?: \n"))
    global guass_noise
    if use_guass_noise == 1:
        guass_noise = True
    elif use_guass_noise == 0:
        guass_noise = False
    else:
        print("error selecting gaussian noise tool")

    use_s_a_p = int(input("Use salt and pepper noise tool?: \n"))
    global s_a_p
    if use_s_a_p == 1:
        s_a_p = True
    elif use_s_a_p == 0:
        s_a_p = False
    else:
        print("error selecting salt and pepper noise tool")

    use_rename = int(input("Do you want to rename all the files?: \n"))
    global rename
    if use_rename == 1:
        rename_files_bool == True
    elif use_rename == 0:
        rename_files_bool == False
    else:
        print("There was an issue choosing whether to rename files")

    do_work()

def do_work():
    file_to_extract = r"C://Users/lewis/Desktop/csgo photos2"
    for file in os.listdir(file_to_extract):
        file_to_save_directory = f"C:/Users/lewis/Desktop/mass_batch_save_test/"
        file_to_save = f"C:/Users/lewis/Desktop/mass_batch_save_test/{file}"
        file_to_extract_img = file_to_extract + "/" + file

        if gs == True:
            greyscale_pic(file_to_extract_img, file_to_save)

        if rap == True:
            resize_aspect_not_preserved_pic(46, 120, file_to_extract_img, file_to_save)

        if flip == True:
            flip_pic(True, file_to_extract_img, file_to_save)

        if rot == True:
            rotate_pic(70, True, file_to_extract_img, file_to_save)

        if crop == True:
            crop_pic(40, file_to_extract_img, file_to_save)

        if blur == True:
            blur_pic(6, file_to_extract_img, file_to_save)

        if gauss_blur == True:
            gaussian_blur_pic(4, file_to_extract_img, file_to_save)

        if bright == True:
            brightness_pic(130, file_to_extract_img, file_to_save)

        if contrast == True:
            contrast_pic(90, file_to_extract_img, file_to_save)

        if sharp == True:
            sharpness_pic(100, file_to_extract_img, file_to_save)

        if colour == True:
            colour_pic(600, file_to_extract_img, file_to_save)

        if guass_noise == True:
            gauss_noise_pic(20, file_to_extract_img, file_to_save)

        if s_a_p == True:
            s_and_p_noise_pic(40, file_to_extract_img, file_to_save)

        if rename_files_bool == True:
            rename_pictures(file_to_save_directory)

set_requirments()









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
    greyscale_pic("C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/greyscale.jpeg")
    resize_aspect_preserved_pic(20, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/resize_preserved.jpeg")
    resize_aspect_not_preserved_pic(500, 60, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/resize_not_preserved.jpeg")
    flip_pic(True, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/flip.jpeg")
    rotate_pic(26, True, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/rotate.jpeg")
    crop_pic(45, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/crop.jpeg")
    blur_pic(6, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/blur.jpeg")
    gaussian_blur_pic(6, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/gaussian_blur.jpeg")
    brightness_pic(50, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/brightness.jpeg")
    contrast_pic(250, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/contrast.jpeg")
    colour_pic(300, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/colour.jpeg")
    gauss_noise_pic(10, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/gauss_noise.jpeg")
    s_and_p_noise_pic(5, "C:/Users/lewis/Desktop/csgo photos/21.jpeg", "C:/Users/lewis/Desktop/saveDataTest/s_and_p_noise.jpeg")

