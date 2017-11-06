# vision-training

Environment setup (FOR TRAINING):

- OpenCV 2.4.13 with Python 2.7 bindings
- [python-v4l2capture](https://github.com/gebart/python-v4l2capture) (make sure to install from this repository and not using pip! They're incompatible)
- v4l-utils
- pynetworktables (`pip install pynetworktables`, we might swap this out for zeromq though, TBD)

## Season roadmap

- Hardware Setup
  - Coprocessor on the robot (either the Jetson TX1 or TK1)
    - Set up static IP and/or mDNS to make accessing it easy
  - Camera on the robot, with a green LED ring
- Retrieve images from camera
  - What is the best way to set camera properties such as exposure and ISO? Current solution using v4l2-ctl is messy
  - 
- Image processing
  - Convert to HSL/HSV (which is better and why?)
  - Normalize the entire image (or possibly only intensity/saturation channels, not sure) to make it robust to lighting changes (note: this is NOT contrast stretching, see [here](https://stackoverflow.com/questions/41118808/difference-between-contrast-stretching-and-histogram-equalization))
  - Threshold the image to identify the target (and maybe come up with an easy way to tune our threshold values? ex. sliders)
  - Morphology to reduce noise (see [here](https://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html), we are looking to perform an "open" operation to get rid of small flecks)
  - **Stretch goal:** perform all of most of these operations on the GPU (must be done using either C++ or Cython, OpenCV 2.4 does not support GPU operations directly through Python)
- Targeting
  - Find the contours in the image
  - Identify whether or not there are target contour(s) in the image. Methods to do this will vary by game
  - If there is a target in the image, extract useful information about its real world position:
    - Angle/distance to the camera (can be calculated using the known orientation of the camera, its field of view, and the dimensions of the target)
    - Full 3D pose (see [here](https://docs.opencv.org/3.1.0/d7/d53/tutorial_py_pose.html) for general information about what this means)
- Networking
  - Send targeting data from coprocessor to roboRIO
  - Can be done using NetworkTables, the official WPIlib solution for networking (see [here](https://wpilib.screenstepslive.com/s/3120/m/7912/l/80205-writing-a-simple-networktables-program-in-c-and-java-with-a-java-client-pc-side), there is also a third-party Python library available)
  - Some teams have problems using NetworkTables, and it isn't really the best for a number of reasons. Possibly investigate alternatives, such as the industry-standard [ZeroMQ](http://zeromq.org/)
- Automatic aiming
  - This happens on the roboRIO
  - Adjust robot position (could be angle or distance) using a PID loop ([What is a PID loop?](http://frc-pdr.readthedocs.io/en/latest/control/pid_control.html))
- Accessibility/Debug
  - Ensure code is commented well
  - Log statements everywhere
  - Coprocessor should host a web server which shows a live feed of the webcam. This will make debugging significantly easier, making it so we don't actually have to connect a monitor to the coprocessor to see what's going on.
    - We can use Flask in Python for this, see last year's code ([feed.py](https://github.com/FRCTeamPhoenix/visionworks2017/blob/master/feed.py))
