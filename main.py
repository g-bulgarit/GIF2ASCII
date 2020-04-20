import os
import glob
from PIL import Image
import numpy as np
import imageio
from gooey import Gooey, GooeyParser


def get_sprite_dict(sprite_size=50):
    # Load all sprites from the sprite folder,
    # Get the image objects and their grayscale values into a dictionary and return it.
    sprite_dict = {}
    file_list = glob.glob("Sprites/*")

    for filename in file_list:
        image_file = Image.open(filename)
        gray_image = image_file.convert("L")
        image_matrix = np.asarray(gray_image)
        avg_brightness = image_matrix.sum()//image_matrix.shape[0]**2
        sprite_dict[avg_brightness] = gray_image.resize((sprite_size, sprite_size))
        image_file.close()

    return sprite_dict


def sort_filenames(st):
    # Function to sort lists by filenames as integers,
    # instead of in lexicographical order.
    # To be used as key= in the .sort() method.
    return int(st.split("\\")[-1].strip(".gif"))


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


def extract_frames(in_gif, out_folder):
    # Split :in_gif: to separate .gif files containing only one frame.
    # Save all these new files in :out_folder:.

    frame = Image.open(in_gif)
    frame_number = 0
    while frame:
        frame.save('%s/%s.gif' % (out_folder, frame_number), 'GIF')
        frame_number += 1
        try:
            frame.seek(frame_number)
        except EOFError:
            break
    return True


def delete_gifs(path):
    files_to_delete = glob.glob(path + "*.gif")
    for file in files_to_delete:
        os.remove(file)


def frames_to_ascii(path, sprite_dictionary, out_path, scale_down):
    # Convert single-frame gifs from :path: to ascii-fied pictures.
    # Optionally, scale down the sprites used to reduce image size.

    # Read and sort our images to ascii-fy.
    path += "/*"
    frame_list = glob.glob(path)
    frame_list.sort(key=lambda x: sort_filenames(x))

    # For each image, ascii-fy and save the result in :out_path:.
    for number, filename in enumerate(frame_list):
        ascii_frame_matrix = matrix_values(filename, sprite_dictionary, scale_down)
        constructed_frame = create_frame(ascii_frame_matrix, sprite_dictionary)
        out_file_name = out_path + "/" + str(number) + ".gif"
        constructed_frame.save(out_file_name)


def create_gif(folder):
    # Take a :folder: of images and make a gif out of it.

    images = []
    # Read and sort the images in the input folder.
    frame_list = glob.glob(folder + ".gif")
    frame_list.sort(key=lambda x: sort_filenames(x))

    # Append the images (as imageio objects) to a list
    for filename in frame_list:
        images.append(imageio.imread(filename))

    # Turn the list into a gif :)
    imageio.mimsave('output.gif', images)

    # Delete everything gif in our folders.
    delete_gifs("ascii_frames/")
    delete_gifs("gif_frames/")


@Gooey(language="english")
def main():
    parser = GooeyParser(description="Select an image to process")
    parser.add_argument('path', metavar='File', widget="FileChooser", help="Browse to your file.")
    parser.add_argument('--scale_down',
                        metavar="Scale Down %",
                        type=int,
                        default=50,
                        gooey_options={
                            'validator': {
                                'test': '0 < int(user_input) < 100',
                                'message': 'Scale down % can\'t be negative or larger than 100%!'
                            }
                        }
                        )
    parser.add_argument('--tile_size',
                        metavar="tile size in pixels",
                        type=int,
                        default=20,
                        gooey_options={
                            'validator': {
                                'test': '0 < int(user_input) < 100',
                                'message': 'Tile can\'t be negative or larger than 100!'
                            }
                        }
                        )
    arguments = parser.parse_args()
    path = arguments.path
    scale_down = arguments.scale_down
    tile_size = arguments.tile_size
    sprite_dictionary = get_sprite_dict(tile_size)
    extract_frames(path, "gif_frames")
    frames_to_ascii("gif_frames", sprite_dictionary, "ascii_frames", scale_down)
    create_gif("ascii_frames/*")


if __name__ == "__main__":
    main()
