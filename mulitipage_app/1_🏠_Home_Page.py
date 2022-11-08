from janitor import xlsx_table # extracting 'Tables' from a worksheet using the 'pyjanitor' module
import streamlit as st
from streamlit_option_menu import option_menu # using side bar menu in steamlit web page
import plotly.figure_factory as ff
import plotly.express as px
from PIL import Image # To Upload an image 

st.set_page_config(
    page_title="Multipage",
)


image = st.container()

background_color= '#F5F5F5'
with image:
    #Upload Morocco Mall Image
    image = Image.open('/Users/tariq/opt/miniconda3/envs/test1/Test1_Code/MMM.png')
    st.image(image, use_column_width= True, output_format="SVG") #display image to match column width



st.title("Morocco Mall Marrakech")
st.sidebar.success("Select a page above")

