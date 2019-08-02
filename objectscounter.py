import imutils
import cv2
import numpy as np

width = 300
hight = 220
textIn = 0
textOut = 0
points = []
# Based: https://www.youtube.com/watch?v=BDt0-F3PL8U
video = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)NV12, framerate=(fraction)20/1 ! nvvidconv flip-method=2 ! video/x-raw, width=(int)640, height=(int)480, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink'

if __name__ == "__main__":

    camera = cv2.VideoCapture(video, cv2.CAP_GSTREAMER)

    master = None

    if camera.isOpened():
        window_handle = cv2.namedWindow('CSI Camera', cv2.WINDOW_AUTOSIZE)
        # loop over the frames of the video
        while cv2.getWindowProperty('CSI Camera', 0) >= 0:
            # grab the current frame and initialize the occupied/unoccupied
            # text
            # grab a frame
            (grabbed, frame0) = camera.read()

            # end of feed
            if not grabbed:
                break
            frame0 = imutils.resize(frame0, width=width)
            # gray frame
            frame1 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)

            # blur frame
            frame2 = cv2.GaussianBlur(frame1, (21, 21), 0)

            # initialize master
            if master is None:
                master = frame2
                continue

            # delta frame
            frame3 = cv2.absdiff(master, frame2)

            # threshold frame
            frame4 = cv2.threshold(frame3, 15, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes
            kernel = np.ones((5, 5), np.uint8)
            frame5 = cv2.dilate(frame4, kernel, iterations=4)

            # find contours on thresholded image
            #contours = cv2.findContours(frame5.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = cv2.findContours(frame5.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

            # make coutour frame
            frame6 = frame0.copy()

            # target contours
            targets = []

            # loop over the contours
            for c in contours:

                # if the contour is too small, ignore it
                if cv2.contourArea(c) < 500:
                    continue

                # contour data
                M = cv2.moments(c)  # ;print( M )
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                x, y, w, h = cv2.boundingRect(c)
                rx = x + int(w / 2)
                ry = y + int(h / 2)
                ca = cv2.contourArea(c)

                # plot contours
                cv2.drawContours(frame6, [c], 0, (0, 0, 255), 2)
                cv2.rectangle(frame6, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame6, (cx, cy), 2, (0, 0, 255), 2)
                cv2.circle(frame6, (rx, ry), 2, (0, 255, 0), 2)

                # save target contours
                targets.append((rx, ry, ca))

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

            # plot target
            tr = 50
            frame7 = frame0.copy()
            if targets:
                cv2.circle(frame7, (mx, my), tr, (0, 0, 255, 0), 2)
                cv2.line(frame7, (mx - tr, my), (mx + tr, my), (0, 0, 255, 0), 2)
                cv2.line(frame7, (mx, my - tr), (mx, my + tr), (0, 0, 255, 0), 2)

            # Calculate in or out
            if my>0:
                points.append(my)
            if mx==0 and my==0 and len(points)>0:
                results=[]
                if len(points)>15:
                    for index in range (0,len(points)-1):
                        results.append(points[index]>points[index+1])
                    if results.count(False)>results.count(True):
                        textOut += 1
                    else:
                        textIn += 1
                points=[]

            # update master
            master = frame2
            cv2.line(frame7, (0, hight // 2), (width, hight // 2), (0, 255, 255), 2)
            cv2.putText(frame7, "In: {}".format(str(textIn)), (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame7, "Out: {}".format(str(textOut)), (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # display
            cv2.imshow("CSI Camera", frame7)

            # key delay and action
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key != 255:
                print('key:', [chr(key)])
    else:
        print('Unable to open camera')
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()

# ---- end code ----