# functions for different parts of the app to communicate together

# from backend.code_readers.datamatrix_recognition import decode_gs1
from backend.code_readers.barcode_recognition import decode_barcode
from backend.frontend_interface.pilulka_scraper import get_name_from_EAN
from backend.date_recognition.expiry_date import Expiry_Date_Recognition
from backend.date_recognition.string_to_date import sseparate_date
from database.database_connection import insert_user, check_pwd, add_user_medication, _remove_user_medication, retrieve_user_medications

import hashlib

def photo2date(file_path):
    # will take a file_path, send it through date detection neural network
    # returns the expiration date as a string

    detect = 'db_resnet50'
    recog = 'crnn_vgg16_bn'

    exp_date_rec = Expiry_Date_Recognition(file_path, detect, recog)
    date = exp_date_rec.extract_dates()
    print(date)
    return date


# def matrixcode2string(path_to_img):  # both 2D and 1D code - needs a way to decide which is which ?
#     # is given an image and sends it to 2D code reader
#     # returns data as a string
#     return decode_gs1(path_to_img)


def _barcode2code(path_to_img):
    code = decode_barcode(path_to_img)
    if code == ' ':
        code = None
    return code

def _EAN2name(EAN):
    try:
        return get_name_from_EAN(EAN)
    except Exception as e:
        print("Driver not working")
        return None

def barcode2name(path_to_img):
    ean = _barcode2code(path_to_img)
    if ean == None:
        name = "UNKNOWN"
    else:
        name = _EAN2name(ean)
    return name

def string2data(string):
    # will take the string of data from 2D code reader
    # returns ('code of medication', 'expiration date')
    pass

def expcode_unification(string):
    # takes expiration date as a string
    # returns expiration date in format DD/MM/YYYY
    pass


# database stuff
def login(name, password):
    if check_pwd(name, password):
        return True
    else:
        return False
def register(name, password):
    if insert_user(name, password):
        return True
    else:
        return False

def add_item_to_lekarnicka(name, med, exp_date):
    # will create a lekarnicka item with name, number and the expiration date
    # saves this item in the lekarnicka of given user
    # returns True if successful
    if add_user_medication(name, med, exp_date):
        return True
    else:
        return False
def remove_item_from_lekarnicka(name, med, exp_date):
    # connects to the lekarnicka database and removes given item
    # returns true if item was succesfully removed
    if _remove_user_medication(name, med, exp_date):
        return True
    else:
        return False
    pass
def get_all_meds(name):
    items = retrieve_user_medications(name)
    r_items = []
    for item in items:
        r_items.append(item[1:])
    return r_items


# add_item_to_lekarnicka("test", "med1", "zitra")
# TODO pokud jsou v lekarnicce dva leky se stejnym jmenem a expiration, tak je to odstrani oba
# remove_item_from_lekarnicka("test", "med1", "zitra")

# na hashovani hesel
def hush_hush(psw_string, email):
    hashed = hashlib.md5((psw_string+email).encode())
    return hashed.hexdigest()

# print(hush_hush("meow", "kk@kk.cz"))

def separate_date(date_str):
    return sseparate_date(date_str)
