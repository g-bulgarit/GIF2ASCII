def get_sprite_dict():
    import glob
    from PIL import Image
    import numpy as np

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
