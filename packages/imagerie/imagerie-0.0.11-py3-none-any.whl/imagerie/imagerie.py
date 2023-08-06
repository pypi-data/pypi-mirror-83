from imagerie.operations.morphology import remove_small_objects, binary_fill_holes

from PIL.Image import Image, composite, fromarray, open, AFFINE
from PIL.JpegImagePlugin import JpegImageFile

from imagerie.operations.img import img_as_uint, img_as_float

from imagerie.operations.img_format import toimage

import numpy as np
import math
import cv2


def get_rotation(pt1, pt2):
    """ Returns the rotation value in degrees of two spacial points from an image. """

    origin_x, origin_y = pt1[0], pt1[1]
    dest_x, dest_y = pt2[0], pt2[1]

    delta_x = dest_x - origin_x
    delta_y = dest_y - origin_y

    degrees_temp = math.atan2(delta_x, delta_y) / math.pi * 180
    if degrees_temp < 0:
        degrees_final = 360 + degrees_temp
    else:
        degrees_final = degrees_temp

    return degrees_final


def order_points(points: np.ndarray):
    """ Sorts the 4 (x, y) points clockwise starting from top-left point. """

    x_sorted = points[np.argsort(points[:, 0]), :]

    left_most = x_sorted[:2, :]
    right_most = x_sorted[2:, :]

    left_most = left_most[np.argsort(left_most[:, 1]), :]
    (tl, bl) = left_most

    # right_most = right_most[argsort(right_most[:, 1]), :]
    D = calculate_distance(tl[np.newaxis], right_most)
    (br, tr) = right_most[np.argsort(D)[::-1], :]

    return np.array([tl, tr, br, bl], dtype='float32')


def biggest_contour(grayscale):
    """ Finds and retrieves the biggest contour """

    contours, _ = cv2.findContours(grayscale, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return max(contours, key=cv2.contourArea)


def get_biggest_contour(contours):
    """ Simply retrieves the biggest contour """

    return max(contours, key=cv2.contourArea)


def calculate_distance(pt1, pt2):
    """ Calculates the spacial distance between 2 (x,y) points """

    if type(pt1) is tuple and type(pt2) is tuple:
        x1, y1 = pt1
        x2, y2 = pt2
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        return dist

    result = None
    pt1_type = type(pt1)
    pt2_type = type(pt2)
    if pt2_type is list or pt2_type is np.ndarray:
        result = []

        if pt1_type is list or pt1_type is np.ndarray:
            pt1 = pt1[0]
        else:
            pt1 = pt1

        x1, y1 = pt1

        for pt in pt2:
            if pt2_type is list:
                x2, y2 = pt
            else:
                x2, y2 = pt.ravel()

            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            result.append(dist)

    return np.array(result, dtype='float32')


def closest_point(point: tuple, points):
    """ Returns the closest (x, y) point from a given list of (x, y) points/coordinates. """

    distances = []
    for x, y in points:
        dist = calculate_distance(point, (x, y))
        distances.append(dist)

    return points[np.array(distances).argmin()]


def midpoint(ptA, ptB):
    """ Calculates X,Y middle points from provided 2 points. """

    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def line_intersection(line1: tuple, line2: tuple):
    """ Returns the intersection point between two lines. """

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('[imagerie] lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    return int(x), int(y)


def get_corners(grayscale, middle_points=False, centroid=False, max_corners=4, quality_level=0.01, min_distance=15):
    """ Returns the (x, y) coordinates of the 4 corners of a rectangular shaped object from binary mask by default.
    However, you can also calculate the top and bottom middle coordinates by providing \"middle_points=True\".
    And by providing \"centroid=True\", you can get the (x, y) coordinates of the center. """

    corners = cv2.goodFeaturesToTrack(grayscale, maxCorners=max_corners, qualityLevel=quality_level, minDistance=min_distance)
    corners = np.int0(corners)

    if corners is None:
        raise Exception('[error][imagerie] Could not detect corners.')

    corners2 = []
    for cr in corners:
        x, y = cr.ravel()
        corners2.append([x, y])

    corners = np.array(corners2)
    corners = order_points(corners)
    corners = np.int0(corners)

    c1 = tuple(corners[0])
    c2 = tuple(corners[1])
    c3 = tuple(corners[2])
    c4 = tuple(corners[3])
    
    corners = [c1, c2, c3, c4]

    x = [p[0] for p in corners]
    y = [p[1] for p in corners]
    centroid = (sum(x) / len(corners), sum(y) / len(corners))

    if not middle_points:
        if not centroid:
            return corners
        else:
            return [corners, centroid]

    contours, _ = cv2.findContours(grayscale, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = get_biggest_contour(contours)

    centroid_top_approx = (int(centroid[0]), int(centroid[1]) - 2)
    centroid_bottom_approx = (int(centroid[0]), int(centroid[1]) + 5)

    centroid_top = closest_point(centroid_top_approx, np.vstack(cnt).squeeze())
    centroid_bottom = closest_point(centroid_bottom_approx, np.vstack(cnt).squeeze())

    centroid_top = (centroid[0], centroid_top[1])
    centroid_bottom = (centroid[0], centroid_bottom[1])

    if not centroid:
        return np.int0([c1, centroid_top, c2, c3, centroid_bottom, c4])
    else:
        return [np.int0([c1, centroid_top, c2, c3, centroid_bottom, c4]), centroid]


def warp_perspective(image, src_pts, dst_pts, shape: tuple):
    """ Performs a warpPerspective() operation and expects the 4 (x, y) coordinates of the source and destination
    image. """

    width, height = shape

    src_pts = np.float32(src_pts)
    dst_pts = np.float32(dst_pts)

    h = cv2.getPerspectiveTransform(src_pts, dst_pts)

    res = cv2.warpPerspective(image, h, (width, height))

    return res


def warp_homography(image, src_pts, dst_pts, shape: tuple, method=cv2.RANSAC, reproj_threshold=5.0):
    """ Performs a warpPerspective() operation after findHomography(). """

    width, height = shape

    src_pts = np.float32(src_pts)
    dst_pts = np.float32(dst_pts)

    h, _ = cv2.findHomography(src_pts, dst_pts, method, reproj_threshold)

    res = cv2.warpPerspective(image, h, (width, height))

    return res


def image_composite_with_mask(to_add: Image, destination: Image, mask: Image) -> Image:
    """ Combines the `to_add` and `destination` images, `to_add` image will be added on top of `destination` image
     and only the white area from the `mask` image will be retained from `to_add` image. """

    if mask.mode != 'L':
        mask = mask.convert('L')

    return composite(to_add, destination, mask=mask)


def combine_two_images_with_mask(background_img, foreground_img, mask):
    """ Selects and pastes the content from "foreground_img" to "background_img" with the help of the provided mask.
    """

    if type(background_img) is str:
        background_img = open(background_img)

    if type(background_img) is np.ndarray:
        background_img = fromarray(background_img)

    if type(background_img) is not Image and type(background_img) is not JpegImageFile:
        raise Exception(f'Type of "background_img" must be one of these types [{Image}, {JpegImageFile}, {np.ndarray}, str]. "{type(background_img)}" given.')

    if type(foreground_img) is str:
        foreground_img = open(foreground_img)

    if type(foreground_img) is np.ndarray:
        foreground_img = fromarray(foreground_img)

    if type(foreground_img) is not Image and type(foreground_img) is not JpegImageFile:
        raise Exception(f'Type of "foreground_img" must be one of these types [{Image}, {JpegImageFile}, {np.ndarray}, str]. "{type(foreground_img)}" given.')

    if type(mask) is str:
        mask = open(mask, 'L')

    if type(mask) is np.ndarray:
        mask = fromarray(mask).convert('L')

    if type(mask) is not Image and type(mask) is not JpegImageFile:
        raise Exception(f'Type of "mask" must be one of these types [{Image}, {JpegImageFile}, {np.ndarray}, str]. "{type(mask)}" given.')

    return composite(foreground_img, background_img, mask=mask)


def prepare_for_prediction_single(img: str, shape=(768, 768), as_array=True):
    """ Loads and resizes the image to given shape (default: 768, 768) and returns as a numpy array.
    """

    img = cv2.imread(img)
    img = img_as_float(cv2.resize(img, shape)) / 255.0

    out = img
    if as_array:
        out = np.array([out])

    return out


def prepare_for_prediction(imgs, shape=(768, 768)):
    """ Loads and resizes each image in "imgs" to a given (default: 768, 768) shape and returns the result as a numpy array.
    """

    out = []
    for img in imgs:
        _img = prepare_for_prediction_single(img, shape=shape, as_array=False)

        out.append(_img)

    return np.array(out)


def remove_lonely_small_objects(grayscale):
    """ Removes lonely small objects from binary mask, the \"grayscale\" parameter must be a grayscale. """

    binary = np.where(grayscale > 0.1, 1, 0)
    processed = remove_small_objects(binary.astype(bool))

    mask_x, mask_y = np.where(processed == 0)
    grayscale[mask_x, mask_y] = 0

    return grayscale


def remove_smaller_objects(grayscale):
    """ Removes all objects from binary mask except the biggest one. """

    inter = cv2.morphologyEx(grayscale, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    cnts, _ = cv2.findContours(inter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = max(cnts, key=cv2.contourArea)

    out = np.zeros(grayscale.shape, np.uint8)
    cv2.drawContours(out, [cnt], -1, 255, cv2.FILLED)
    out = cv2.bitwise_and(grayscale, out)

    return out


def fill_holes(gray: np.ndarray, min=200, max=255):
    """ Removes black spots in a binary object. """

    _, thresh = cv2.threshold(gray, min, max, cv2.THRESH_BINARY)
    gray = binary_fill_holes(thresh)
    gray = img_as_uint(gray)

    return gray


def translate_image(img, x_shift: int, y_shift: int):
    """ Translates image from a given x and y values. """

    a = 1
    b = 0
    c = x_shift
    d = 0
    e = 1
    f = y_shift

    return img.transform(img.size, AFFINE, (a, b, c, d, e, f))


def normalize_binary_img(img: np.ndarray):
    """ Re-converts binary mask image to original grayscale image. """

    _img = toimage(img, channel_axis=2)

    return np.array(_img)
