
import streamlit


import streamlit as st
from janitor import xlsx_table
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder


data = st.container()

with data:
   
    @st.cache(allow_output_mutation=True)
    def RECAP_MMM_upload():
        df = xlsx_table('/Users/tariq/Library/CloudStorage/OneDrive-Personal/WORK/MMM/TARIQ/Summary-PowerBI.xlsm', 'RECAP','RECAP_MMM')
        return df
   
    summary=RECAP_MMM_upload()
    
    #data.write(summary)
    #st.info(len(summary))
    # Display table using the Aggrid module
    st.markdown('## A deep look into the data')

    gd_summary = GridOptionsBuilder.from_dataframe(summary)
    gd_summary.configure_pagination(enabled=True, paginationPageSize=10)
    gd_summary.configure_default_column(editable=True, groupable=True)
    sel_mode = st.radio('Selection Type', options=["single", "multiple"])
    gd_summary.configure_selection(selection_mode='sel_mode', use_checkbox=True)
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
    
