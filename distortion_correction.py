import cv2 as cv
import numpy as np

# I will use 20-frame version, because this version is the most stable and has the fewer errors.

K = np.array([ 
    [1650.56076, 0.0, 535.530111],
    [0.0, 1648.70566, 969.272973],
    [0.0, 0.0, 1.0]
])

dist = np.array([0.156832604, -0.0498690928, 0.000298108179, -0.00133517438, -1.69994992])

video = cv.VideoCapture("chessboard.mp4")

map1, map2 = None, None

while True:
    ret, frame = video.read()
    if not ret:
        break

    if map1 is None:
        h, w = frame.shape[:2]
        map1, map2 = cv.initUndistortRectifyMap(
            K, dist, None, None, (w, h), cv.CV_32FC1
        )

    undistorted = cv.remap(frame, map1, map2, interpolation=cv.INTER_LINEAR)

    diff = cv.absdiff(frame, undistorted)
    diff_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    _, diff_mask = cv.threshold(diff_gray, 10, 255, cv.THRESH_BINARY)
    diff_colored = cv.cvtColor(diff_mask, cv.COLOR_GRAY2BGR)

    # OG + Undistorted
    top = np.hstack([frame, undistorted])
    bottom = np.hstack([diff_colored, diff_colored])
    combined = np.vstack([top, bottom])

    # Show info with text
    cv.putText(combined, "Original | Undistorted", (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0), 1)
    cv.putText(combined, "Difference Highlight", (10, h+25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 255), 1)

    # Show the video
    cv.imshow("Distortion Correction Visualization", combined)

    if cv.waitKey(1) == 27:
        break

video.release()
cv.destroyAllWindows()