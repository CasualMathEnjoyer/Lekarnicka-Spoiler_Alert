import os

from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re
from dateutil import parser

# Define a regex pattern to find potential date candidates
date_patterns_global = re.compile(
    r'\b\d{4}[-./]\d{2}[-./]\d{2}\b|'  # Matches "YYYY-MM-DD" format
    r'\b\d{2}[-./]\d{2}[-./]\d{4}\b|'  # Matches "MM-DD-YYYY" format
    r'\b\d{2}[-./]\d{4}\b|'  # Matches "MM-YYYY" format
    r'\b\d{4}[-./]\d{2}\b|'  # Matches "YYYY-MM" format
    r'\b\d{1,2}[-./]\d{1,2}[-./]\d{2,4}\b|'  # Matches "DD/MM/YYYY" or "DD-MM-YYYY" or "DD.MM.YYYY" format
    r'\b\d{1,2}/\d{1,2}/\d{2,4}\b'  # Matches "DD/MM/YYYY" or "DD-MM-YYYY" or "DD.MM.YYYY" format with slashes
)


class Expiry_Date_Recognition:
    def __init__(self, img, detect, recog):
        self.date_patterns = date_patterns_global
        self.img = DocumentFile.from_images(img)
        self.detect = detect
        self.recog = recog
        # Model
        model = ocr_predictor(det_arch=self.detect, reco_arch=self.recog, pretrained=True)
        # Analyze
        self.result = model(self.img)
        # print(self.result)

    def extract_dates(self, if_print_date=False):
        # Create a set to store unique dates
        unique_dates = set()

        # Iterate through pages, blocks, lines, and words
        for page in self.result.pages:
            for block in page.blocks:
                for line in block.lines:
                    words = line.words
                    for i in range(len(words)):
                        current_word = words[i].value

                        # Check if the current word contains a potential date candidate
                        potential_dates = re.findall(self.date_patterns, current_word)

                        # Remove any leading/trailing whitespace in potential dates
                        potential_dates = [date.strip() for date in potential_dates]

                        # Filter out numeric sequences that don't represent valid dates
                        potential_dates = [date for date in potential_dates if self.is_valid_date(date)]

                        # Add potential dates to the set
                        unique_dates.update(potential_dates)

                        # Check if the current word is a four-digit number
                        if re.match(r'\d{4}', current_word) and len(current_word) == 4:
                            # Check the word before the current word
                            if i > 0 and re.match(r'\d{2}', words[i - 1].value):
                                # Possible "MM YYYY" format
                                unique_dates.add(f"{words[i - 1].value} {current_word}")
                            # Check the word after the current word
                            if i < len(words) - 1 and re.match(r'\d{2}', words[i + 1].value):
                                # Possible "YYYY MM" format
                                unique_dates.add(f"{current_word} {words[i + 1].value}")

        # Filter out the results to only include the desired format "YYYY MM" or "MM YYYY"
        filtered_dates = [date for date in unique_dates if re.match(r'\d{2} \d{4}', date)]

        # I would add something like  "if print_output == True:" and make print_output a variable of this fucnnion
        if not filtered_dates:
            # Print unique dates
            for date in unique_dates:
                if if_print_date:
                    print("Found date:", date)
                return date
        else:
            # Print unique dates
            for date in filtered_dates:
                if if_print_date:
                    print("Found date:", date)
                return date

    def is_valid_date(self, date_str):
        try:
            date_obj = parser.parse(date_str, fuzzy=True)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    file_path = "expiry_date_dataset/leky_56.jpg"  # this is incorrect path 20231125, so:
    file_path = os.path.join(os.getcwd(), '..', '..', 'demo/expiry_date_dataset/leky_56.jpg')
    detect = 'db_resnet50'
    recog = 'crnn_vgg16_bn'

    exp_date_rec = Expiry_Date_Recognition(file_path, detect, recog)
    date = exp_date_rec.extract_dates()

    print(date)

