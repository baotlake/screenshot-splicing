# USAGE
# put your folder containing images you want to stitch into the images folder

# import the necessary packages
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2


# grab the paths to the input images and initialize our images list
inputFolder = input("Insert folder name contain images to be stitch: ")
print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images("img/"+inputFolder)))
images = []

# loop over the image paths, load each one, and add them to our
# images to stitch list
for imagePath in imagePaths:
	image = cv2.imread(imagePath)
	image = imutils.rotate_bound(image, 90)
	images.append(image)

# initialize OpenCV's image sticher object and then perform the image
# stitching
print("[INFO] stitching images...")
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)

# if the status is '0', then OpenCV successfully performed image
# stitching
if status == 0:
	# write the output stitched image to disk
	stitched = imutils.rotate_bound(stitched, 270)
	outputName = input("Input your desired filename for the output: ")
	cv2.imwrite(outputName+".png", stitched)

	# display the output stitched image to our screen
	print("[INFO] image stitching success...")
	cv2.imshow("Stitched", stitched)
	cv2.waitKey(0)

# otherwise the stitching failed, likely due to not enough keypoints)
# being detected
else:
	print("[INFO] image stitching failed ({})".format(status))