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
        sprite_dict[avg_brightness] = gray_image.resize((20, 20))
        image_file.close()

    return sprite_dict


def gray_resized(in_image, percent):
    pic_file = Image.open(in_image)
    gray_image = pic_file.convert("L")
    width, height = gray_image.size
    percent_left = 100 - percent
    new_width = (width * percent_left // 100) // 20 * 20
    new_height = (height * percent_left // 100) // 20 * 20
    new_size = (new_width, new_height)
    gray_image_resized = gray_image.resize(new_size)
    return gray_image_resized


def matrix_values(input_img, sprites, resize_value):
    gray_image_resized = gray_resized(input_img, resize_value)
    sprite_dict_values = list(sprites.keys())
    sprite_dict_values.sort(reverse=True)
    gray_image_resized_matrix = np.asarray(gray_image_resized)
    gray_image_resized_matrix_copy = gray_image_resized_matrix.copy()
    for i in range(len(sprite_dict_values)):
        gray_image_resized_matrix_copy[gray_image_resized_matrix < sprite_dict_values[i]] = sprite_dict_values[i]
    return gray_image_resized_matrix_copy


def create_frame(image_matrix, sprites):
    img_height = image_matrix.shape[0]
    img_width = image_matrix.shape[1]
    img_size = (img_width * 20, img_height * 20)
    output_img = Image.new('L', img_size, color=0)
    for row in range(img_height):
        for col in range(img_width):
            value = image_matrix[row][col]
            output_img.paste(sprites[value], box=(col * 20, row * 20))
    return output_img


def main():
    img_path = "Koala.jpg"
    sprite_dictionary = get_sprite_dict()
    color_matrix = matrix_values(img_path, sprite_dictionary, 85)

    constructed_frame = create_frame(color_matrix, sprite_dictionary)
    constructed_frame.show()


if __name__ == "__main__":
    main()
