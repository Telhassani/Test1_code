from janitor import xlsx_table # extracting 'Tables' from a worksheet using the 'pyjanitor' module
import streamlit as st
from streamlit_option_menu import option_menu # using side bar menu in steamlit web page
import plotly.figure_factory as ff
import plotly.express as px
from PIL import Image # To Upload an image 

import streamlit_authenticator as stauth
import pickle
from pathlib import Path

st.set_page_config(
    page_title="Multipage",
)


image = st.container()

background_color= '#F5F5F5'
with image:
    #Upload Morocco Mall Image
    image = Image.open('/Users/tariq/opt/miniconda3/envs/test1/Test1_Code/Test1_code/MMM.png')
    st.image(image, use_column_width= True, output_format="SVG") #display image to match column width




# -------- USER AUTHENTIFICATION ---------

names = ["Chaiema Benour"]
usernames = ["C.Benour"]

# -------- LOAD THE PASSWORDS ---------

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
 "MMM_Dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("login", "main" )


if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    st.title("Morocco Mall Marrakech")
    st.sidebar.success("Select a page above")


