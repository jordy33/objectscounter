# People-Counter


### Hardware Requirements

NVIDIA Jetson with CSI Camera (Raspberry pi v2)

### Procedure

* Grab a frame
* Convert frame to gray
* Blur the frame
* Initialize a master frame
* Do a Delta frame (Differences)
* Do a threshold frame
* Dilate the thresholded image to fill in holes
* Find contours on thresholded image
* Make coutour frame
* Target contours
* Check no strictly increasing numbers in (Y) Axis Determine direction
* Calculate in / outs (Store every point in an array)
* Write on screen target simbol
* Write on screen in / outs 
