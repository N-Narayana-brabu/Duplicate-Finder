# UI

import streamlit as st
import base64
import pandas as pd
import mysql.connector
from db_connection import insert_data_into_database
from db_connection import delete_data_from_database
from db_connection import insert_existing_email_into_database
from db_connection import delete_existing_email_from_database
from db_connection import get_table_download_link
from db_connection import compare_and_delete
# To hide the default text by Streamlit Application
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden}
            footer {visibility: hidden}
            header {visibility: hidden} 
            </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)


# Background Image function
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background('image.avif')

st.sidebar.markdown("<h1 style='height: 100%;width:"
                    " 100%;text-align:"
                    " center;padding:25px;"
                    " margin-top: -45px; font-size:30px;"
                    " text-shadow: 2px 2px 4.5px ;"
                    "letter-spacing: 5px;"
                    " font-style:italic; "
                    "padding: 2px;"
                    " border-radius: 5px;"
                    " background-color: white;"
                    "color: black;"
                    "border:0.1px solid rgba(255, 99, 71, 0.6);"
                    "width: 100%;"
                    "max-width:365px;"
                    "height: 100%;"
                    "'>DUPLICATE FINDER</h1>", unsafe_allow_html=True)

# to adjust the sidebar transperncy
st.markdown("""
    <style>

        [data-testid=stSidebar] {
       background-color: rgba(0, 0, 255, 0.1);

        }

   /* Drag And Drop container */

.st-emotion-cache-taue2i {
    background-color: rgba(255, 255, 255, 0.9);
    border:0.1px solid rgba(255, 99, 71, 0.6);
    color: black;

}


.st-emotion-cache-1aehpvj {
    color: black; /* Change to your desired color code */
    }

   /* Drag And Drop container height and width  */  

 .st-emotion-cache-taue2i.e1b2p2ww15 {
    height: 150px;
    max-width:365px;/* Change this value to adjust the height as desired */
  }

   /* Drag And Drop container button color */

        .st-emotion-cache-13ejsyy.ef3psqc12 {
    background-color: lightcoral !important;
    color: white; 
  }

   /* Drag And Drop container button hover color */

  .st-emotion-cache-13ejsyy.ef3psqc12:hover {
    background-color: darkseagreen;
    color: black ;
}

  /* paragraph in the side bar it located in the below of the side bar image */
  .st-emotion-cache-16idsys.e1nzilvr5 p {
    color: black;
    background-color: rgba(255, 255, 255, 0.9);
    border:0.1px solid rgba(255, 99, 71, 0.6);
    margin-left:1px;
    border-radius:5px;
    padding:5px;
    font-size:16px;
    font-style:;

  }

  /* Close button */
.st-emotion-cache-ztfqz8.ef3psqc5 {
   background-color: lightcoral;
    color: white; 

}
/* close button hover */
.st-emotion-cache-ztfqz8.ef3psqc5:hover {
    background-color: darkseagreen;
    color: black ;

}

/* st.success  */
.st-ae {
   background-color: rgba(245, 245, 245, 0.7);
   color: black;
   border:0.1px solid rgba(255, 99, 71, 0.6);
   border-radius: 5px;
   margin-top: 50px;

}

/* video file with name ui shows white color */
 .st-emotion-cache-fis6aj {
  background-color: rgba(255, 255, 255, 0.9);
  margin-top: 10px;
  border-radius:5px;
    max-width:365px;

}

.svg-container {
  background-color: #FF0000;

   /* Change to your desired background color */
 }
a {
    text-decoration: none;
    
}

    </style>
    """, unsafe_allow_html=True)

st.sidebar.text("")

lead_data = st.sidebar.file_uploader("Upload Lead Data Sheet", type=["xlsx", "xls"])

# Create a two-column layout for buttons
col1, col2 = st.sidebar.columns(2)

# Button 1: Submit
if col1.button("Submit"):
    if lead_data is not None:
        # Load the Excel data into a pandas dataframe
        df = pd.read_excel(lead_data)

        # Insert data into the database
        if insert_data_into_database(df):
            st.success("Lead Sheet Data submitted successfully!")

# Button 2: Delete Data
if col2.button("Delete Data"):
    # Delete data from the database
    if delete_data_from_database():
        st.warning("Lead Sheet Data deleted from the database!")

st.sidebar.text("")
st.sidebar.text("")

# Upload file
Email_data = st.sidebar.file_uploader("Upload Existing Email-ID Sheet", type=["xlsx", "xls"])

# Create a two-column layout for buttons
col3, col4 = st.sidebar.columns(2)

# Button 1: Submit
if col3.button("Submit", key="submit_button"):
    if Email_data is not None:
        # Load the Excel data into a pandas dataframe
        df = pd.read_excel(Email_data)

        # Insert data into the database
        if insert_existing_email_into_database(df):
            st.success("Existing Email's submitted successfully!")

# Button 2: Delete Data
if col4.button("Delete Data", key="delete_data_button"):
    # Delete data from the database
    if delete_existing_email_from_database():
        st.warning("Existing Email's deleted from the database!")


st.sidebar.text("")
# Example usage in Streamlit app
if st.sidebar.button("Get Sheet"):
    deleted_rows_count, deleted_email_addresses, email_occurrence_count = compare_and_delete()

    if deleted_rows_count > 0:  # Check if any rows were deleted
        st.success(f"Number of deleted rows: {deleted_rows_count}")


        for email_address in deleted_email_addresses:
            st.write(f"{email_address} - It appears: {email_occurrence_count.get(email_address, 0)} Times")

        # Download updated data from lead_sheet
        st.markdown(get_table_download_link(), unsafe_allow_html=True)
    else:
        st.warning("No rows deleted.")  # Indicate that no rows were deleted







