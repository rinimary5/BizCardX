import warnings
warnings.filterwarnings('ignore')
import easyocr
import numpy as np
import cv2 #OpenCV
from matplotlib import pyplot as plt
import os
import re
import sqlite3
import pandas as pd

# Establishing connection to database
conn = sqlite3.connect('C:/sqlite/test.sqlite',check_same_thread=False)
cursor = conn.cursor()
#Creating table in sql
table_create_sql = 'CREATE TABLE IF NOT EXISTS business (ID INTEGER PRIMARY KEY AUTOINCREMENT,Name TEXT,Designation TEXT,Company_name TEXT,Area TEXT,City TEXT,State TEXT,Pincode TEXT,Contact_number TEXT,Mail_id TEXT,Website_link TEXT,Image BLOB);'
cursor.execute(table_create_sql)
def process_upload(image):
#--------------------------PROCESSING IMAGE--------------------------------------------------------------
#Reading the image:
    img = cv2.imread(image)

#Converting to BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#Resizing the image
    resized_img = cv2.resize(img,(700,390 ))

#Cropping the image
    crop = resized_img[30:384, 15:690]

#Converting to gray image for thresholding
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#THRESHOLDING:
# for black backgrounds - binary - global
    _, th_1 = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
# for white backgrounds - binary - global
    _, th_2 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
#In order to determine if the image has a dark or light background,
#we will simply count the length of text considering the dark background and white background and compare them.
#---------------------------------------Extracting data using EasyOCR---------------------------------------------------
    reader = easyocr.Reader(['en'])
    data1 = []
    data2 = []
    data3 = []
    result1 = reader.readtext(th_1, paragraph=True, decoder='wordbeamsearch')
    j = 0
    for i in result1:
        data1.append(result1[j][1])
        j += 1

    result2 =  reader.readtext(th_2, paragraph=True, decoder='wordbeamsearch')
    j = 0
    for i in result2:
        data2.append(result2[j][1])
        j += 1
    result3 = reader.readtext(gray, paragraph=True, decoder='wordbeamsearch')
    j = 0
    for i in result3:
        data3.append(result3[j][1])
        j += 1
#The text corresponding to the right consideration will be longer than the other one
    if (len(data1)>len(data2)) and (len(data1)>len(data3)) :
        image_text = data1
        thresh_image = th_1
    elif(len(data2)>len(data1)) and (len(data2)>len(data3)):
        image_text = data2
        thresh_image = th_2
    else:
        image_text = data3
        thresh_image =gray

    org_reg = " ".join(image_text)
    reg = " ".join(image_text)

#Separating EMAIL---------------------------------------------------------------------------
    email_regex = re.compile(r'''([a-zA-z0-9]+@[a-zA-z0-9]+\.[a-zA-Z]{2,10})''', re.VERBOSE)
    email = ''
    for i in email_regex.findall(reg):
        email += i
        reg = reg.replace(i, '')
# ------------------------------------------Separating phone number---------------------------------------------------------------------------
    phoneNumber_regex = re.compile(r'\+*\d{2,3}-\d{3,10}-\d{3,10}')
    phone_no = ''
    for numbers in phoneNumber_regex.findall(reg):
        phone_no = phone_no + ' ' + numbers
        reg = reg.replace(numbers, '')
#---------------------------------------------Seperating company name-----------------------------------------------------
    comp_name_list = ['selva digital', 'GLOBAL INSURANCE','BORCELLE AIRLINES', 'Family Restaurant', 'Sun Electrical']
    company_name = ''
    for i in comp_name_list:
        if re.search(i, reg, flags=re.IGNORECASE):
            company_name =company_name +' '+i
            reg = reg.replace(i, '')

#--------------------------------------------Seperating address---------------------------------------------------------
    address_regex = re.compile(r'\d{2,4}.+\d{6}')
    address = ''
    for i in address_regex.findall(reg):
        address = address + ' ' + i
        reg = reg.replace(i, '')
#--------------------------------------------Separting Website URL------------------------------------------------------
    link_regex = re.compile(r'www.?[\w.]+', re.IGNORECASE)
    link = ''
    for lin in link_regex.findall(reg):
        link += lin
        reg = reg.replace(lin, '')
#-------------------------------------------Seperating Designation------------------------------------------------------
    desig_list = ['DATA MANAGER', 'CEO & FOUNDER', 'General Manager', 'Marketing Executive', 'Technical Manager']
    designation = ''
    for i in desig_list:
        if re.search(i, reg):
            designation += i
            reg = reg.replace(i, '')
#------------------------------------------Seperating name--------------------------------------------------------------
    name = reg.strip()

    address1=address
#---------------------------------------------Seperating State from Address---------------------------------------------

    states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat',
          'Haryana','Hyderabad', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
            'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
            'Rajasthan', 'Sikkim', 'TamilNadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
    State=''
    for i in states:
        if re.search(i,address1, flags=re.IGNORECASE):
            State =State +' '+i
            address1 = address1.replace(i, '')

#---------------------------------------------Seperating City from Address---------------------------------------------

    city = ['Ariyalur ', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 'Dindigul', 'Erode', 'Kanchipuram',
        'Kanyakumari', 'Karur',
        'Krishnagiri', 'Madurai', 'Nagapattinam', 'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai', 'Ramanathapuram',
        'Salem', 'Sivagangai', 'Thanjavur', 'Theni', 'Thoothukudi',
        'Thiruchirapalli', 'Thirunelveli', 'Tirupur', 'Thiruvallur', 'Thiruvannamalai', 'Thiruvarur', 'Vellore',
        'Viluppuram', 'Virudhunagar', 'Mumbai', 'Delhi', 'Kolkata', 'Bangalore', 'HYDRABAD', 'Ahemdabad',
        'Pune', 'Surat', 'Kanpur']
    City=''
    for i in city:
        if re.search(i,address1, flags=re.IGNORECASE):
            City =City +' '+i
            address1 = address1.replace(i, '')
#---------------------------------------------Seperating Pincode from Address---------------------------------------------


    match = re.search(r'\d{6,7}', address1.lower())
    if match:
        PIN = match.group()
        address1 = address1.replace(PIN, '')

#---------------------------------------------Seperating Area from Address---------------------------------------------

    area = address1.replace(',', '')
    area= area.replace(';', '')
    with open(image, 'rb') as file:
        blobimg = file.read()

#Uploading values into database
    table_enter_value = "INSERT INTO business(Name,Designation,Company_name,Area,City,State,Pincode,Contact_number,Mail_id,Website_link,Image)VALUES(?,?,?,?,?,?,?,?,?,?,?);"
    cursor.execute(table_enter_value,(name, designation, company_name, area, City, State, PIN, phone_no, email, link, blobimg))
#To display the extracted data by showing rectangle
def extracted_data(image):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image, paragraph=True, decoder='wordbeamsearch')
    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    for detection in result:
        top_left = tuple([int(val) for val in detection[0][0]])
        bottom_right = tuple([int(val) for val in detection[0][2]])
        text = detection[1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.rectangle(img, top_left, bottom_right, (204, 0, 34), 5)
        img = cv2.putText(img, text, top_left, font, 0.8,(0, 0, 255), 2, cv2.LINE_AA)
    return img

#To display all values stored in db
def show_database():
    new_df = pd.read_sql("SELECT * FROM business", con=conn)
    return new_df