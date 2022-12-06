#Mohit Kapur
#Developed for ELG4192 - Electrical Engineering Final Capstone Project

#this is the first iteration of the CV code.
#currently this uses an aglorithm developed by myself to determine the change in users position to send to the sensors
#The program uses facial recognition currently, as a machine learning algorithm for shoulders has not been developed for the project yet
#currently the script will constantly take the y value of a users face and move when the y position is outside of pre specified bounds
import cv2
import sys

val = 0
ylst = []


#function to append the face y value to a list for processing
def lst(ypos, yy):
    ypos.append(yy)


cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    imGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        imGray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    yyy = 0
    #Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y-35),(x+w, y), (0,255,0), -2)
        cv2.putText(frame,'face', (x, y-6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255),1)
        #print (y)
        #ypos.append(y)
        #print (ypos)
        if (len(ylst) < 100):
            if (len(ylst) == 1 or len(ylst) == 0):
                lst(ylst, y)
            else:
                i = len(ylst)
                lst(ylst, y)

        elif (len(ylst) == 100):
            #print("at 100: " + str(ylst)) all print statments are for debugging
            i = -1
            spare = []
            for i in range(50):
                lst(spare, ylst[-50+i])
            #print("finding last 50:" + str(spare))
            ylst = []
            for i in range(len(spare)):
                lst(ylst, spare[i])
            #print("new ylist: " + str(ylst))
            #print("spare: " + str(spare))
            spare = []

    
    #print (ylst)
        

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()