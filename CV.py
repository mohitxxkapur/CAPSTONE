#Mohit Kapur
#Developed for ELG4192 - Electrical Engineering Final Capstone Project

#this is the first iteration of the CV code.
#currently this uses an aglorithm developed by myself to determine the change in users position to send to the sensors
#The program uses facial recognition currently, as a machine learning algorithm for shoulders has not been developed for the project yet
#currently the script will constantly take the y value of a users face and move when the y position is outside of pre specified bounds
#only focus on front user

import cv2
import sys
import socket

val = 0
ylst = []

#function to append the face y value to a list for processing
def lst(ypos, yy):
    ypos.append(yy)

#the following three functions are for the actuators.
def moveUp():
    print("Move system up")
    #send signal to rpi
    client_socket.send(b"move system up")

def moveDown():
    print("Move system down")
    #send signal to rpi
    client_socket.send(b"move system down")

def stay():
    print("No need to move")
    #send signal to rpi
    client_socket.send(b"stay")

#Connecting to the server code running on the rpi
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('capstone.local', 12345)
client_socket.connect(server_address) #connecting to server


def moveCheck(lst):
    x = (len(lst)/2)
    A= lst[:len(lst)//2]
    B= lst[len(lst)//2:]
    #print(A)
    #print(B)
    a = sum(A)/len(A)
    b = sum(B)/len(B)
    #print(a,b)
    if a-b >= -5 and a-b <= 5 : #user didnt move much
        stay()
    elif a - b > 5: #user moved up
        moveUp()
    elif a - b < -5 :#user moved down
        moveDown()
    
    #to optimize this function: connect the camera to this script, determine the ideal positions and from there set the bounds accordingly
    #figure out what values actually entail movement, also look into updating the refresh rate. that might involve updating the bounds. 

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
    #No Face detected
    #print(str(len(faces)))
    if len(faces) == 0:
        #print("no face")
        stay()
    #Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y-35),(x+w, y), (0,255,0), -2)
        cv2.putText(frame,'face', (x, y-6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255),1)
        #print (y)
        #ypos.append(y)
        #print (ypos)

        #These two if statements are for checking the bounds of the detected face.
        if (y <= 25):
            moveUp()

        if (y >= 300):
            moveDown()
        
        if (len(ylst) < 100):
            if (len(ylst) == 1 or len(ylst) == 0):
                lst(ylst, y)
            else:
                i = len(ylst)
                lst(ylst, y)

        if len(ylst) == 100:
            moveCheck(ylst)

        if (len(ylst) == 100):
            #print("at 100: " + str(ylst)) 
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
client_socket.close()
video_capture.release()
cv2.destroyAllWindows()
