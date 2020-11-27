#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numba
import numpy as np
from PIL import Image, ImageEnhance


@numba.jit
def dither(num, thresh = 127):
    derr = np.zeros(num.shape, dtype = int)
    div = 8
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
                derr[y, x + 1] += errval / div
                if x + 2 < num.shape[1]:
                    derr[y, x + 2] += errval / div
            if y + 1 < num.shape[0]:
                derr[y + 1, x - 1] += errval / div
                derr[y + 1, x] += errval / div
                if y + 2< num.shape[0]:
                    derr[y + 2, x] += errval / div
                if x + 1 < num.shape[1]:
                    derr[y + 1, x + 1] += errval / div
    return num[::-1,:] * 255

def to_bit_stream(bin_image: np.ndarray):
    bits_str = ''.join(map(str, bin_image.flatten()))
    partitioned_str = [bits_str[i:i + 8] for i in range(0, len(bits_str), 8)]
    int_str = [int(i, 2) for i in partitioned_str]
    return bytes(int_str)

def to_bin_image(path):
    basewidth = 384
    img = Image.open(path).convert('L')
    img = img.transpose(Image.ROTATE_90)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    m = np.array(img)[:,:]
    m2 = dither(m)
    out = Image.fromarray(m2[::-1,:])
    out.show()
    enhancer = ImageEnhance.Contrast(out)
    enhanced_img = enhancer.enhance(4.0)
    enhanced_img.show()
    np_img = np.array(enhanced_img).astype(bool).astype(int)
    np_img[np_img == 1] = 100
    np_img[np_img == 0] = 1
    np_img[np_img == 100] = 0
    return to_bit_stream(np_img)
