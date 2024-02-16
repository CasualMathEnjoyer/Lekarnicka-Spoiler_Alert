from dateutil.parser import parse
from datetime import datetime

def string_to_date(string_date):
    dt = parse(string_date)
    date_time_format = '%d.%m.%y'
    string_date = dt.strftime(date_time_format)
    date = datetime.strptime(string_date, date_time_format)
    return date

# simple if else function, because the implemented python library had problems:
def sseparate_date(string_date):
    print(string_date)
    separators = [".", "/", ",", "-"]
    for sep in separators:
        if sep in string_date:
            date = string_date.split(sep)
            if len(date) == 2:
                try:
                    month = int(date[0])
                    if month > 12:
                        return None
                    year = int(date[1])
                    if year < 1000:
                        return None
                except:
                    return None
                dt = ["1", date[0], date[1]]
                st_string = dt[0] + "." + dt[1] + "." + dt[2]
                return st_string
            elif len(date) == 3:
                try:
                    day = int(date[0])
                    if day > 31:
                        return None
                    month = int(date[1])
                    if month > 12:
                        return None
                    year = int(date[2])
                    if year < 1000:
                        return None
                except:
                    return None
                dt = date
                st_string = dt[0] + "." + dt[1] + "." + dt[2]
                return st_string
            elif len(date) == 1:
                try:
                    year = int(date[0])
                    if year < 1000:
                        return None
                except:
                    return None
                dt = ["1", "1", date[1]]
                st_string = dt[0] + "." + dt[1] + "." + dt[2]
                return st_string
    if len(string_date) == 4:
        try:
            year = int(string_date)
            dt = ["1", "1", string_date]
            st_string = dt[0] + "." + dt[1] + "." + dt[2]
            return st_string
        except:
            return None
    return None

# print(separate_date("2.12.2001"))

# my_dates = ['02-15-2020','15-02-2020','2.15.20','15.2.20','15/02/20','2/15/2020']
# date_list = []
#
# for date in my_dates:
#     date_list.append(string_to_date(date))
#
# for date in date_list:
#     print (date)

# from datetime import datetime
#
# def format_date(input_date, separator="."):
#     separators = [".", "/", ",", "-"]
#     for char in input_date:
#         if char in separators:
#             separator = char
#     try:
#         try:
#             format_str = f"%d{separator}%m{separator}%Y"
#             parsed_date = datetime.strptime(input_date, format_str)
#         except ValueError:
#             # If parsing fails, try parsing without the day
#             format_str = f"01{separator}%m{separator}%Y"
#             parsed_date = datetime.strptime("01" + separator + input_date, format_str)
#     except:
#         return None
#     # Construct the formatted date string
#     out_separator = "."
#     formatted_date = f"{parsed_date.day}{out_separator}{parsed_date.month}{out_separator}{parsed_date.year}"
#
#     return formatted_date
#
# if __name__ == "__main__":
#     # Example usage
#     input_date = "1-2023"
#     formatted_date = format_date(input_date)
#     print("Input Date:", input_date)
#     print("Formatted Date:", formatted_date)
