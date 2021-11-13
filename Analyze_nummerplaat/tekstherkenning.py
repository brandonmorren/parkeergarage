#https://stackoverflow.com/questions/52029233/how-to-make-usb-camera-work-with-opencv
#https://maker.pro/raspberry-pi/tutorial/optical-character-recognizer-using-raspberry-pi-with-opencv-and-tesseract

import cv2
import pytesseract
from PIL import Image


cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    
    image = cam.read()
    key = cv2.waitKey(1) & 0xFF
    #rawCapture.truncate(0)
    
    if key == ord("s"):
        img_name = "opencv_frame_{}.png".format(img_counter)
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
    cv2.imshow("test", frame)

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