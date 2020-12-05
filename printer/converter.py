# -*- coding: utf-8 -*-

import cv2
import numpy as np
from numba import jit
from PIL import Image


@jit
def dither(num, thresh = 127):
    derr = np.zeros(num.shape, dtype = int)
    for y in range(num.shape[0]):
        for x in range(num.shape[1]):
            newval = derr[y, x] + num[y ,x]
            if newval >= thresh:
                errval = newval - 255
                num[y, x] = 1.
            else:
                errval = newval
                num[y, x] = 0.
            if x + 1 < num.shape[1]:
                derr[y, x + 1] += errval / 8
                if x + 2 < num.shape[1]:
                    derr[y, x + 2] += errval / 8
            if y + 1 < num.shape[0]:
                derr[y + 1, x - 1] += errval / 8
                derr[y + 1, x] += errval / 8
                if y + 2< num.shape[0]:
                    derr[y + 2, x] += errval / 8
                if x + 1 < num.shape[1]:
                    derr[y + 1, x + 1] += errval / 8
    return num[::-1,:] * 255

def adjust(path, min_brightness = 0.4, basewidth = 384):
    original = cv2.flip(cv2.imread(path), 0)
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    cols, rows = gray.shape
    brightness = np.sum(gray) / (255 * cols * rows)
    ratio = brightness / min_brightness
    adj = cv2.convertScaleAbs(gray, alpha = (1 / ratio), beta = 0)
    pil = Image.fromarray(adj)
    wpercent = (basewidth / float(pil.size[0]))
    hsize = int((float(pil.size[1]) * float(wpercent)))
    img = pil.resize((basewidth, hsize), Image.ANTIALIAS)
    dithered = dither(np.array(img)[:,:])
    return dithered

def convert_img(path):
    img = adjust(path)
    bin_image = np.array(img).astype(bool).astype(int)
    bin_image[bin_image == 1] = 2
    bin_image[bin_image == 0] = 1
    bin_image[bin_image == 2] = 0
    bits_str = ''.join(map(str, bin_image.flatten()))
    partitioned_str = [bits_str[i:i + 8] for i in range(0, len(bits_str), 8)]
    int_str = [int(i, 2) for i in partitioned_str]
    return bytes(int_str)
