#Created by Lewis Murch
import os
import os.path
import numpy as np
from matplotlib import image
from matplotlib import pyplot
import cv2
from PIL import Image, ImageFile, ImageDraw, ImageChops, ImageFilter, ImageEnhance
from pathlib import Path
import time
import random

gs, rap, ranp, flip, rot, crop, blur, gauss_blur, bright, contrast, sharp, colour, guass_noise, s_a_p = False, False, False, False, False, False, False, False, False, False, False, False, False, False
rap_value, ranp_x, ranp_y, flip_value, rot_direction, rot_value, crop_value, blur_value, g_blur_value, bright_value, contrast_value, sharp_value, colour_value, g_noise_value, sap_value = 0,0,0,True,True,0,0,0,0,0,0,0,0,0,0
rename_files_bool = False



def greyscale_pic(path, save_path):
    image = Image.open(path) #Load the image
    gs_image = image.convert(mode='L') #Convert the image to greyscale
    gs_image.save(save_path + "_greyscale.jpeg", format='jpeg') 

def resize_aspect_preserved_pic(size_chosen, path, save_path):
    image = Image.open(path) #Load the image
    resized_image = image.thumbnail((size_chosen, size_chosen)) #Resize the image
    image.save(save_path + "_preserved_aspect.jpeg", format='jpeg') 

def resize_aspect_not_preserved_pic(size_x_chosen, size_y_chosen, path, save_path):
    image = Image.open(path) #Load the image
    resized_image = image.resize((size_x_chosen, size_y_chosen)) #Resize the image
    resized_image.save(save_path + "_not_preserved_aspect.jpeg", format='jpeg') 

def flip_pic(vertical, path, save_path):
    image = Image.open(path) #Load the image
    if vertical == False:
        hoz_flip = image.transpose(Image.FLIP_LEFT_RIGHT)
        hoz_flip.save(save_path + "_hoz_flip.jpeg", format='jpeg') 
    else:
        ver_flip = image.transpose(Image.FLIP_TOP_BOTTOM)
        ver_flip.save(save_path + "_ver_flip.jpeg", format='jpeg') 
        
def rotate_pic(amount, clockwise, path, save_path): #clockwise is bool, allow up to 360 degrees
    image = Image.open(path) #Load the image
    amount = random.randrange(1, amount)
    if clockwise == True:
        image_rotated = image.rotate(-amount)
        pyplot.imshow(image_rotated)
        image_rotated.save(save_path + "_rotated.jpeg", format='jpeg') 
    else:
        image_rotated = image.rotate(amount)
        pyplot.imshow(image_rotated)
        image_rotated.save(save_path + "_rotated.jpeg", format='jpeg') 

def crop_pic(percent_cropped, path, save_path): #input as coords. cannot accept 100 or above!
    percent_cropped = random.randrange(1, int(percent_cropped))
    percent_cropped /= 2
    image = Image.open(path) #Load the image
    x=image.size[0]
    y=image.size[1]
    x_use = int(x/100 * percent_cropped)
    y_use = int(y/100 * percent_cropped)
    cropped = image.crop((x_use, y_use, x - x_use, y - y_use))
    cropped.save(save_path + "_crop.jpeg", format='jpeg') 
    
def blur_pic(radius, path, save_path):
    image = Image.open(path) #Load the image
    radius = random.randrange(1, radius)
    blur_image = image.filter(ImageFilter.BoxBlur(radius))
    blur_image.save(save_path + "_blur.jpeg", format='jpeg') 

def gaussian_blur_pic(radius, path, save_path):
    raduis = random.randrange(1, radius)
    image = Image.open(path) #Load the image
    gauss_image = image.filter(ImageFilter.GaussianBlur(5))
    gauss_image.save(save_path + "_guass_blur.jpeg", format='jpeg') 

def brightness_pic(percent_brightness, path, save_path): 
    percent_brightness = random.randrange(1, int(percent_brightness))
    percent_brightness /= 100
    image = Image.open(path) #Load the image
    enhancer = ImageEnhance.Brightness(image)
    bright_image = enhancer.enhance(percent_brightness)
    bright_image.save(save_path + "_brightness.jpeg", format='jpeg') 

def contrast_pic(percent_contrast, path, save_path): 
    percent_contrast = random.randrange(1, int(percent_contrast))
    percent_contrast /= 100
    image = Image.open(path) #Load the image
    enhancer = ImageEnhance.Contrast(image)
    contrast_image = enhancer.enhance(percent_contrast)
    contrast_image.save(save_path + "_contrast.jpeg", format='jpeg') 

def sharpness_pic(percent_sharpness, path, save_path): 
    percent_sharpness = random.randrange(1, int(percent_sharpness))
    percent_sharpness /= 100
    image = Image.open(path) #Load the image
    enhancer = ImageEnhance.Sharpness(image)
    sharpness_image = enhancer.enhance(percent_sharpness)
    sharpness_image.save(save_path + "_sharpness.jpeg", format='jpeg') 

def colour_pic(percent_colour, path, save_path): 
    percent_colour = random.randrange(1, int(percent_colour))
    percent_colour /= 100
    image = Image.open(path) #Load the image
    enhancer = ImageEnhance.Color(image)
    sharpness_image = enhancer.enhance(percent_colour)
    sharpness_image.save(save_path + "_colour.jpeg", format='jpeg') 

def gauss_noise_pic(percent_noise, path, save_path): 
    percent_noise = random.randrange(1, int(percent_noise))
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
    image.save(save_path + "_guass_noise.jpeg", format='jpeg') 

def s_and_p_noise_pic(percent_noise, path, save_path):
    percent_noise = random.randrange(1, int(percent_noise))
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
    image.save(save_path + "_s_and_p_noise.jpeg", format='jpeg') 

def initial_rename_pictures_pic(path):
    files = os.listdir(path)

    for index, file in enumerate(files):
        os.rename(os.path.join(path, file), os.path.join(path, ''.join([str(index)])))

def post_rename_pictures_pic(path):
    files = os.listdir(path)

    for index, file in enumerate(files):
        try:
            os.rename(os.path.join(path, file), os.path.join(path, ''.join([str(index), '.jpg'])))
        except:
            pass #error with renaming

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
    global rap_value
    if use_rap == 1:
        rap = True
        use_rap = int(input("Please enter a resize value: \n"))
        rap_value = use_rap
    elif use_rap == 0:
        rap = False
    else:
        print("error selecting aspect ratio resize")

    use_ranp = int(input("Resize the image controlling both axis?: \n"))
    global ranp
    global ranp_x
    global ranp_y
    if use_ranp == 1:
        ranp = True
        use_ranp = int(input("Please enter an x axis dimension: \n"))
        ranp_x = use_ranp
        use_ranp = int(input("Please enter a y axis dimension: \n"))
        ranp_y = use_ranp
    elif use_ranp == 0:
        ranp = False
    else:
        print("error selecting resize (not aspect locked) tool")

    use_flip = int(input("Use flip?: \n"))
    global flip
    global flip_value
    if use_flip == 1:
        flip = True
        use_flip = int(input("Vertical rotation? 1 for yes and 0 for no: \n"))
        if use_flip == 1:
            flip_value = True
        elif use_flip == 0:
            flip_value = False
        else:
            print("Error selecting flip direction")
    elif use_flip == 0:
        flip = False
    else:
        print("error selecting flip tool")

    use_rot = int(input("Use rotation tool?: \n"))
    global rot
    global rot_value
    global rot_direction
    if use_rot == 1:
        rot = True
        use_rot = int(input("Do you want to rotate the image clockwise?: \n"))
        if use_rot == 1:
            rot_direction = True
        elif use_rot == 0:
            rot_direction = False
        else:
            print("There was an issue selecting the direction to rotate the image")
        use_rot = int(input("How many degrees do you want to rotate the image?: \n"))
        rot_value = use_rot
    elif use_rot == 0:
        rot = False
    else:
        print("error selecting rotation tool")

    use_crop = int(input("Use crop tool?: \n"))
    global crop
    global crop_value
    if use_crop == 1:
        crop = True
        use_crop = int(input("What percent do you want to crop?: \n"))
        crop_value = use_crop
    elif use_crop == 0:
        crop = False
    else:
        print("error selecting crop tool")

    use_blur = int(input("Use blur tool?: \n"))
    global blur
    global blur_value
    if use_blur == 1:
        blur = True
        use_blur = int(input("Please enter your desired blur radius?: \n"))
        blur_value = use_blur
    elif use_blur == 0:
        blur = False
    else:
        print("error selecting blur tool")

    use_gauss_blur = int(input("Use gaussian blur tool?: \n"))
    global gauss_blur
    global g_blur_value
    if use_gauss_blur == 1:
        gauss_blur = True
        use_gauss_blur = int(input("Please enter your desired blur radius??: \n"))
        g_blur_value = use_gauss_blur
    elif use_gauss_blur == 0:
        gauss_blur = False
    else:
        print("error selecting gaussian blur tool")

    use_bright = int(input("Use brightness tool?: \n"))
    global bright
    global bright_value
    if use_bright == 1:
        bright = True
        use_bright = int(input("What % of brightness do you want?: \n"))
        bright_value = use_bright
    elif use_bright == 0:
        bright = False
    else:
        print("error selecting brightness tool")

    use_contrast = int(input("Use contrast tool?: \n"))
    global contrast
    global contrast_value
    if use_contrast == 1:
        contrast = True
        use_contrast = int(input("What % of contrast do you want?: \n"))
        contrast_value = use_contrast
    elif use_contrast == 0:
        contrast = False
    else:
        print("error selecting contrast tool")

    use_sharp = int(input("Use sharpness tool?: \n"))
    global sharp
    global sharp_value
    if use_sharp == 1:
        sharp = True
        use_sharp = int(input("What % of sharpness do you want?: \n"))
        sharp_value = use_sharp
    elif use_sharp == 0:
        sharp = False
    else:
        print("error selecting sharpness tool")

    use_colour = int(input("Use colour tool?: \n"))
    global colour 
    global colour_value
    if use_colour == 1:
        colour = True
        use_colour = int(input("What % of saturation do you want?: \n"))
        colour_value = use_colour
    elif use_colour == 0:
        colour = False
    else:
        print("error selecting colour tool")

    use_guass_noise = int(input("Use gaussian noise tool?: \n"))
    global guass_noise
    global g_noise_value
    if use_guass_noise == 1:
        guass_noise = True
        use_guass_noise = int(input("What % of gaussian noise do you want?: \n"))
        g_noise_value = use_guass_noise
    elif use_guass_noise == 0:
        guass_noise = False
    else:
        print("error selecting gaussian noise tool")

    use_s_a_p = int(input("Use salt and pepper noise tool?: \n"))
    global s_a_p
    global sap_value
    if use_s_a_p == 1:
        s_a_p = True
        use_s_a_p = int(input("what % of noise do you want?: \n"))
        sap_value = use_s_a_p
    elif use_s_a_p == 0:
        s_a_p = False
    else:
        print("error selecting salt and pepper noise tool")

    use_rename = int(input("Do you want to rename all the files?: \n"))
    global rename_files_bool
    if use_rename == 1:
        rename_files_bool = True
    elif use_rename == 0:
        rename_files_bool = False
    else:
        print("There was an issue choosing whether to rename files")

    do_work()

def do_work():
    send_user_images_to_this_folder = r"C://Users/lewis/Desktop/csgo photos2" #folder where uploaded user photos will be sent to

    for name in os.listdir(send_user_images_to_this_folder):
        initial_rename_pictures_pic(send_user_images_to_this_folder)

    for file in os.listdir(send_user_images_to_this_folder):
        file_to_save = f"C:/Users/lewis/Desktop/mass_batch_save_test/{file}"
        file_to_extract_img = send_user_images_to_this_folder + "/" + file

        if gs == True:
            greyscale_pic(file_to_extract_img, file_to_save)

        if rap == True:
            resize_aspect_preserved_pic(rap_value, file_to_extract_img, file_to_save)

        if ranp == True:
            resize_aspect_not_preserved_pic(ranp_x, ranp_y, file_to_extract_img, file_to_save)

        if flip == True:
            flip_pic(flip_value, file_to_extract_img, file_to_save)

        if rot == True:
            rotate_pic(rot_value, rot_direction, file_to_extract_img, file_to_save)

        if crop == True:
            crop_pic(crop_value, file_to_extract_img, file_to_save)

        if blur == True:
            blur_pic(blur_value, file_to_extract_img, file_to_save)

        if gauss_blur == True:
            gaussian_blur_pic(g_blur_value, file_to_extract_img, file_to_save)

        if bright == True:
            brightness_pic(bright_value, file_to_extract_img, file_to_save)

        if contrast == True:
            contrast_pic(contrast_value, file_to_extract_img, file_to_save)

        if sharp == True:
            sharpness_pic(sharp_value, file_to_extract_img, file_to_save)

        if colour == True:
            colour_pic(colour_value, file_to_extract_img, file_to_save)

        if guass_noise == True:
            gauss_noise_pic(g_noise_value, file_to_extract_img, file_to_save)

        if s_a_p == True:
            s_and_p_noise_pic(sap_value, file_to_extract_img, file_to_save)

    for name in os.listdir(send_user_images_to_this_folder):
        post_rename_pictures_pic(send_user_images_to_this_folder)

    if rename_files_bool == True:
        for files in os.listdir(send_user_images_to_this_folder):
            file_to_save_directory = f"C:/Users/lewis/Desktop/mass_batch_save_test/"
            post_rename_pictures_pic(file_to_save_directory)


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

