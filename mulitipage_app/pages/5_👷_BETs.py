from matplotlib import container
import streamlit as st
import plotly.express as px
from janitor import xlsx_table

bets =  st.container()

with bets:

     # Extraction data function  
    @st.cache(allow_output_mutation=True)
    def RECAP_ETUDES_upload():
        df = xlsx_table('/Users/tariq/Library/CloudStorage/OneDrive-Personal/WORK/MMM/TARIQ/Summary-PowerBI.xlsm', 'RECAP','RECAP_ETUDES')
        return df


    st.header("Suivi Bureaux d'Etudes")
    bets = RECAP_ETUDES_upload()
    bets_hist = px.histogram(bets, x='PRESTATAIRES', y=['MARCHE TTC', 'Régler  '],text_auto= '.2s',
    width= 1100, height= 600,
    barmode= 'group', labels= True)
    st.write(bets_hist)
