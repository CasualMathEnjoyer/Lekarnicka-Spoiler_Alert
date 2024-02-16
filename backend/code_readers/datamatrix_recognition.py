"""
function(s) to recognize and generate GS1 DataMatrix codes

"""

from pylibdmtx.pylibdmtx import \
    decode  # import of existing recognizer ( https://github.com/NaturalHistoryMuseum/pylibdmtx/ )
import cv2  # opencv-python aka cv2
from backend.code_readers.img_manipulations import show  # my own shower

from treepoem import generate_barcode
from PIL import Image

import treepoem


def decode_gs1(path_to_img: str, show_img: bool = False, print_contents: bool = False, timeout: int = None):
    """
    Function that takes image of GS1DataMatrix code and returns the contents in the code
    :param path_to_img: path to image as str
    :param show_img: bool - to show or not. Works both in console Python and IPYNB notebook
    :param print_contents: bool - print in console
    :param timeout: int - how many miliseconds can we afford to spend on searching for the code in the image provided
    :return: contents ... list of elements read from code (string with actual code, and its relative position)
    """
    if type(path_to_img) != str:
        raise TypeError("input 'path_to_img' should be a string. Aborted.")
    img = cv2.imread(path_to_img)
    if timeout == None:
        # no precise time limit
        contents = decode(img)
    else:
        # we have a time limit (how many milliseconds we can spent on thinking about the image)
        contents = decode(img, timeout=timeout)
    if show_img:
        show(img, 200)
    if print_contents:
        print(contents)
    return contents


def generate_gs1(gtin, serial_number, expiry_date, batch_number, filename: str = "output.png", show_img: bool = False):
    """
    GS1 DataMatrix generator
    :param gtin:
    :param serial_number:
    :param expiry_date:
    :param batch_number:
    :param filename:
    :param show_img:
    :return:
    """
    datamatrix = treepoem.generate_barcode(
        barcode_type='gs1datamatrix',
        data=f"(01){gtin}(21){serial_number}(17){expiry_date}(10){batch_number}",
        options={"parsefnc": True, "format": "square", "version": "26x26"})

    # Resize datamatrix to desired size
    dm_size_px = (120, 120)
    datamatrix = datamatrix.resize(dm_size_px, Image.NEAREST)

    # Create white picture
    picture_size_px = (200, 200)
    picture = Image.new('L', picture_size_px, color='white')

    # Position the datamatrix
    barcode_position_px = (40, 40)
    picture.paste(datamatrix, barcode_position_px)

    # Save the image
    picture.save(filename)
    img = cv2.imread(filename)
    if show_img:
        show(img, 200)
    return True


def generate_datamatrix(data: str = "dummycode", name_of_img: str = "gs1_dm_via_treepoem_sample.png"):
    """
    generator of DataMatrix (NOT GS1 !!! there seems to be difference) 2D cods written using 'treepoem' library
    :param data:
    :param name_of_img:
    :return:
    """
    datamatrix = treepoem.generate_barcode(
        barcode_type='datamatrix',
        data="01234567890",
        options={"eclevel": "M"},  # Error correction level, adjust as needed
    )
    datamatrix.save(name_of_img)
    return None


if __name__ == "__main__":
    # Example usage:
    decode_gs1("../../demo/imgs_barcodes/gs1datamatrix_sample.jpg", show_img=True, print_contents=True, timeout=500)

    gtin = "01234567890128"
    serial_number = "01234567891011"
    expiry_date = "250731"
    batch_number = "DATAMATRIXalex"

    generate_gs1(gtin=gtin, serial_number=serial_number, expiry_date=expiry_date, batch_number=batch_number,
                 filename="gs1_generated_sample.png", show_img=True)
