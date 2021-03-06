# Author: Jose G Perez
# Version 1.0
# Last Modified: January 31, 2018
import cv2
import numpy as np
import pylab as plt
from multiprocessing.pool import ThreadPool
from timeit import default_timer as timer

from util_sift import load_sift
from util_matching import match_details
INDIVIDUAL = False

np.random.seed(1)
np.set_printoptions(threshold=np.nan, linewidth=1000)
# Default: contrast 0.04, edge 10, sigma 1.6
# Experiment: 0.08, 30, 2
# CT: The larger the threshold, the less features are produced by the detector
# ET: The larger the threshold, the more features that are retained
SIFT = cv2.xfeatures2d.SIFT_create(contrastThreshold=0.05, edgeThreshold=100, sigma=2)

RADIUS = 50
RADIUS_SQUARED = RADIUS ** 2
SCALE_THRESHOLD = 3
DISTANCE_THRESHOLD = 200
RESPONSE_THRESHOLD = 0.01

DISTANCE_RATIO = 0.95
RANSAC_REPROJ_TRESHHOLD = 10 # The higher the threshold, the lower the inliers
RANSAC_MAX_ITERS = 2000
RANSAC_CONFIDENCE = 0.99

FIGURE_IDX = 0
def imshow(im, title=''):
    global FIGURE_IDX
    plt.figure(FIGURE_IDX)
    plt.axis('off')
    plt.tick_params(axis='both',
                    left='off', top='off', right='off', bottom='off',
                    labelleft='off', labeltop='off', labelright='off', labelbottom='off')
    plt.title(title)
    plt.imshow(im)

    FIGURE_IDX += 1

def gallery(array, ncols=3):
    # Grayscale
    if len(array.shape) == 3:
        nindex, height, width = array.shape
        nrows = nindex//ncols
        result = (array.reshape(nrows, ncols, height, width)
                  .swapaxes(1,2)
                  .reshape(height*nrows, width*ncols))
        return result
    # Color
    else:
        nindex, height, width, intensity = array.shape
        nrows = nindex//ncols
        # want result.shape = (height*nrows, width*ncols, intensity)
        result = (array.reshape(nrows, ncols, height, width, intensity)
                  .swapaxes(1,2)
                  .reshape(height*nrows, width*ncols, intensity))
        return result

s_im, s_label, s_kp, s_des = load_sift('S_BB_V1_SIFT.npz')
pw_im, pw_label, pw_kp, pw_des = load_sift('PW_BB_V1_SIFT.npz')

time_start = timer()
# ==== MATCHING SYSTEM BEGIN
if INDIVIDUAL:
    # im1 = s_im[np.where(s_label == 67)[0][0]]
    # im2 = pw_im[np.where(pw_label == 145)[0][0]]

    # im1 = s_im[np.where(s_label == 6)[0][0]]
    # im2 = pw_im[np.where(pw_label == 8)[0][0]]

    im1 = s_im[np.where(s_label == 33)[0][0]]
    im2 = pw_im[np.where(pw_label == 68)[0][0]]

    kp1, des1 = SIFT.detectAndCompute(im1, None)
    kp2, des2 = SIFT.detectAndCompute(im2, None)

    m, matches, stat_s_diff, stat_d_dist, stat_resp_kp1, stat_resp_kp2, stat_rad  = match_details(kp1, des1, kp2, des2)
    print("\t[ScaleD] Max %.3f, Min %.3f, Avg %.3f" % (max(stat_s_diff) , min(stat_s_diff), sum(stat_s_diff) / len(stat_s_diff)))
    print("\t[DescD] Max %.3f, Min %.3f, Avg %.3f" % (max(stat_d_dist),  min(stat_d_dist), sum(stat_d_dist) / len(stat_d_dist)))
    print("\t[RespKp1] Max %.3f, Min %.3f, Avg %.3f" % (max(stat_resp_kp1), min(stat_resp_kp1), sum(stat_resp_kp1) / len(stat_resp_kp1)))
    print("\t[RespKp2] Max %.3f, Min %.3f, Avg %.3f" % (max(stat_resp_kp2), min(stat_resp_kp2), sum(stat_resp_kp2) / len(stat_resp_kp2)))
    print("\t[Rad] Max %.3f, Min %.3f, Avg %.3f" % (max(stat_rad), min(stat_rad), sum(stat_rad) / len(stat_rad)))

    # For comparison, the selected SIFT keypoints
    # BF = cv2.BFMatcher(normType=cv2.NORM_L2, crossCheck=True)
    # bf_matches = BF.match(des1, des2)
    # im_bf_matches = cv2.drawMatches(im1,kp1,im2,kp2,bf_matches,None,flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
    # metric_bf = len(bf_matches)/ (len(kp1) + len(kp2) - len(bf_matches))
    BF = cv2.BFMatcher(normType=cv2.NORM_L2)
    bf_matches = BF.knnMatch(des1, des2, k=2)

    # For comparison, RANSAC
    good_matches = [m[0] for m in bf_matches if len(m) == 2 and m[0].distance < m[1].distance * DISTANCE_RATIO]
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches])
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches])
    H, mask = cv2.findHomography(src_pts, dst_pts, method=cv2.RANSAC, ransacReprojThreshold=RANSAC_REPROJ_TRESHHOLD, maxIters=RANSAC_MAX_ITERS, confidence=RANSAC_CONFIDENCE)
    matchesMask = mask.ravel().tolist()
    drawParameters = dict(matchColor=None, singlePointColor=None, matchesMask=matchesMask,
                          flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

    # Draw the lines between the 2 images connecting matches
    im_ransac = cv2.drawMatches(im1, kp1, im2, kp2, good_matches, None, **drawParameters)

    # Images
    im1_kp = cv2.drawKeypoints(im1, kp1, None, None, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    im2_kp = cv2.drawKeypoints(im2, kp2, None, None, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    im_matches = cv2.drawMatches(im1,kp1,im2,kp2,matches,None,flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

    metric = len(matches) / (len(kp1) + len(kp2) - len(matches))
    print("Metric", metric)
    print("Inliers", mask.sum())

    plt.gray()
    imshow(im1_kp, 'S Keypoint Data')
    imshow(im2_kp, 'PW Keypoint Data')
    #imshow(im_bf_matches, 'BF Matches')
    imshow(im_matches, 'New Matching')
    imshow(im_ransac, 'RANSAC')
else:
    # im2 = pw_im[np.where(pw_label == 68)[0][0]]
    pw_idx = 33
    im2 = pw_im[pw_idx]
    (kp2, des2) = (pw_kp[pw_idx], pw_des[pw_idx])

    all_matches = []
    all_im = []
    all_kp = []
    all_des = []

    cidx = 0
    for sidx in range(25, 40):
        # if sidx == 32:
        #     print('=[P]', end='')
        print("S", (sidx + 1), "CIDX", cidx)

        (im1, kp1, des1) = (s_im[sidx], s_kp[sidx], s_des[sidx])
        m, matches, stat_s_diff, stat_d_dist, stat_resp_kp1, stat_resp_kp2, stat_rad = match_details(kp1, des1, kp2,
                                                                                                     des2)
        # print("\t[ScaleD] Max %.3f, Min %.3f, Avg %.3f" % (
        # max(stat_s_diff), min(stat_s_diff), sum(stat_s_diff) / len(stat_s_diff)))
        # print("\t[DescD] Max %.3f, Min %.3f, Avg %.3f" % (
        # max(stat_d_dist), min(stat_d_dist), sum(stat_d_dist) / len(stat_d_dist)))
        # print("\t[RespKp1] Max %.3f, Min %.3f, Avg %.3f" % (
        # max(stat_resp_kp1), min(stat_resp_kp1), sum(stat_resp_kp1) / len(stat_resp_kp1)))
        # print("\t[RespKp2] Max %.3f, Min %.3f, Avg %.3f" % (
        # max(stat_resp_kp2), min(stat_resp_kp2), sum(stat_resp_kp2) / len(stat_resp_kp2)))
        # print("\t[Rad] Max %.3f, Min %.3f, Avg %.3f" % (max(stat_rad), min(stat_rad), sum(stat_rad) / len(stat_rad)))

        metric = len(matches) / (len(kp1) + len(kp2) - len(matches))

        print("\tMetric w/PW %s is %.3f, Matches %d" % (pw_idx, metric, len(matches)))

        all_matches.append(matches)
        all_im.append(im1)
        all_kp.append(kp1)
        all_des.append(des1)
        cidx += 1

    # index = 7
    # imshow(cv2.drawMatches(all_im[index], all_kp[index], im2, kp2, all_matches[index], None, flags=2), '[P]SW33')
    # index = 8
    # imshow(cv2.drawMatches(all_im[index], all_kp[index], im2, kp2, all_matches[index], None, flags=2), 'SW34')

duration = timer() - time_start
print("Program took %.3fs" % duration)