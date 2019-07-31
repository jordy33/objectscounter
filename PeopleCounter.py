import argparse
import datetime
import imutils
import math
import cv2
import numpy as np
# Based: https://www.youtube.com/watch?v=BDt0-F3PL8U
#video='nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)20/1 ! nvvidconv flip-method=2 ! video/x-raw, width=(int)1280, height=(int)720, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink'
video='nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)NV12, framerate=(fraction)20/1 ! nvvidconv flip-method=2 ! video/x-raw, width=(int)640, height=(int)480, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink'

width = 300
hight = 225
textIn = 0
textOut = 0

def testIntersectionIn(x, y):
    res = -450 * x + 400 * y + 157500
    if ((res >= -550) and (res < 550)):
        print(str(res))
        return True
    return False


def testIntersectionOut(x, y):
    res = -450 * x + 400 * y + 180000
    if ((res >= -550) and (res <= 550)):
        print(str(res))
        return True

    return False


if __name__ == "__main__":

    camera = cv2.VideoCapture(video, cv2.CAP_GSTREAMER)

    firstFrame = None
    if camera.isOpened():
        window_handle = cv2.namedWindow('CSI Camera', cv2.WINDOW_AUTOSIZE)
        # loop over the frames of the video
        while cv2.getWindowProperty('CSI Camera',0) >= 0:
            # grab the current frame and initialize the occupied/unoccupied
            # text
            (grabbed, frame) = camera.read()
            text = "Unoccupied"

            # if the frame could not be grabbed, then we have reached the end
            # of the video
            if not grabbed:
                break

            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=width)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the first frame is None, initialize it
            if firstFrame is None:
                firstFrame = gray
                continue

            # compute the absolute difference between the current frame and
            # first frame to show only the pixels that have changed
            frameDelta = cv2.absdiff(firstFrame, gray)
            # Every value that goes from 25 goes to 255
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image. What ever shape there is and expands out a little
            thresh = cv2.dilate(thresh, None, iterations=2)
            # The contours are the red shapes. The countours is the shape build arround the blob where is the same color or shape
            # The red dos is the centroid or middle mass (middle area portion)

            #cv2.line(frame, (width // 2, 0), (width, 450), (250, 0, 1), 2)  # blue line
            #cv2.line(frame, (width // 2 - 50, 0), (width - 50, 450), (0, 0, 255), 2)  # red line
            #(H, W) = frame.shape[:2]
            #print(W)

            cv2.line(frame, (0, hight // 2), (width, hight // 2), (0, 255, 255), 2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            targets = []
            # loop over the contours
            for c in cnts:
                print(c)
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < 12000:
                    continue
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                rx = x + int(w / 2)
                ry = y + int(h / 2)
                ca = cv2.contourArea(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                targets.append((rx, ry, ca))


                rectagleCenterPont = ((x + x + w) // 2, (y + y + h) // 2)
                cv2.circle(frame, rectagleCenterPont, 1, (0, 0, 255), 5)

                if (testIntersectionIn((x + x + w) // 2, (y + y + h) // 2)):
                    textIn += 1

                if (testIntersectionOut((x + x + w) // 2, (y + y + h) // 2)):
                    textOut += 1

                # draw the text and timestamp on the frame

                # show the frame and record if the user presses a key
                #cv2.imshow("Thresh", thresh)
                #cv2.imshow("Frame Delta", frameDelta)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # make target
            area = sum([x[2] for x in targets])
            mx = 0
            my = 0
            if targets:
                for x, y, a in targets:
                    mx += x
                    my += y
                mx = int(round(mx / len(targets), 0))
                my = int(round(my / len(targets), 0))

            cv2.putText(frame, "In: {}".format(str(textIn)), (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, "Out: {}".format(str(textOut)), (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            #cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            cv2.imshow("CSI Camera", frame)
            keyCode = cv2.waitKey(30) & 0xff
            # Stop the program on the ESC key
            if keyCode == 27:
                break
    else:
        print ('Unable to open camera')
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
