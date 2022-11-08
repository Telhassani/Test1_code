import pandas as pd
import xlrd as xl
from janitor import xlsx_table # extracting 'Tables' from a worksheet using the 'pyjanitor' module
import streamlit as st
from streamlit_option_menu import option_menu # using side bar menu in steamlit web page

##Read Excel file from path
##Read the file from OneDrive after granting access to VsCode
#xls = pd.ExcelFile('/Users/tariq/Library/CloudStorage/OneDrive-Personnel/WORK/MMM/TARIQ/Summary-Mac.xlsm')

## Get all the sheet names of the excel file
#Sheet_Names = xls.sheet_names
#Sheet_Names

##Read data from a specific sheet in the excel file
#df = pd.read_excel(xls, 'RECAP')
#df
#st.dataframe(df)


#Reading a specific table in the worksheet
#xlsx_table('/Users/tariq/Library/CloudStorage/OneDrive-Personnel/WORK/MMM/TARIQ/Summary-Mac.xlsm', 'RECAP','RECAP_MMM')

# Read the tables names from the sheetname
# The keys will be loaded as a dictionary
tables = xlsx_table('/Users/tariq/Library/CloudStorage/OneDrive-Personnel/WORK/MMM/TARIQ/Summary-Mac.xlsm','RECAP')
tables.keys()



# Read 'RECAP_TRAVAUX' table
#tables['RECAP_TRAVAUX']
#tables['RECAP_MMM']
#tables['Avancement_Archis']

#Configuration of the layout and the side bar (expanded in this case)
#st.set_page_config(layout='wide', initial_sidebar_state='expanded')



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