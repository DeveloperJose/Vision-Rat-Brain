# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pylab as plt

import scipy.ndimage.filters as filters
import scipy.signal as signal
import scipy.misc as misc

import feature
import timing

import logbook
logger = logbook.Logger(__name__)

sift = cv2.xfeatures2d.SIFT_create(contrastThreshold=0.08, edgeThreshold=30, sigma=2)
affine = True


def draw_kp(im):
    if affine:
        kp, des = feature.extract_sift(im)
    else:
        kp = sift.detect(im)

    print("Keypoints: ", len(kp))
    im_kp = cv2.drawKeypoints(im, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    plt.figure(figsize=(10,10))
    plt.imshow(im_kp)


def match(im):
    atlas = feature.im_read('scripts_testing/plate-34.jpg')

    if affine:
        kp, des = feature.extract_sift(im)
        kp2, des2 = feature.extract_sift(atlas)
    else:
        kp, des = sift.detectAndCompute(im, None)
        kp2, des2 = sift.detectAndCompute(atlas, None)

    match = feature.match(im, kp, des, atlas, kp2, des2)
    print("Matches: ", len(match.matches))
    print("Inliers: ", match.inlier_count)
    plt.figure(figsize=(10,10))
    plt.imshow(match.result)
    plt.figure(figsize=(10,10))
    plt.imshow(match.result2)

    return match.H

filename = 'scripts_testing/region-70-HQ.jpg'
im_region = feature.im_read(filename)
im_region_gray = feature.im_read(filename, flags=cv2.IMREAD_GRAYSCALE)

# *************** Resizing
#im_region = misc.imresize(im_region, (170, 310))
im_region = misc.imresize(im_region, 10)

# *************** Convolution
#n = 6
#kernel = np.ones((n,n),np.float32)/(n**2)
#dst = cv2.filter2D(im_region,-1,kernel)

affine = True
draw_kp(feature.im_read('scripts_testing/region-34.jpg'))
draw_kp(im_region)

timing.stopwatch()
H = match(im_region)
timing.stopwatch("Matching")