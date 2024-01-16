import fitz
import re
import json
import numpy as np
import cv2
import pytesseract
import pandas as pd
import datetime
from word2number import w2n
import os
from openpyxl import load_workbook
from PIL import ImageDraw, Image, ImageFont

"""Function to convert each page of the pdf document to jpg images and return a list of numpy array for each image.
   The images are resized to avoid memory related exceptions"""


def pdf_to_jpg(pdf_path):
    pdf_document = fitz.open(pdf_path, )
    images = []

    if len(pdf_document) > 1:
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            px = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))
            image_array = np.frombuffer(px.samples, dtype=np.uint8).reshape(px.h, px.w, px.n)

            resized_image = cv2.resize(image_array, (3200, 4200))
            # print("Read resized Image ->", page_number + 1)
            images.append(resized_image)
    else:
        page = pdf_document[len(pdf_document)]
        px = page.get_pixmap()
        image_array = np.frombuffer(px.samples, dtype=np.uint8).reshape(px.h, px.w, px.n)
        images.append(image_array)
    pdf_document.close()

    return images


""" Function to save the output of tesseract as .txt file """


def save_to_txt(output_file, text):
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(text)


"""Function to retrieve the text data from the page by 
specifying the page number as the sliced index of the numpy array"""


def image_to_text(OCR_path, *args):
    for arg in args:
        if not isinstance(arg, list):
            raise TypeError("Input parameter must be a list of numpy array")
        else:
            pytesseract.pytesseract.tesseract_cmd = OCR_path
            final_json = {}
            master_list = []
            for _, images in enumerate(arg[192:193]):
                image = cv2.resize(images, None, fx=0.625, fy=0.625)
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                threshold_img = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                      cv2.THRESH_BINARY, 81, 15)
                text = pytesseract.image_to_string(threshold_img, config=r'--psm 4')
                # output_file1 = "psm4.txt"
                # save_to_txt(output_file1, text)
                lines = text.split("\n")
                # print(lines)

                date_pattern = r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|' \
                               r'\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{2,4}|' \
                               r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2})\b'
                dates = re.findall(date_pattern, text)
                # print("All the dates in the text:\n", dates)
                supp_dates = []
                for date in dates:
                    if bool(re.search(r'[a-zA-z]', date)) and bool(re.search(r'\d', date)):
                        supp_dates.append(date)
                # print("Supp dates:", supp_dates)
                duration_keywords = ['months', 'days', 'years']

                def keep_int_or_float(value):
                    try:
                        if isinstance(int(value), int):
                            return int(value)
                    except:
                        try:
                            if isinstance(float(value), float):
                                return float(value)
                        except:
                            return None

                year_pattern = r'\b(?:19\d{2}|20\d{2})\b'
                years = re.findall(year_pattern, text)
                print("All the years in the text:\n", years)

                num_pattern = r'[-+]?\d{1,5}(?:,?\d{3})*(?:\.\d+)?|\(\s*[-+]?\d{1,3}(?:,?\d{3})*(?:\.\d+)?\s*\)'
                # num_pattern = r'(?:\b\d{1,5}(?:,?\d{3})*(?:\.\d+)?\b|\b(?:19\d{2}|20\d{2})\b)'
                pattern = r'[,:()\-]'
                year_list = None
                unstruct_data = []
                prev_lookup = []
                i = 0
                for word_list in lines:
                    num_list = re.findall(num_pattern, word_list)
                    # print("Num List ->", i, ":\n")
                    # print("Word_list:", word_list, "num_list:", num_list)
                    # i += 1
                    num_list = [num.replace(',', '') for num in num_list]
                    # print("Num-list ->", i, "after replacing commas:\n")
                    # print("Word_list:", word_list, "num_list:", num_list)
                    num_list = [
                        float(number.replace('(', '').replace('(', '')) * (-1) if '(' in number else float(number) for
                        number in num_list]
                    word_list = re.sub(pattern, '', word_list)
                    word_list = word_list.split()
                    # print("Word list:\n ")
                    # print(word_list)
                    label = "_".join(
                        [word for word in word_list if word.isalpha()]).lower()
                    # print(label)
                    if len(num_list) != 0:
                        num_list = list(map(keep_int_or_float, num_list))
                        print(f"Num list {i + 1}:", num_list)
                        i+=1
                        if all(isinstance(x, int) for x in num_list):
                            if all((x >= datetime.datetime.today().year - 6 and x <= datetime.datetime.today().year) for
                                   x in num_list):
                                year_list = num_list
                                # print("Year List inside the loop:", year_list)
                            unstruct_data.append({label: num_list})
                            # print("Unstruct data inside the loop:", unstruct_data)

                    for duration in duration_keywords:
                        if duration in [item.lower() for item in word_list]:
                            has_number = any(item.isdigit() for item in word_list)
                            if has_number:
                                nl = "_".join(word_list).lower()
                                prev_lookup.append(nl)
                            else:
                                prev_lookup.append(label)
                    # print("Previous Lookup:", prev_lookup)
                    # print("Unstructured Data outside the loop:", unstruct_data)
                    month_num = []
                    for looks in prev_lookup:
                        for lk in [look for look in looks.split('_')]:
                            try:
                                month_num.append(w2n.word_to_num(lk))
                            except:
                                pass
                    resultant = []
                    if len(month_num) != 0:
                        month_num.sort()
                        for year in set(year_list):
                            for month in set(supp_dates):
                                datestring = month + ', ' + str(year)
                                date_obj = datetime.datetime.strptime(datestring,'%B %d, %Y')
                                for nums in month_num:
                                    if nums == 3:
                                        prev_date = date_obj - \
                                                    datetime.timedelta(nums * 30)
                                        prev_date = prev_date.strftime("%b, %Y")
                                        resultant.append(prev_date + '-' + datestring)

                                    if nums == 6:
                                        prev_date = date_obj - \
                                                    datetime.timedelta(nums * 30)
                                        prev_date = prev_date.strftime("%b, %Y")
                                        resultant.extend([prev_date + '-' + datestring])

                                    if nums == 9:
                                        prev_date = date_obj - \
                                                    datetime.timedelta(nums * 30)
                                        prev_date = prev_date.strftime("%b, %Y")
                                        resultant.extend([prev_date + '-' + datestring])

                                    if nums == 12:
                                        prev_date = date_obj - \
                                                    datetime.timedelta(nums * 30)
                                        prev_date = prev_date.strftime("%b, %Y")
                                        resultant.extend([prev_date + '-' + datestring])
                    resultant.sort()
                    # print("Year List:", year_list)

pdf = "bhel.pdf"
path_ocr = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
img = pdf_to_jpg(pdf)
image_to_text(path_ocr, img)
