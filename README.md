# People-Counter

![](pc480.gif)
### Hardware Requirements

NVIDIA Jetson Nano with CSI Camera (Raspberry pi v2)

### Software Requirements

*Install Quartz in MacOS to enable Remote Graphic environment

*PyCharm (Enable remote interpreter)

*Install OpenCV 4.0.0 in the Nvidia Jetson Nano

```
https://github.com/mdegans/nano_build_opencv
```

### Know how 

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
* Calculate ins / outs 
* Write on screen target symbol
* Write on screen ins / outs 

### How to Run

Connect to the Nvidia Jetson nano
```
ssh -Y jetson@192.168.100.35
```
```
python3 peoplecounter.py
```
