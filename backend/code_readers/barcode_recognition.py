import cv2
from pyzbar.pyzbar import decode

from .img_manipulations import show  # my own shower


def decode_barcode(img=None, img_show: bool = False):
    """
    function that simply reads the barcode from image (should be robust to cases when
    several codes are in single image (todo test this))
    :param img: path to image as 'str' OR 'cv2.Image'
    :param img_show: bool = to show detected code in the picture or not
    :return: string = code detected.
    """
    # Load the image
    if img is None:
        raise Exception("detect_barcode has not received any input image. Abort.")
    if type(img) is str:
        image = cv2.imread(img)
    else:
        image = img.copy()  # already in cv2 image type

    barcode_data = " "
    # Decode barcodes in the image
    barcodes = decode(image)

    # Iterate through the barcodes found
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        x1, y1, x2, y2 = barcode.rect  # Get the coordinates of the barcode

        # Print the barcode data and type
        print(f"Data: {barcode_data}, Type: {barcode_type}")

        # Draw a rectangle around the barcode on the image
        cv2.rectangle(image, (x1, y1), (x1 + x2, y1 + y2), (0, 255, 0), 2)

    if barcode_data == " ":
        print(f'Error: no code recognized.')

    if img_show == True:
        # Display the image with barcode information
        show(image, 200)
        #cv2.imshow(winname='Barcode Image', mat=image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    return barcode_data


if __name__ == "__main__":
    curr_code = decode_barcode('../../demo/imgs_barcodes/mybarcode.jpg', True)
    print(f'curr_code = {curr_code}')

    curr_code2 = decode_barcode('../../demo/imgs_barcodes/barcode_cola.jpg', True)
    print(f'curr_code = {curr_code2}')

    curr_code3 = decode_barcode('../../demo/imgs_barcodes/barcode_greenmess.jpg', True)
    print(f'curr_code = {curr_code3}')

    curr_code4 = decode_barcode('../../demo/imgs_barcodes/barcode_many.jpg', True)
    print(f'curr_code = {curr_code4}')
