# Import Libraries
import cv2, os
import numpy as np


# Receive Image path and values
img_path = './paint.jpg'
filename, ext = os.path.splitext(os.path.basename(img_path))

# Read the recalled image
ori_img = cv2.imread(img_path)

#Function to place the 4 cordinates of the image
src = []


# Mouse callback handler
# Assigning 4 coordinates on the image to scan (With a mouse)
def mouse_handler(event, x, y, flags, param):
if event == cv2.EVENT_LBUTTONUP:
img = ori_img.copy()

src.append([x, y])

# Drawing green circles on mouse click for coordinates
for xx, yy in src:
cv2.circle(img, center=(xx, yy), radius=5, color=(0, 255, 0), thickness=-1, lineType=cv2.LINE_AA)

cv2.imshow('img', img)

# Extract the image based on the 4 coordinates and rearrange the image array through perspective transform
# Perspective transform
# There as to be '4' dots inorder for perspective transform to work

if len(src) == 4:
src_np = np.array(src, dtype=np.float32)

# Calculation the on the new image
# Uses the longer length from the height and width
# numpy.linalg.norm(a-b) = function that calculates the distance from point a to point b vectors

width = max(np.linalg.norm(src_np[0] - src_np[1]),
np.linalg.norm(src_np[2] - src_np[3]))
height = max(np.linalg.norm(src_np[0] - src_np[3]),
np.linalg.norm(src_np[1] - src_np[2]))

# Assigns the destination and size of the cropped scanned image
dst_np = np.array([
[0, 0],
[width, 0],
[width, height],
[0, height]
], dtype=np.float32)

#Receives the perspective transform matrix values
M = cv2.getPerspectiveTransform(src=src_np, dst=dst_np)

#
result = cv2.warpPerspective(ori_img, M=M, dsize=(width, height))

#show image results
cv2.imshow('result', result)

# Save image results
cv2.imwrite('./result/%s_result%s' % (filename, ext), result)


# Execution; Scan the ROI from the original image and display it
#main

# Call the window with the image (img)
cv2.namedWindow('img')

# Function that Callback mouse on the specific window(img)
cv2.setMouseCallback('img', mouse_handler)

#show the original image on the window
cv2.imshow('img', ori_img)
cv2.waitKey(0)
