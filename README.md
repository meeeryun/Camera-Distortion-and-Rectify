# Camera-Distortion-and-Rectify
I show my video's distortion and rectify that distortion

In this project, I used OpenCV to analyze distortion in a chessboard video and performed distortion correction based on the extracted data.
--------------------------------------------------------------------------------------------------------------------------------------
1. camera_calibration.py

First, the function select_img_from_video takes three parameters: video file, board_pattern, and threshold.

To detect corner points and identify the chessboard pattern from the video file, I set board_pattern = (8, 6). This value may vary depending on the chessboard used, so it should be adjusted accordingly. Since the size of one cell in my chessboard is 25 mm, I set cellsize = 25. The threshold parameter is used to select high-quality frames.

The selected frames are stored in an array called img_select, which is returned by the function.

The most important part of this function is the condition:

```
if (len_select) >= 20
```

I experimented with three cases: 5 frames, 20 frames, and no limit.

Case 1: 5 frames
```
K:
[[1.66553871e+03 0.00000000e+00 5.27091992e+02]
 [0.00000000e+00 1.66064014e+03 9.67089399e+02]
 [0.00000000e+00 0.00000000e+00 1.00000000e+00]]

dist:
[[ 1.34010418e-01  5.67192870e-01 -1.04790274e-03 -2.62121819e-03 -6.47472397e+00]]

error: 0.2072
```
Although the error value (≈ 0.2) is very low and appears excellent, the distortion coefficients are clearly abnormal.
This suggests that the model is overfitting, meaning the numerical error is low but the result is not statistically reliable.

Case 2: 20 frames
K:
[[1.65056076e+03 0.00000000e+00 5.35530111e+02]
 [0.00000000e+00 1.64870566e+03 9.69272973e+02]
 [0.00000000e+00 0.00000000e+00 1.00000000e+00]]

dist:
[[ 1.56832604e-01 -4.98690928e-02  2.98108179e-04 -1.33517438e-03 -1.69994992e+00]]

error: 0.2309

In this case, the error is still low, and the distortion coefficients are within a reasonable range.
This indicates a good balance between accuracy and stability, making this configuration the most appropriate.

Case 3: No limit
K:
[[1.66154532e+03 0.00000000e+00 5.35913969e+02]
 [0.00000000e+00 1.66115195e+03 9.59435557e+02]
 [0.00000000e+00 0.00000000e+00 1.00000000e+00]]

dist:
[[ 1.84817711e-01 -2.28319713e-01 -1.00642962e-03 -1.18184632e-03 -1.31939361e+00]]

error: 0.3316

In this case, the error is higher than the previous cases, and the distortion coefficients are less stable.
Therefore, this configuration is also considered inappropriate.

✅ Conclusion (Calibration)

From the experiments, using 20 frames provides the best balance between stability and accuracy.

Additionally, debug print statements such as:

print("A number of ...")
print("Detected ...")

were intentionally kept to allow easy comparison between the three cases during compilation.

2. distortion_correction.py

This file performs distortion correction using the calibration results.
Among the tested configurations, I used the 20-frame version, as it was determined to be the most reliable.

The K and dist values obtained from the 20-frame calibration are passed into the function:

cv.initUndistortRectifyMap()

I used a mapping approach instead of directly applying the distortion formula because direct computation is slower.
The map precomputes pixel coordinate transformations, improving performance.

The parameter:

cv.CV_32FC1

specifies that the map uses 32-bit floating-point values.

Visualization Process
cv.absdiff() computes the absolute difference between the original and corrected images.
cv.cvtColor() converts the result to grayscale to highlight differences.
cv.threshold() emphasizes regions where the difference exceeds a certain threshold.

Finally:

np.hstack and np.vstack are used to arrange the images side by side.
Text such as "Original | Undistorted" is displayed.
The program can be terminated by pressing the ESC key.
