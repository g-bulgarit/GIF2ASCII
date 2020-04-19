import glob
from PIL import Image
import numpy as np


def get_sprite_dict():
    sprite_dict = {}
    file_list = glob.glob("Sprites/*")

    for filename in file_list:
        image_file = Image.open(filename)
        gray_image = image_file.convert("L")
        image_matrix = np.asarray(gray_image)
        avg_brightness = image_matrix.sum()//image_matrix.shape[0]**2
        sprite_dict[filename] = avg_brightness
        image_file.close()

    return sprite_dict


def main():
    classified_sprite = get_sprite_dict()
    print(classified_sprite)


if __name__ == "__main__":
    main()


def gray_resized(in_image, percent):
    pic_file = Image.open(in_image)
    gray_image = pic_file.convert("L")
    width, hight = gray_image.size
    percent_left = 100 - percent
    new_width = (width * percent_left // 100) // 50 * 50
    new_hight = (hight * percent_left // 100) // 50 * 50
    new_size = (new_width, new_hight)
    gray_image_resized = gray_image.resize(new_size)
    return gray_image_resized
