#from sys import path
#from altair import Header
#from matplotlib.pyplot import legend
#import pandas as pd
#import xlrd as xl
# ---Modules
from lib2to3.pgen2.pgen import DFAState
from janitor import xlsx_table # extracting 'Tables' from a worksheet using the 'pyjanitor' module
import streamlit as st
from streamlit_option_menu import option_menu # using side bar menu in steamlit web page
import plotly.figure_factory as ff
import plotly.express as px
from PIL import Image # To Upload an image 

from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

import warnings
warnings.simplefilter("ignore") #Ignore excel data validation error message

# ---Containers
image = st.container()
header = st.container()
metrics = st.container()
data = st.container()
overview = st.container()
budget_lot = st.container()

#st.markdown(
#    """
#    <style>
#    .main {
#        background-color: #F5F5F5;
#    }
#    <style>
#    """,
#    unsafe_allow_html=True
#)
background_color= '#F5F5F5'
with image:
    #Upload Morocco Mall Image
    image = Image.open('/Users/tariq/opt/miniconda3/envs/test1/Test1_Code/MMM.png')
    st.image(image, use_column_width= True, output_format="SVG") #display image to match column width
    

with metrics:
    st.markdown('### Metrics')

    col1, col2, col3, col4, = st.columns(4)
    col1.metric(" GO Mall", "312.5M")
    col2.metric(" GO Res.", "26.5M")
    col3.metric(" Archis Mall", "46.4M")
    col4.metric(" BETs Mall", "22.4M")


# This container includes the header, the title and the pic of the project
with header:
    st.header('AKSAL PROPERTY')
    st.header('DASHBOARD: MOROCCCO MALL MARRAKECH')

with data:
   
    @st.cache(allow_output_mutation=True)
    def RECAP_MMM_upload():
        df = xlsx_table('/Users/tariq/Library/CloudStorage/OneDrive-Personal/WORK/MMM/TARIQ/Summary-PowerBI.xlsm', 'RECAP','RECAP_MMM')
        return df
   
    summary=RECAP_MMM_upload()
    
    #data.write(summary)
    st.info(len(summary))
    # Display table using the Aggrid module
    st.markdown('## A deep look into the data')
    gd_summary = GridOptionsBuilder.from_dataframe(summary)
    gd_summary.configure_pagination(enabled=True,paginationAutoPageSize=True,paginationPageSize=15)
    gd_summary.configure_default_column(editable=True, groupable=True)
    sel_mode = st.radio('Selection Type', options=["single", "multiple"])
    gd_summary.configure_selection(selection_mode= sel_mode, use_checkbox=True)
    gridoptions = gd_summary.build()
    grid_table = AgGrid(summary, 
                        gripOptions=gridoptions,
                        update_mode=GridUpdateMode.SELECTION_CHANGED,
                        height= 500,
                        reload_data=True,
                        allow_unsafe_jscode=True,
                        editable=True)                    

    # Show selected data in the table

    sel_rows = grid_table["selected_rows"]
    st.write(sel_rows)




# This container contains graphs showing an overview of the project 
with overview:

    st.header("Overview of the Project")
    st.subheader('Budget par Lot et Prestatire')

    # Treemap detailling "Budget par prestataire"
    summary_treemap = px.treemap(data_frame = summary, 
    path=['LOT', 'PRESTATAIRES', 'Lot Contrat'], values='MARCHE TTC',
    width= 1000, height= 500,
    labels= True)
    summary_treemap.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    
    # Define the type of the data to display on the layout
    summary_treemap.data[0].textinfo = 'label+text+value'
    # Disactivate the hovermode
    summary_treemap.layout.hovermode = False
    #summary_treemap.update_traces(root_color="#F5F5F5")
    overview.write(summary_treemap)
    
    #Histogram detailing "Suivi de paiement par Lot"
    st.header("Suivi de paiement par lot")
    summary_hist = px.histogram(summary, x= 'LOT', y= ['MARCHE TTC','Régler  ','Réste à Régler '], text_auto= '.2s',
    width= 1000, height= 500,
    barmode= 'group', labels= True)
    
    # Change the histogram layout
    summary_hist.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    summary_hist.update_traces(textposition='inside', text='label')
    
    # Disactivate the hovermode
    summary_hist.layout.hovermode = False
    #summary_treemap.update_traces(root_color="#F5F5F5")
    overview.write(summary_hist)



# This container contains a bar and a pie chart
with budget_lot:

    # Container's header
    st.header('Répartition du Budget par Contrats')
    
    load = st.button('Import Data')
    
    # Function extracting the table from Excel
    @st.cache(allow_output_mutation=True)
    def Budget_Par_Lot_upload():
        bpl = xlsx_table('/Users/tariq/Library/CloudStorage/OneDrive-Personal/WORK/MMM/TARIQ/Summary-PowerBI.xlsm', 'RECAP','Budget_Par_Lot')
        return bpl


    # Initialize session state
    if 'load_state' not in st.session_state:
        st.session_state.load_state = False

    if load or st.session_state.load_state:

        st.session_state.load_state = True

        # Load the Excel table from the file
        budget_par_lot = Budget_Par_Lot_upload()
        
        # User option button
        opt = st.radio('Choose the chart type:',['Bar','Pie'])
       
        if opt == 'Bar':

            # Show Data
            #st.write(budget_par_lot)
            #Reading a specific table in the worksheet
            fg = px.bar(budget_par_lot, y= 'Budget', x= 'Lot Contrat', text_auto= '.2s')
            #width= 1000, height= 500)
            budget_lot.write(fg)
        else:    
            fg = px.pie(budget_par_lot, names= 'Lot Contrat', values = 'Pourcentage')
            fg.update_traces(textposition='inside', textinfo='percent+label')
            fg.update(layout_showlegend = False)
            budget_lot.write(fg)



    

    


