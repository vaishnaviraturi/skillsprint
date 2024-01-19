import cv2
import os
import numpy as np

haar_file='haarcascade_frontalface_default (1).xml'
datasets='C:/Users/Vaishnavi Raturi/PycharmProjects/pythonProject/facedetect/dataset/'
(images,labels,names,id)=([],[],{},0)
for(subdirs,dirs,files) in os.walk(datasets):
    for subdir in dirs:
        names[id]=subdirs
        subjectpath=os.path.join(datasets,subdir)
        for filename in os.listdir(subjectpath):
            path=os.path.join(subjectpath,filename)
            label=id
            images.append(cv2.imread(path,0))
            labels.append(int(label))
        id=id+1

(images,labels)=[np.array(lists) for lists in [images,labels]]
model=cv2.face.LBPHFaceRecognizer_create()
model.train(images,labels)


face_cascade = cv2.CascadeClassifier(haar_file)
cap = cv2.VideoCapture(0)
# returns true or false (if the camera is on or not)
# print("Webcam is open? ", cap.isOpened())
# # wait for the camera to turn on (just to be safe, in case the camera needs time to load up)
# time.sleep(2)
# #Takes pictures of detected face and saves them
# count = 1
# print("Taking pictures...")
# this takes 100 pictures of your face. Change this number if you want.
# Having too many images, however, might slow down the program
while True:
    # im = camera stream
    ret, frame= cap.read()
    # if it recieves something from the webcam...
    if ret == True:
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect face using the haar cascade file
        faces = face_cascade.detectMultiScale(img_gray, 1.3, 4)  #(source,scale,min_neighbours)
        for (x,y,w,h) in faces:
            # draws a rectangle around your face when taking pictures
            # this is to create a ROI (region of interest) so it only takes pictures of your face
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            # define 'face' as the inside of the rectangle we made above and make it grayscale
            face = img_gray[y:y + h, x:x + w]
            # resize the face images to the size of the 'face' variable above (i.e: area captured inside of the rectangle)
            face_resize = cv2.resize(face, (640,488))
            prediction=model.predict(face_resize)
            if prediction[1]<74:
                cv2.putText(frame,'%s'%(names[prediction[0]].strip()),(x+5,(y+25+h)),cv2.FONT_HERSHEY_PLAIN,1.5,(20,185,20),2)
            else:
                cv2.putText(frame,"Unknown",(x+5,(y+25+h)),cv2.FONT_HERSHEY_PLAIN,1.5,(65,65,255),2)

            cv2.imshow("Face Recognition",frame)
            if cv2.waitKey(1)==ord("q"):
                break
cap.release()
cv2.destroyAllWindows()
