# ---Modules

from janitor import xlsx_table
from matplotlib.pyplot import hist # extracting 'Tables' from a worksheet using the 'pyjanitor' module
import streamlit as st
from streamlit_option_menu import option_menu # using side bar menu in steamlit web page
#import plotly.figure_factory as ff
import plotly.express as px
from PIL import Image # To Upload an image 

from streamlit_extras.dataframe_explorer import dataframe_explorer
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

import warnings
warnings.simplefilter("ignore") #Ignore excel data validation error message

# Set the page layout to 'wide'
st.set_page_config(layout='wide')


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

background_color= '#FFFFFF'

with open('/Users/tariq/opt/miniconda3/envs/test1/Test1_Code/Test1_code/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ---Containers
image = st.container()
header = st.container()
metrics = st.container()
data = st.container()
overview = st.container()
pmt_lot = st.container()
budget_lot = st.container()
bets =st.container()

with image:
    #---Upload Morocco Mall Image
    image = Image.open('/Users/tariq/opt/miniconda3/envs/test1/Test1_Code/Test1_code/MMM.png')
    
    #---display image to match column width
    st.image(image, use_column_width= True) 
    

with metrics:
    st.markdown('## Metrics')

    col1, col2, col3, col4, = st.columns(4)
    col1.metric(" GO Mall", "312.5M")
    col2.metric(" GO Res.", "26.5M")
    col3.metric(" Archis Mall", "46.4M")
    col4.metric(" BETs Mall", "22.4M")


# This container includes the header and the title of the project
with header:
    st.header('AKSAL PROPERTY')
    st.header('DASHBOARD: MOROCCCO MALL MARRAKECH')
    st.markdown('''
    ----
    ''')


# Extraction data function  
@st.cache(allow_output_mutation=True)
def RECAP_MMM_upload():
    df = xlsx_table('/Users/tariq/Library/CloudStorage/OneDrive-Personal/WORK/MMM/TARIQ/Summary-PowerBI.xlsm', 'RECAP','RECAP_MMM')
    return df

# Extraction data function  
@st.cache(allow_output_mutation=True)
def RECAP_ETUDES_upload():
    df = xlsx_table('/Users/tariq/Library/CloudStorage/OneDrive-Personal/WORK/MMM/TARIQ/Summary-PowerBI.xlsm', 'RECAP','RECAP_ETUDES')
    return df

# Function extracting the table from Excel
@st.cache(allow_output_mutation=True)
def Budget_Par_Lot_upload():
    bpl = xlsx_table('/Users/tariq/Library/CloudStorage/OneDrive-Personal/WORK/MMM/TARIQ/Summary-PowerBI.xlsm', 'RECAP','Budget_Par_Lot')
    return bpl


with data:

    summary=RECAP_MMM_upload()
    

    #data.write(summary)
    st.info(len(summary))
    # Display table using the Aggrid module
    st.markdown('## A deep look into the data')
    gd_summary = GridOptionsBuilder.from_dataframe(summary)
    gd_summary.configure_pagination(enabled=True)
    gd_summary.configure_default_column(editable=True, groupable=True)
    #sel_mode = st.radio('Selection Type', options=["single", "multiple"])
    gd_summary.configure_selection(selection_mode= "single", use_checkbox=True)
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



with bets:

    st.header("Suivi Bureaux d'Etudes")
    bets = RECAP_ETUDES_upload()
    bets_hist = px.histogram(bets, x='PRESTATAIRES', y=['MARCHE HT', 'Régler  '],text_auto= '.2s',
    width= 1100, height= 600,
    barmode= 'group', labels= True)
    st.write(bets_hist)



# This container displays a Treemap showing an overview of the project 
with overview:

    st.header("Overview of the Project")
    st.subheader('Budget par Lot et Prestatire')

    # Treemap detailing "Budget par prestataire"
    summary_treemap = px.treemap(data_frame = summary, 
    path=['LOT', 'PRESTATAIRES', 'Lot Contrat'], values='MARCHE TTC',
    width= 1000, height= 500,
    labels= True)
    summary_treemap.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    
    # Define the type of the data to display on the layout
    summary_treemap.data[0].textinfo = 'label+text+value'
    # Disactivate the hovermode
    summary_treemap.layout.hovermode = False
    summary_treemap.update_traces(root_color="#FFFFFF")
    overview.write(summary_treemap)
    



# This containers displays a historam of "Paiements par Lots"
with pmt_lot:

    #Histogram detailing "Suivi de paiement par Lot"
    st.header("Suivi de paiement par lot")

    suivi_pmt_lot = RECAP_MMM_upload()
    suivi_pmt_lot_hist = px.histogram(suivi_pmt_lot, x= 'LOT', y= ['MARCHE HT','Régler  ','Réste à Régler '], text_auto= '.2s',
    width= 1000, height= 500,
    barmode= 'group', labels= True)
    
    # Change the histogram layout & traces
    suivi_pmt_lot_hist.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    suivi_pmt_lot_hist.update_traces(textposition='inside', text='label')
    
    # Disactivate the hovermode
    suivi_pmt_lot_hist.layout.hovermode = False
    summary_treemap.update_traces(root_color="#FFFFFF")
    pmt_lot.write(suivi_pmt_lot_hist)



# This container contains a bar and a pie chart
with budget_lot:

    # Container's header
    st.header('Répartition du Budget par Contrats')

    load = st.button('Import Data')

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



    

    
#figure = px.sunburst(summary, path=["LOT","Lot Contrat"], values='MARCHE TTC',
#hover_data=['MARCHE TTC'])

#figure.update_layout(margin = dict(t=0, l=0, r=0, b=0),
#autosize=False,
#height=500,width=500)
#figure.update_traces(textinfo="label+percent parent")
#figure.data[0].textinfo = 'label+text+value'
#st.write(figure)


#st.slider(label='Le Nombre de Lots que vous voulez afficher',min_value=0, max_value= 13, step=1)

#Extract the data cells from the 'budget_par_lot' table for the mectrics
archis=budget_par_lot['Budget'].loc[0]
#prct_archis=budget_par_lot['Pourcentage'].loc[0]

etudes=budget_par_lot['Budget'].loc[1]
mall_go=budget_par_lot['Budget'].loc[2]
res_go=budget_par_lot['Budget'].loc[3]
mall_mep=budget_par_lot['Budget'].loc[4]



#ROW A








# Read the tables names from the sheetname
# The keys will be loaded as a dictionary
#tables = xlsx_table('/Users/tariq/Library/CloudStorage/OneDrive-Personnel/WORK/MMM/TARIQ/Summary-Mac.xlsm','RECAP')
#st.write(tables.keys())

#st.write(tables['RECAP_MMM']

#Importing the PBI app from PBI publisher
#st.components.v1.iframe(src="https://app.powerbi.com/view?r=eyJrIjoiNGI0NDEzNmEtODNkMC00YjMzLTkxYmItNDdmNjM1NWUxOWZmIiwidCI6IjBlODhkMjhiLTE4YzgtNDk4OC04MDI0LWQ0ZWIzMzA3MWYxYSJ9", height=800, width=1300)


# Creating a menu bar using streamlit_option_menu module from streamlit
#with st.sidebar:
    #selected = option_menu(
#        menu_title="Main Menu", #required
#        options=["Overview", "Architects", "BETs"], #required
#        icons=["house", "book", "worksite"], #optional
#        menu_icon="cast", #optional
#        default_index=0, #optional
#        orientation="vertical",
   #)