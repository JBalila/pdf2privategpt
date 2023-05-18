# Image Pre-Processing Functions to improve output accurracy
from libraryHeaders import *

# Convert to grayscale
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Remove noise
def remove_noise(img):
    return cv2.medianBlur(img, 5)

# Thresholding
def threshold(img):
    # return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# Dilation
def dilate(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(img, kernel, iterations=1)

# Erosion
def erode(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(img, kernel, iterations=1)

# Opening -- erosion followed by a dilation
def opening(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# Canny edge detection
def canny(img):
    return cv2.Canny(img, 100, 200)

# Skew correction
def deskew(img):
    coords = np.column_stack(np.where(img > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = img.shape[:2]
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# Template matching
def match_template(img, template):
    return cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

# Preprocesses <img> and produces binary output
def convert_img2bin(img):
    # Convert the image into a grayscale image
    output_img = grayscale(img)
    
    # Invert the grayscale image by flipping pixel values
    # All pixels that are grater than 0 are set to 0 and all pixels that are = to 0 are set to 255
    output_img = cv2.bitwise_not(output_img)

    # Converting image to binary by Thresholding in order to show a clear separation between white and blacl pixels
    output_img = threshold(output_img)

    return output_img