# BizCardX
Extracting Business Card Data with OCR

# EasyOCR
EasyOCR is actually a python package that holds PyTorch as a backend handler. EasyOCR like any other OCR(tesseract of Google or any other) detects the text from images but in my reference, while using it I found that it is the most straightforward way to detect text from images also when high end deep learning library(PyTorch) is supporting it in the backend which makes it accuracy more credible. EasyOCR supports 42+ languages for detection purposes. EasyOCR is created by the company named Jaided AI company.<br/>
## To use easyocr you need to install pytorch also.
pip3 install torch torchvision torchaudio
<br/>
pip install git+https://github.com/JaidedAI/EasyOCR.git
# Image Processing:
![impro](https://user-images.githubusercontent.com/71283204/235315533-0cfa0e3d-9e5e-4696-996e-ee8a4189aa07.png)
# Establishing connection to database
![connec](https://user-images.githubusercontent.com/71283204/235315976-2fda55b8-f8dc-4f21-a6d5-6b9c891aa5ad.png)
# Creating table in sql
table_create_sql = '''CREATE TABLE IF NOT EXISTS business (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                         Name TEXT,Designation TEXT,Company_name TEXT,
                                                         Area TEXT,City TEXT,State TEXT,Pincode TEXT,
                                                         Contact_number TEXT,Mail_id TEXT,Website_link TEXT,
                                                         Image BLOB);'''<br/>
cursor.execute(table_create_sql)
# To display the extracted data by showing rectangle:
![ext](https://user-images.githubusercontent.com/71283204/235316176-7356f1ff-d3e7-4ecd-b463-4cd3eeb94e92.png)
# Extracting data using EasyOCR:
![read](https://user-images.githubusercontent.com/71283204/235316335-a0d0b4de-1905-44ce-b736-db6d299db3e7.png)
# Uploading values into database:
table_enter_value = '''INSERT INTO business(Name,Designation,Company_name,
                                          Area,City,State,Pincode,
                                          Contact_number,Mail_id,Website_link,Image)
                                          VALUES(?,?,?,?,?,?,?,?,?,?,?);'''<br/>
cursor.execute(table_enter_value,(name, designation, company_name, area, City, State, PIN, phone_no, email, link, blobimg))

# To display all values stored in db
![disp](https://user-images.githubusercontent.com/71283204/235316634-5182102a-9972-4130-8214-a7bd62c29c17.png)
