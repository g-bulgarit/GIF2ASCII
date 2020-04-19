import glob
from PIL import Image
import numpy as np
file_list = glob.glob("Sprites/*")


def get_sprite_dict():
    sprite_dict = {}
    for filename in file_list:
        image_file = Image.open(filename)
        gray_image = image_file.convert("L")
        image_matrix = np.asarray(gray_image)
        avg_brightness = image_matrix.sum()//image_matrix.shape[0]**2
        sprite_dict[avg_brightness] = gray_image
        image_file.close()

    return sprite_dict


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


def matrix_values():
    sprite_dict = get_sprite_dict()
    gray_image_resized = gray_resized("grisi.jpg", 95)
    sprite_dict_values = list(sprite_dict.keys())
    sprite_dict_values.sort(reverse=True)
    gray_image_resized_matrix = np.asarray(gray_image_resized)
    gray_image_resized_matrix_copy = gray_image_resized_matrix.copy()
    for i in range(len(sprite_dict_values)):
        gray_image_resized_matrix_copy[gray_image_resized_matrix < sprite_dict_values[i]] = sprite_dict_values[i]
    return gray_image_resized_matrix_copy


def create_frame(image_matrix):
    sprite_dict = get_sprite_dict()
    img_hight = image_matrix.shape[0]
    img_width = image_matrix.shape[1]
    img_size = (img_hight*50, img_width*50)
    output_img = Image.new('L', img_size, color=0)
    for row in range(img_hight):
        for col in range(img_width):
            value = image_matrix[row][col]
            output_img.paste(sprite_dict[value],box=(row*50,col*50))
    return output_img


def main():
    q = matrix_values()
    temp = create_frame(q)
    my_dict = get_sprite_dict()
    temp.show()
if __name__ == "__main__":
    main()
