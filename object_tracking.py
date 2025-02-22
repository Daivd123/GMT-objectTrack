import cv2
import time
import math
#fixed position of the hoop
p1 = 530
p2 = 300
#creating list to store all of the x, y values
xs = []
ys = []


video = cv2.VideoCapture("PRO-C119-Teacher-Boilerplate-main/bb3.mp4")

tracker = cv2.TrackerCSRT_create()

returned, img = video.read()

bbox = cv2.selectROI("Tracking", img, False)

tracker.init(img, bbox)
 
def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]),int(bbox[3])

    cv2.rectangle(img,(x,y),((x+w), (y+h)), (255,0,255), 3, 1)

    cv2.putText(img, "Tracking", (75, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

def goal_track(img,bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]),int(bbox[3])
#center points of box
#finding center to draw dots
    c1 = x + int(w/2)
    c2 = y + int(h/2)

    cv2.circle(img,(c1,c2), 2, (0,0,255),5)

    cv2.circle(img,(int(p1),int(p2)), 2,(0,255,0),3)

    # 2 stars = exponent
    #calculating distance
    dist = math.sqrt(((c1-p1)**2) + (c2-p2)**2)
    print(dist)

    if(dist<=20):
        cv2.putText(img, "Goal",(300,90), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    xs.append(c1)
    ys.append(c2)

    for i in range(len(xs) - 1):
        cv2.circle(img,(xs[i],ys[i]),2,(0,0,255),5)

while True:
    check,img = video.read()   

    success, bbox = tracker.update(img)
    if success:
        drawBox(img,bbox)
    else:
        cv2.putText(img, "Lost",(75, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        #call goal_track to say goal
        goal_track(img,bbox)

    cv2.imshow("result",img)
            
    key = cv2.waitKey(25)

    if key == 32:
        print("Stopped!")
        break


video.release()
cv2.destroyAllWindows()

