import cv2 as cv
import numpy as np

# Using threshold, we can filter out duplicated frames
def select_img_from_video(video_file, board_pattern, threshold=30):
    video = cv.VideoCapture(video_file)
    img_select = []
    prev_gray = None

    while True: 
        valid, frame = video.read()
        if not valid:
            break

        # Detect the chessboard's corners 
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        complete, _ = cv.findChessboardCornersSB(gray, board_pattern)

        if complete:
            if prev_gray is None: # To get the different frame in the video, so 
                img_select.append(frame)
                prev_gray = gray
            else:
                # Get the difference of the frames
                diff = cv.absdiff(gray, prev_gray)
                score = np.mean(diff)

                if score > threshold:
                    img_select.append(frame)
                    prev_gray = gray
                    print(f"Append ({len(img_select)}) | diff={score:.2f}")
        
        if len(img_select) >= 20: # This is the important part of my code that set a number of the frames to get. I set the number 5, 20, No limit(95)
            break

    return img_select

def calib_camera_from_chessboard(images, board_pattern, board_cellsize, K=None, dist_coeff=None, calib_flags=None):
    img_points = []
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            img_points.append(pts)
    assert len(img_points) > 0
    obj_pts = [[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])]
    obj_points = [np.array(obj_pts, dtype=np.float32) * board_cellsize] * len(img_points) 

    return cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], K, dist_coeff, flags=calib_flags)

# Call the video file to get the frames
video_file = "chessboard.mp4"

# Get the frames in the video
images = select_img_from_video(video_file, (8,6))
print("A number of the frames: ", len(images))

# Debugging
board_pattern = (8,6) # A number of the checker's corners
board_cellsize = 25 # Cell's size (mm), but this is not important in calibration (this is important in 3D, AR, GPS...etc.)

for img in images:
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    complete, pts = cv.findChessboardCorners(gray, board_pattern)

    print("Detected:", complete) # To check which image is True or False to detect in this code

ret, K, dist, rvecs, tvecs = calib_camera_from_chessboard(
    images,
    board_pattern,
    board_cellsize
)

print("K:\n", K)
print("dist:\n", dist)
print("error:", ret)