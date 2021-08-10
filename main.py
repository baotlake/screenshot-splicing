#! python3

import os
import sys
from PIL import Image
from image import get_vertical_color
from core import find_same_subsequences, find_max_subsequence

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


path = sys.argv[1]
img = Image.open(path)
img = img.convert('L')

path2 = sys.argv[2]
img2 = Image.open(path2)
img2 = img2.convert('L')

i = 0
x = 1
# while i < 1:
color_list_1 = get_vertical_color(img, x)
color_list_2 = get_vertical_color(img2, x)

print(find_same_subsequences(color_list_1, color_list_2))
print(find_max_subsequence(color_list_1, color_list_2))

i += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/