import cv2
import numpy as np
import smtplib
import serial
import os, time


 
#video_file = "video_1.mp4"
video = cv2.VideoCapture(0)
 
while True:
    (grabbed, frame) = video.read()
    if not grabbed:
        break
 
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
 
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
    
 
 
    output = cv2.bitwise_and(frame, hsv, mask=mask)
    no_red = cv2.countNonZero(mask)
    cv2.imshow("output", output)
    
    #print("output:", frame)
    if int(no_red) > 10000:
        print ('Fire detected')
        
        #sending email
        smtpUser = 'forhadreza1596@gmail.com'
        smtpPass = 'gutusmutus'

        toAdd = 'forhadreza.developer@gmail.com'
        fromAdd = smtpUser

        subject = 'Fire Alert'
        header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
        body = 'Fire Detected at this place: https://maps.google.com/?q=23.807756,90.383120'


        s = smtplib.SMTP('smtp.gmail.com',587) 

        s.ehlo()
        s.starttls()
        s.ehlo()

        s.login(smtpUser, smtpPass)
        s.sendmail(fromAdd, toAdd, header + '\n\n' + body)

        s.quit()
        
        #sending sms
        port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
        port.write('AT'+'\r\n')
        rcv = port.read(10)
        print rcv

        port.write('AT+CMGF=1'+'\r\n')
        rcv = port.read(10)
        print rcv

        port.write('AT+CMGS="8801673722190"'+'\r\n')
        rcv = port.read(10)
        print rcv
        time.sleep(1)

        port.write('Fire Detected at this place: https://maps.google.com/?q=23.807756,90.383120'+'\r\n')
        rcv = port.read(10)
        print rcv

        port.write("\x1A")
        for i in range(10):
            rcv = port.read(10)
            print rcv
        
        break

    #print(int(no_red))
   #print("output:".format(mask))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cv2.destroyAllWindows()
video.release()
