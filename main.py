import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pyodbc
from matplotlib import pyplot as plt
path = 'Image' #Creating a path for our Images folder
Image=[] #Inserting all the image in an array
studentname=[] #Name of all the students
list_of_student=os.listdir(path) #creating a list of images present in the image path in list of
students
#print(list_of_student)
#seperating the name of images from our list to names only i.e splitting text and .jpg file :
for current_image in list_of_student:
image_read_current=cv2.imread(f'{path}/{current_image}') #Reading all the images under
variable imagereadcurrent
#inserting the current images in the Image[] array declared above using append in the
Image variable :
Image.append(image_read_current)
#assigning names to each images by splitting the 0th component(name of student) and
the 1st component(extension)
studentname.append(os.path.splitext(current_image)[0])
#print(studentname)
#GENERATING FACE ENCODINGS FOR N NUMBER OF IMAGES IN THE DATASET TO
PREVENT MULTIPLE ENCODINGS
#Creating A function named encodings
def encoder(Image): #passing Image as parameter (using encoding the dlib library encodes
the image into 128 different features)
encodedlist=[]
for image_access in Image:
encodedlist
img=cv2.cvtColor(image_access,cv2.COLOR_BGR2RGB) #since CV2 reads image in
BGR format we need to convert it into RGB
encode=face_recognition.face_encodings(image_access)[0]
encodedlist.append(encode)
return encodedlist
#print(encoder(Image))
#THIS FACE_ENCODINGS ATTRIBUTE USES HOG ALGORITHM (HOG
TRANSFORMATION) INOREDER TO ENCODE THE IMAGES INTO FEATURES
encodedvalues=encoder(Image)
if (encodedvalues != 0):
print("ENCODINGS OF IMAGES SUCCESSFULLY DONE")
def mark2(name_of_student,Date,Time): #CONNECTING TO SQL SERVER
connect=pyodbc.connect('Driver={SQL Server};'
'Server=LAPTOP-OK0O9F1M\SQLEXPRESS;'
'Database=test;'
'Trusted_Connection=yes;')
cursor=connect.cursor()
sql='''insert into test.dbo.Attendance1(Name,Date,Time) values(?, ?, ?)'''
val=(name_of_student,Date,Time)
cursor.execute(sql,val)
connect.commit()
#CAPTURING LIVE VIDEO USING CV2:
CAM=cv2.VideoCapture(0) #Zero is used for capturing videos live:
Status="Absent"
while True :
ret,frame=CAM.read()
#The resolution of some camera maybe more for some users and less for others thus we
need to resize it into a standard resolution
student_faces=cv2.resize(frame,(0,0),None,0.25,0.25) #Setting Destination to None and
decreasing the size by 1/4 in both X and Y
#There Occurs a small problem here that since the video is captured from the camera
itself the format is BGR thus we need to convert it into RGB
student_faces=cv2.cvtColor(student_faces,cv2.COLOR_BGR2RGB)
#FINDING OUT FACE LOCATIONS OF EACH IMAGES:
face_finder=face_recognition.face_locations(student_faces)#SEARCHES FACES IN THE
CURRENT FRAME OF A VIDEO
face_encoder=face_recognition.face_encodings(student_faces,face_finder)#encodes
current frame into 128 features
#USING THE FACE_FINDER AND FACE_ENCODER VARIABLES WE MAtCH FACES
WITH THE PICTURES:
for encode_the_face , face_location in zip(face_encoder,face_finder):
face_match=face_recognition.compare_faces(encodedvalues,encode_the_face)#Compare_
faces attribute uses two parameters our encoded list which has face features and
encode_the_face variable which stores the encoded values from camera
#CALCULATING FACE DISTANCES
face_distance=face_recognition.face_distance(encodedvalues,encode_the_face)#Face_dist
ance attribute also uses encoded_values form our training image and encoded values
captured in real time
#IF FACE_DISTANCE IS LESS THEN FACES ARE MATCHED IF FACE DISTANCE IS
MORE FACES ARE NOT MATCHED:
#CALCULATING DISTANCE BETWEEN TRAINING IMAGE AND REAL TIME FRAME :
matched_reference=np.argmin(face_distance) #FINDS OUT THE INDEX VALUE OF
THE MINIMUM VALUE INSIDE FACE_DISTANCE:
if face_match[matched_reference]: #TO CHECK IF THE FACE CAPTURED BY
CAMERA AND ITS ENCODED VALUE MATCHES WITH THE ENCODED VALUE OF OUR
TRAINING IMAGE:
name_of_student=studentname[matched_reference].upper()
print(name_of_student)
#(THIS WILL RECOGNIZE ME :)
#CREATING FRAMES AROUND THE FACE
y1,x2,y2,x1=face_location
y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)
cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
cv2.putText(frame,name_of_student,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,2
55,255),2)
Time=datetime.now().time()
Date=datetime.now().date()
if name_of_student!=Status:
mark2(name_of_student,str(Date),str(Time))
Status=name_of_student
cv2.imshow('Frames',frame)
if cv2.waitKey(1)& 0xF==ord('q'):
break
CAM.release()
cv2.destroyAllWindows()
