import cv2
import numpy as np


def align_images(img1, img2):
    # Convert images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Find keypoints and descriptors with SIFT
    sift = cv2.SIFT_create()
    keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

    # Use a FLANN based matcher to match the keypoints
    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descriptors1, descriptors2, k=2)

    # Store all the good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # Get the matching keypoints' coordinates
    points1 = np.zeros((len(good_matches), 2), dtype=np.float32)
    points2 = np.zeros((len(good_matches), 2), dtype=np.float32)

    for i, match in enumerate(good_matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography matrix
    H, mask = cv2.findHomography(points2, points1, cv2.RANSAC)
    
    # Align the images
    height, width, channels = img1.shape
    aligned_img = cv2.warpPerspective(img2, H, (width, height))

    return aligned_img


def blend_images(img1, img2, alpha=0.5):
    # Check if the sizes of images are equal
    if img1.shape != img2.shape:
        raise ValueError('Images must have the same dimensions for blending')
    
    # Blend the images
    blended = cv2.addWeighted(img1, alpha, img2, 1 - alpha, 0)
    return blended


def match_color(src, target):
    src = cv2.cvtColor(src, cv2.COLOR_BGR2Lab)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2Lab)

    # Calculate mean and standard deviation of the source and target images
    src_mean, src_std = cv2.meanStdDev(src)
    target_mean, target_std = cv2.meanStdDev(target)

    # Subtract the means from the source
    src -= src_mean

    # Scale the source according to the target's standard deviation
    src = (src_std / target_std) * src

    # Add the target mean to the adjusted source
    matched = np.uint8(src + target_mean)

    # Convert back to BGR color space
    matched = cv2.cvtColor(matched, cv2.COLOR_Lab2BGR)
    return matched

