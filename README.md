Hand Movement Detection
============================================
By: Parimal Mehta @prmehta24 , Parth Panchal @Parth19499

The code can identify hand movements in a live videofeed(from a webcam). We have tried to identify the direction in which the hand is moving in all three axes - x, y and z (Up, Down, Left, Right, Closer, Farther).

We have based our program on @sashagaz's excellent Hand Detection program.

The code captures frames using a web camera and outputs a video which:

* Tells if the hand is detected
* If moving, what direction the hand is moving in



This project is written in Python 2.7. The following libraries are used in this project and necessary to be add to your computer:
1) Time - usually comes with Python 2.7
2) OpenCV (2.4.9) - http://docs.opencv.org/trunk/doc/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html
3) NumPy (1.8.0rc1) - http://www.numpy.org

The code is consist of a single file and can be executed from the commandline or terminal by calling: python HandMovementDetection.py

When running the python file, you can expect to see the real time frame from your camera with a bounding rectangle framing your hand.  The center mass of your hand will be labeled in the bounding rectangular.

The direction of hand movement will be written on the sides of the frame in white.

## Notes

* To increase accuracy of the detection, it is recommended to run the code in a bright light room. 

* The code can only detect one hand at a time. It would also be unable to recognise a partially occluded hand.

* The to use the hand color method to detect a hand from camera frames. A shortcoming of this method was that it would classify anything of skin color as a hand (including other body parts - head, elbow ). 

* It also needed a clear background to be able to detect a hand in the frame.


References:
opencv documentation http://docs.opencv.org/
[2] Skin Detection using HSV color space - V. A. Oliveira, A. Conci
[3] OpenCv Documentation - Miscellaneous Image Transformation
http://docs.opencv.org/modules/imgproc/doc/miscellaneous_transformations.html
[4] OpenCv Documentation - Morphological Operations http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
[5] Suzuki, S. and Abe, K., Topological Structural Analysis of Digitized Binary Images by Border Following. CVGIP 30 1, pp 32-46 (1985)


 
