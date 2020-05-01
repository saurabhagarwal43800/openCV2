import os
import smtplib
import cv2
import numpy as np

# Remember before using this program:
# 1. Create your environment variables in local system for id and password
# 2. Go to myaccounts.google.com/lesssecureapps, turn it on before using

def face_detect():
    cap=cv2.VideoCapture(0) # To access the camera
    face_model=cv2.CascadeClassifier('haarcascade_frontalface_default.xml') # To load face model
    eye_model=cv2.CascadeClassifier('haarcascade_eye.xml') # To load haarcascade eye model
    count="No. of Faces 0"
    while True:

        ret,photo=cap.read() # To capture image
        gray=cv2.cvtColor(photo,cv2.COLOR_BGR2GRAY) # Converting original image to gray image
        faces=face_model.detectMultiScale(gray,1.3,5) # To detect faces

        for x,y,w,h in faces:
            cv2.rectangle(photo,(x,y),(x+w,y+h),[0,255,0],3)
            count="No. of Faces "+str(len(faces))
            roi_gray=gray[y:y+h,x:x+w] # To store position of eyes in gray image
            roi_color=photo[y:y+h,x:x+w] # To store position of eyes in original image
            eyes=eye_model.detectMultiScale(roi_gray) # To detect eyes from gray image
            for ex,ey,ew,eh in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),3) # To draw rectangle on eyes
                photo=cv2.putText(photo, count, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
        
        cv2.imshow("Eye detector",photo)
        if cv2.waitKey(1)==13:
            break

    cv2.destroyAllWindows()
    cap.release()
    return count

def sendmail(count):
    EMAIL_ADDRESS=os.environ.get("EMAIL_USER")
    EMAIL_PASSWORD=os.environ.get("EMAIL_PASS")

    with smtplib.SMTP('smtp.gmail.com:587') as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject="Counting faces in opencv python"
        body = f"Hey!! \nWhats'up? \n {count}"
        msg = f'Subject: {subject} \n\n{body}'

        smtp.sendmail(EMAIL_ADDRESS,"500060783@stu.upes.ac.in", msg)
    return "Mail Send Successfully"


if __name__=="__main__":
    c=face_detect()
    c1=c.split(" ")
    if int(c1[-1])>0:
        message=sendmail(c)
        print(message)
    else:
        print("NO face detected")
    

