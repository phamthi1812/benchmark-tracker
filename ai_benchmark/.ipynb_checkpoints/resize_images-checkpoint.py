from PIL import Image


def smart_resize(input_image, new_size):
    width = input_image.width
    height = input_image.height

# Image is portrait or square
    if height >= width:
        crop_box = (0, (height-width)//2, width, (height-width)//2 + width)
        return input_image.resize(size = (new_size,new_size),
                                  box = crop_box)

# Image is landscape
    if width > height:
        crop_box = ((width-height)//2, 0, (width-height)//2 + height, height)
        
        return input_image.resize(size = (new_size,new_size),
                                  box = crop_box)
    
def resize_image( image: Image, length: int) -> Image:
    """
    Resize an image to a square. Can make an image bigger to make it fit or smaller if it doesn't fit. It also crops
    part of the image.

    :param self:
    :param image: Image to resize.
    :param length: Width and height of the output image.
    :return: Return the resized image.
    """

    """
    Resizing strategy : 
     1) We resize the smallest side to the desired dimension (e.g. 1080)
     2) We crop the other side so as to make it fit with the same length as the smallest side (e.g. 1080)
    """
    if image.size[0] < image.size[1]:
        # The image is in portrait mode. Height is bigger than width.

        # This makes the width fit the LENGTH in pixels while conserving the ration.
        resized_image = image.resize((length, int(image.size[1] * (length / image.size[0]))))

        # Amount of pixel to lose in total on the height of the image.
        required_loss = (resized_image.size[1] - length)

        # Crop the height of the image so as to keep the center part.
        resized_image = resized_image.crop(
            box=(0, required_loss / 2, length, resized_image.size[1] - required_loss / 2))

        # We now have a length*length pixels image.
        return resized_image
    else:
        # This image is in landscape mode or already squared. The width is bigger than the heihgt.

        # This makes the height fit the LENGTH in pixels while conserving the ration.
        resized_image = image.resize((int(image.size[0] * (length / image.size[1])), length))

        # Amount of pixel to lose in total on the width of the image.
        required_loss = resized_image.size[0] - length

        # Crop the width of the image so as to keep 1080 pixels of the center part.
        resized_image = resized_image.crop(
            box=(required_loss / 2, 0, resized_image.size[0] - required_loss / 2, length))

        # We now have a length*length pixels image.
        return resized_image
    
import os   
import cv2 as cv
import numpy as np
from os import listdir
from os.path import isfile, join
from pathlib import Path
import argparse


home = os.environ['HOME']  

n = 0 

        
for file in os.listdir(home+"/Benchmark-Tracker/ai_benchmark/val/"):
    im = Image.open(os.path.join(home+"/Benchmark-Tracker/ai_benchmark/val/", file),'r')
    if im.mode != 'RGB':
        im = im.convert(mode='RGB')
    new_im = smart_resize(im,512)
    new_im.save(home+"/Benchmark-Tracker/ai_benchmark/output/%s.jpg"%n)
    n= n+1 
    print("saved ",n)
  
        
 
    