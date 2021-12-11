import cv2
import numpy as np
import face_recognition
# Loading an image file into an numpy array

imgAnurodh=face_recognition.api.load_image_file("Image/Anurodh.jpeg")
imgAnurodh=cv2.cvtColor(imgAnurodh.cv2.COLOR_bgr2rgb)
imgAnurodhtrain=face_recognition.load_img_file("Image/Anurodhtrain.jpeg")
imgAnurodhtrain=cv2.cvtColor(imgAnurodhtrain.cv2.COLOR_bgr2rgb)


facelocation=face_recognition.face_location(imgAnurodh)[0]
encodeAnurodh=face_recognition.face_encodings(imgAnurodh)[0]
cv2.rectangle(imgAnurodh,(facelocation[3],facelocation[0],(facelocation[1]),facelocation[2]),(255,0,255),2)

#print (facelocation)

cv2.imshow("Anurodh",imgAnurodh)
cv2.imshow("Anurodhtrain",imgAnurodhtrain)
cv2.waitKeep(0)
