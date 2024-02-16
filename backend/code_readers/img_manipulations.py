""" """

import os
import cv2
from IPython.display import display, Image
from IPython import get_ipython

import numpy as np


def show(img, width):
    """
    shower of img-s INSIDE JUPYTER or in console, BUT not colab
    1) checks if called from ipython notebook or somehow else
    2) checks if given 'img' is already in 'width' size (if not, resizes 'img' to 'img_resized')
    3) for notebook - displays image via 'IPython.display(...)'
       for other call - shows image via cv2.imshow(...) and waits for window to be destroyed by user
    :param img:
    :param width:
    :return: --visual output--
    """

    try:
        shell = get_ipython().__class__.__name__  # Check if running in a Jupyter environment
        if shell == 'ZMQInteractiveShell':
            print("'show': Running in a Jupyter Notebook")
            # Your Jupyter-specific code here
            # Check if the image width is already the same as the desired width
            if img.shape[1] == width:
                display(Image(data=cv2.imencode('.png', img)[1]))
            else:
                # Resize the image to the desired width
                img_resized = cv2.resize(img, (width, int(img.shape[0] * (width / img.shape[1]))))
                display(Image(data=cv2.imencode('.png', img_resized)[1]))
        else:
            print("'show': Running in a different environment")
            if img.shape[1] == width:
                cv2.imshow(winname="window_name", mat=np.ndarray(img))
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                # Resize the image to the desired width
                img_resized = cv2.resize(img, (width, int(img.shape[0] * (width / img.shape[1]))))
                cv2.imshow(winname="window_name", mat=img_resized)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
    except NameError:  # try-except because not always IPython will tell us if it runs or not. Better safe than raising an error...
        print("'show':Running in a different environment")
        if img.shape[1] == width:
            cv2.imshow(winname="window_name", mat=np.ndarray(img))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            # Resize the image to the desired width
            img_resized = cv2.resize(img, (width, int(img.shape[0] * (width / img.shape[1]))))
            cv2.imshow(winname="window_name", mat=img_resized)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


def dirrename(path_to_dir: str, files: str, naming_pattern: str):
    """

    :param path_to_dir: path to directory with the files, in str format
    :param files: file ending to rename (for example, renaming jpg files -> files = "jpg")
    :param naming_pattern:
    :return:
    """
    if not os.path.exists(path_to_dir):
        print(f"The directory '{path_to_dir}' does not exist.")
        return

    if not os.path.isdir(path_to_dir):
        print(f"'{path_to_dir}' is not a directory.")
        return

    if not naming_pattern:
        print("Please provide a valid naming pattern.")
        return

    # Ensure the naming_pattern ends with a file extension separator (e.g., ".")
    # if not naming_pattern.endswith("."):
    #    naming_pattern += "."

    # Get a list of files in the directory with the specified format
    matching_files = [f for f in os.listdir(path_to_dir) if f.endswith(f".{files}")]

    if not matching_files:
        print(f"No files with the format '{files}' found in '{path_to_dir}'.")
        return

    # Rename the files with the given naming pattern
    for i, old_name in enumerate(matching_files, start=1):
        new_name = f"{naming_pattern}{i}.{files}"
        old_path = os.path.join(path_to_dir, old_name)
        new_path = os.path.join(path_to_dir, new_name)

        try:
            os.rename(old_path, new_path)
            print(f"Renamed '{old_name}' to '{new_name}'")
        except Exception as e:
            print(f"Failed to rename '{old_name}' to '{new_name}': {str(e)}")


def convert_png_to_jpg(path_to_dir):
    if not os.path.exists(path_to_dir):
        print(f"The directory '{path_to_dir}' does not exist.")
        return

    if not os.path.isdir(path_to_dir):
        print(f"'{path_to_dir}' is not a directory.")
        return

    for filename in os.listdir(path_to_dir):
        if filename.endswith(".png"):
            try:
                png_image = Image.open(os.path.join(path_to_dir, filename))
                jpg_filename = os.path.splitext(filename)[0] + ".jpg"
                jpg_image = png_image.convert("RGB")
                jpg_image.save(os.path.join(path_to_dir, jpg_filename))
                os.remove(os.path.join(path_to_dir, filename))
                print(f"Converted '{filename}' to '{jpg_filename}'")
            except Exception as e:
                print(f"Failed to convert '{filename}' to JPG: {str(e)}")


def is_image(file_name):
    """
    check if provided path to file is image or not
    :param file_name: (str) - path to image
    :return: True for image, Flase otherwise
    """
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
    return any(file_name.lower().endswith(ext) for ext in image_extensions)


if __name__ == "__main__":
    # Example usage:
    path_to_dir = "teeeeesting_renaming"
    files = "png"
    naming_pattern = "photo_"
    dirrename(path_to_dir, files, naming_pattern)

    img_temp = cv2.imread('../../demo/imgs_barcodes/gs1datamatrix_sample.jpg')
    show(img_temp, 200)
