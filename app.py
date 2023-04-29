import streamlit as st
from image_pro_ext import process_upload, extracted_data, show_database
# ------------------------------------------setting page configuration---------------------------------------------------------
st.set_page_config(page_title='Bizcardx Extraction', layout="wide")
st.title(':blue[BizCardX Data Extraction]')

data_extraction, database_side = st.tabs(['Data uploading and Viewing', 'Database side'])
with data_extraction:

    st.markdown("![Alt Text](https://nanonets.com/blog/content/images/2020/09/landing-ocr-1.gif)")
    st.subheader(':blue[Choose image file to extract data]')
    #Uploading file to streamlit app ------------------------------------------------------
    uploaded = st.file_uploader('Choose a image file')
    #Convert binary values of image to IMAGE ---------------------------------------------------
    if uploaded is not None:
        with open(f'uploaded','wb') as f:
            f.write(uploaded.getvalue())
        st.subheader(':blue[Image view of Data]')
        if st.button('Extract Data from Image'):
            extracted = extracted_data(f'uploaded')
            st.image(extracted)
        st.subheader(':blue[Upload extracted to Database]')
        if st.button('Upload data'):
            process_upload(f'uploaded')
            st.success('Data uploaded to Database successfully!', icon="✅")
df = show_database()
with database_side:
    st.markdown("![Alt Text](https://i.giphy.com/media/aQCCNezRpb9Hq/giphy.gif)")
    #Showing all datas in database---------------------------------------------------------------
    st.title(':blue[All Data in Database]')
    if st.button('Show All'):
        st.dataframe(df)
    #Search data in the database----------------------------------------------------------------
    st.subheader(':blue[Search Data by Column]')
    column = str(st.radio('Select column to search', ('Name','Designation','Company_name','Area','City','State','Pincode','Contact_number','Mail_id','Website_link'), horizontal=True))
    value = str(st.selectbox('Please select value to search', df[column]))
    if st.button('Search Data'):
        st.dataframe(df[df[column] == value])
