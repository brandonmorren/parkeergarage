#https://stackoverflow.com/questions/52029233/how-to-make-usb-camera-work-with-opencv
import cv2
import pytesseract
from PIL import Image
import numpy as np
import time

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0


#functions

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    
    key = cv2.waitKey(1) & 0xFF
    #rawCapture.truncate(0)
    
    
    if key == ord("s"):
        img_name = "opencv_frame_{}.png".format(img_counter)
        frame=get_grayscale(frame)
        cv2.imwrite(img_name, frame)
        img=Image.open(r'/home/pi/opencv_frame_{}.png'.format(img_counter))
        
        text = pytesseract.image_to_string(img)
        print(text)
        #cv2.imshow("Frame", image)
        cv2.waitKey(0)
        img_counter += 1
        break
    
    if not ret:
        print("failed to grab frame")
        break
    

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
