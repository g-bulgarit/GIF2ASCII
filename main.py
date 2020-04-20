import glob
from PIL import Image
import numpy as np


def get_sprite_dict(sprite_size=50):
    # Load all sprites from the sprite folder,
    # Get the image objects and their grayscale values into a dictionary and return it.
    sprite_dict = {}
    file_list = glob.glob("Sprites3/*")

    for filename in file_list:
        image_file = Image.open(filename)
        gray_image = image_file.convert("L")
        image_matrix = np.asarray(gray_image)
        avg_brightness = image_matrix.sum()//image_matrix.shape[0]**2
        sprite_dict[avg_brightness] = gray_image.resize((sprite_size, sprite_size))
        image_file.close()

    return sprite_dict


def grayscale_and_resize(in_image, percent):
    # Turn input image to grayscale, resize it by :percent: and return it as an image object.

    pic_file = Image.open(in_image)
    gray_image = pic_file.convert("L")
    width, height = gray_image.size
    percent_left = 100 - percent
    new_width = (width * percent_left // 100)
    new_height = (height * percent_left // 100)
    new_size = (new_width, new_height)
    gray_image_resized = gray_image.resize(new_size)
    return gray_image_resized


def matrix_values(input_img, sprites, resize_value):

    # Get a list of all grayscale values in our sprites
    sprite_dict_values = list(sprites.keys())
    sprite_dict_values.sort(reverse=True)

    # Load input image and get it to matrix form
    gs_img = grayscale_and_resize(input_img, resize_value)
    gs_matrix = np.asarray(gs_img)

    # Also create our output matrix as a copy
    out_matrix = gs_matrix.copy()

    # For each grayscale value in our sprites,
    # assign it's value to all pixels with a smaller value.
    for i in range(len(sprite_dict_values)):
        out_matrix[gs_matrix < sprite_dict_values[i]] = sprite_dict_values[i]

    return out_matrix


def create_frame(value_matrix, sprites):
    # Create a frame from a value-matrix and our sprites.
    img_height = value_matrix.shape[0]
    img_width = value_matrix.shape[1]

    # Get the size of a single sprite in order to calculate the new image size.
    sprite_size = sprites[list(sprites.keys())[0]].size[0]

    # Construct a new image.
    img_size = (img_width * sprite_size, img_height * sprite_size)
    output_img = Image.new('L', img_size, color=0)

    # Loop over the value matrix and assign sprites to the new image.
    for row in range(img_height):
        for col in range(img_width):
            value = value_matrix[row][col]
            output_img.paste(sprites[value], box=(col * sprite_size, row * sprite_size))
    return output_img


def main():
    img_path = "Koala.jpg"

    sprite_dictionary = get_sprite_dict(10)
    color_matrix = matrix_values(img_path, sprite_dictionary, 85)
    constructed_frame = create_frame(color_matrix, sprite_dictionary)
    constructed_frame.show()


if __name__ == "__main__":
    main()
