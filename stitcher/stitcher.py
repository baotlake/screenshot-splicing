#! python3
import sys
import os
import imutils
import cv2

if len(sys.argv) <= 2:
    print('At least two pictures are required!')
    print(f'Usage: {sys.argv[0]} image1.png image2.png ...')
    sys.exit(0)

imagePaths = sys.argv[1:]
images = []
root_path = os.path.abspath(os.path.join(__file__, '../../'))

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
    # outputName = input("Input your desired filename for the output: ")
    cv2.imwrite(f"{root_path}/tmp/stitcher_output.png", stitched)

    # display the output stitched image to our screen
    print("[INFO] image stitching success...")
    # cv2.imshow("Stitched", stitched)
    # cv2.waitKey(0)

# otherwise the stitching failed, likely due to not enough keypoints)
# being detected
else:
    print("[INFO] image stitching failed ({})".format(status))
