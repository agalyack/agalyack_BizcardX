import easyocr
import pandas as pd
import numpy as np
import re
import streamlit as st
import os
from PIL import Image
import mysql.connector
from sqlalchemy import create_engine
import pymysql

 # Define MySQL connection parameters
mysql_username = 'root'
mysql_password = 'roots'
mysql_host = 'localhost'
mysql_port = '3306'
mysql_database = 'buzproject'
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="roots",
    database="buzproject"
)
def cardholder_list():
    cursor1=conn.cursor()
    query="Select Card_holder_name from buzproject.buz_card"
    result=cursor1.execute(query)
    name_l=cursor1.fetchall()
    name_list = [i[0] for i in name_l]
    return name_list
def myupdated_table():
    cursor1=conn.cursor()
    query="SELECT Card_holder_name,Designation,Mobile_number,Email,Website,Pincode,Area,City,State,Company_name FROM buz_card "
    result1=cursor1.execute(query)
    mytab=cursor1.fetchall()
    mytable=[i[0] for i in cursor1.description]
    mytable_df=pd.DataFrame(mytab,columns=mytable)
    st.write(mytable_df)



# Create a temporary directory to save uploaded images
if not os.path.exists("tempDir"):
    os.makedirs("tempDir")

st.set_page_config(
    page_title="BizcardX Extracting Business Card Data with OCR",
    layout="wide",
    initial_sidebar_state="expanded")
reader=easyocr.Reader(['en'])
# CSS styling for the header and subheader
st.markdown(
    """
    <style>
    .header-container {
        background-color: green; /* Purple background */
        padding: 20px; /* Increased padding */
        border-radius: 15px; /* Rounded corners */
        width: 100%; /* Make the container broader */
        margin-left: 10px; /* Align to left margin */
        margin-bottom: 20px; /* Reduce gap between header and subheader */
    }
    .header-text {
        font-family: Arial, sans-serif;
        color: white; /* White text color */
        margin: 0; /* Remove default margin */
        font-size: 24px; /* Increase font size */
    }
    .subheader-container {
        background-color: purple; /* Purple background */
        padding: 5px; /* Padding around the text */
        border-radius: 10px; /* Rounded corners */
        width: 100%; /* Width of the container */
        margin-left: 10px; /* Align to left margin */
        margin-top: -10px; /* Reduce gap between header and subheader */
    }
    .subheader-text {
        font-family: Arial, sans-serif;
        color: white; /* White text color */
        font-size: 24px; /* Font size */
        margin: 0; /* Remove default margin */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Display the header with custom styling
st.markdown('<div class="header-container"><p class="header-text">BizCardX</p></div>', unsafe_allow_html=True)

# Display the subheader with custom styling
st.markdown('<div class="subheader-container"><p class="subheader-text">Extracting Business Card Data with OCR</p></div>', unsafe_allow_html=True)

with st.container(height=750,border=True):
     st.image('D:/phonepe/busi.png',caption='Business Card Extraction')

col1_card,col2_card=st.columns(2)
card_data=None
global card_table
with col1_card:
    
    st.title("Buz card Extraction")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
   
    if uploaded_image is not None:
        # Display the uploaded image
        #image = Image.open(uploaded_file)
        st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)
        #save the file
        with open(os.path.join("tempDir", uploaded_image.name), "wb") as f:
            f.write(uploaded_image.getbuffer())
        st.success("Saved File")
        
        card_data=reader.readtext(os.path.join("tempDir", uploaded_image.name))
        print(card_data)
with col2_card:
    
    st.title("Extracted data")
    text=[]
    card_holder_name=[]
    designation=[]
    mobile_numbers=[]
    company_name=[]
    pincode=[]
    website=[]
    areas=[]
    city=[]
    email=[]
    state=[]
    
    if card_data is not None:
        for entry in card_data:
           text.append(entry[1])
        print(text)
        if text:
            card_holder_name=text[0]
            designation=text[1]
            
            for i in text:
                if  '-' in i:
                    mobile_numbers.append(i)
            if len(mobile_numbers)>=2:
                mobile_numbers=' & '.join(mobile_numbers)
            else:
                mobile_numbers=''.join(mobile_numbers)
               
              
            for i in text:
                if "@" in i:
                    email=i
            #website_i = None
            for ind, i in enumerate(text):
                if ("www" in i.lower() or "www." in i.lower()):
                        website = i
                        if ("WWW" in i and "@"not in text[ind+1]):
                            website +="."+ text[ind+1]
                        break

           
            for i in text:
                if len(i) >= 6 and i.isdigit():
                    pincode.append(i)
                elif re.findall('[a-zA-Z]{9} +[0-9]', i):
                    pincode.append(i[10:]) 
            for i in text:
                if re.findall('^[0-9].+, [a-zA-Z]+', i):
                   area = i.split(',')[0]
                   areas=area
                elif re.findall('[0-9] [a-zA-Z]+', i):
                   areas=i
            for i in text:
                city_1=re.findall('St , ([a-zA-Z]+).+',i)
                city_2=re.findall('St,, ([a-zA-Z]+).+',i)
                city_3=re.findall('^[E].*',i)
                if city_1:
                    city=city_1
                elif city_2:
                    city=city_2
                elif city_3:
                    city=city_3
            for item in text:
                state_1 = re.search(r'\bTamilNadu\b', item, flags=re.IGNORECASE)
                if state_1:
                    state=state_1.group(0)
            keywords=['selva','digitals','GLOBAL','INSURANCE','BORCELLE','AIRLINES','Family','Restaurant','Sun Electricals']
            company_name=' '.join(value for value in text if any(keyword== value for keyword in keywords))

            print(card_holder_name)
            print(designation)
            print(mobile_numbers)
            print(email)
            print(website)
            print(pincode)
            print(areas)
            print(city)
            print(state)
            print("Length of card_holder_name:", len(card_holder_name))
            print("Length of designation:", len(designation))
            print("Length of mobile_number:", len(mobile_numbers))
            #print(len(image_data))
      
    
    
        card_table=pd.DataFrame(
        {
            'Card_holder_name':card_holder_name,
            'Designation':designation,
            'Mobile_number':[mobile_numbers],
            'Email':email,
            'Website':website,
            'Pincode':pincode,
            'Area':areas,
            'City':city,
            'State':state,
            'Company_name':company_name
            

         }
         )
        card_table_t=card_table.T
        
        st.dataframe(card_table_t,width=800,hide_index=False)
       
with st.container(height=100):
    
    def img_to_binary(file_path):
        # Convert image data to binary format
        with open(file_path, 'rb') as file:
           binaryData = file.read()
        return binaryData  
    if uploaded_image is not None:
        file_path = os.path.join("tempDir", uploaded_image.name)
        card_table['Image_data']=img_to_binary(file_path)
    else:
        print("upload image")
   
    if st.button("Upload to the Database",use_container_width=True):
        connection_str = f"mysql+mysqlconnector://{'root'}:{'roots'}@{'localhost'}:{'3306'}/{'buzproject'}"
        engine = create_engine(connection_str)
        table_name = 'buz_card'
       
        card_table.to_sql(name='buz_card', con=engine, if_exists='append', index=False)
        engine.dispose() 
mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="roots",
  database="buzproject"
  
)

mycursor = mydb.cursor()
mod=st.selectbox('Select the card holder to modify', options = cardholder_list())
if (len(cardholder_list()) == 0):
    st.write("Please upload card details into database") #no details exist in table, first upload to modify/delete
else:
    ConfirmDisp = st.checkbox("Display Details of selected Card Holder")
    if ConfirmDisp:
            col6,col7 = st.columns([2,2])
            with col6:
                mycursor.execute("SELECT Designation,Mobile_number,Email,Website,Pincode,Area,City,State,Company_name FROM buz_card WHERE Card_holder_name = %s",(mod))
                result = mycursor.fetchone()
                design_new = st.text_input('Designation: ', result[0])
                mob_new = st.text_input('Mobile_number: ', result[1])
                email_new = st.text_input('Email: ', result[2])
                website_new = st.text_input('Website: ', result[3])
                pin_new = st.text_input('Pincode: ', result[4])      
                
            with col7:
                area_new = st.text_input('Area: ', result[5])
                city_new = st.text_input('City: ', result[6])
                state_new = st.text_input('State: ', result[7])
                comp_new = st.text_input('Company_name: ', result[8])

            if st.button("Save Changes"):
                # Update the information for the selected business card in the database
                mycursor.execute("""UPDATE buz_card SET Designation=%s,Mobile_number=%s,Email=%s,Website=%s,Pincode=%s,Area=%s,City=%s,State=%s,Company_name=%s
                                    WHERE Card_holder_name=%s""",(design_new,mob_new,email_new,website_new,pin_new,area_new,city_new,state_new,comp_new,mod))
                mydb.commit()
                st.success("Information updated in database successfully.")
                st.write("PLEASE HAVE A LOOK")
            if st.button("Show Changes"):
                myupdated_table()
mycursor = mydb.cursor()
mod1=st.selectbox('Select the card holder to delete', options = cardholder_list())
if (len(cardholder_list()) == 0):
    st.write("Please upload a card details into database") #no details exist in table, first upload to modify/delete
else:              
    ConfirmDel = st.checkbox("Delete Details of selected Card Holder")
    if ConfirmDel:
            st.error("Are you sure you want to delete?")
            if st.button("Yes"):
                mycursor.execute("""DELETE FROM buz_card WHERE Card_holder_name = %s""", (mod1))
                mydb.commit()
                st.success("Business card information deleted from database.")
                st.write("PLEASE HAVE A LOOK")
            if st.button("Show Now"):
                myupdated_table()                    
        
        

        

       



   


    
