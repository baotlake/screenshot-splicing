from PIL import Image


# 返回图片指定列的灰度颜色值
def get_vertical_color(img: Image, x: int) -> list:
    color_list = []

    if img.width < x:
        return color_list

    for y in range(0, img.height):
        # print(img.getpixel((x, y)))
        color_list.append(img.getpixel((x, y)))

    return color_list
