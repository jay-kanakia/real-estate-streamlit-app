import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title='Price Predictor 💰')

with open('pipeline.pkl', 'rb') as file:
    pipe=pickle.load(file)
with open('df.pkl', 'rb') as file1:
    df=pickle.load(file1)


st.header("Enter your Input")

property_type=st.selectbox('Property Type',sorted(df['property_type'].unique()))
sector=st.selectbox('Sector',sorted(df['sector'].unique()))
builtup=float(st.number_input('Buit-up Area'))
bedRoom=st.selectbox('Bed Room',sorted(df['bedRoom'].unique()))
bathroom=st.selectbox('Bathrooms',sorted(df['bathroom'].unique()))
balcony=st.selectbox('Balcony',sorted(df['balcony'].unique()))
agePossession=st.selectbox('Age Possession',sorted(df['agePossession'].unique()))
furnish_type=st.selectbox('Furnish Type',sorted(df['furnish_type'].unique()))
servant_room=st.selectbox('Servant Room',['Yes','No'])
if servant_room=='Yes':
    servant_room=int(1.0)
else:
    servant_room=int(0.0)
store_room=st.selectbox('Store Room',['Yes','No'])
if store_room=='Yes':
    store_room=int(1.0)
else:
    store_room=int(0.0)
floorNum_category=st.selectbox('Floor Category',sorted(df['floorNum_category'].unique()))
luxury_score_category=st.selectbox('Luxury type',sorted(df['luxury_score_category'].unique()))
but=st.button("Predict")

if but:
    data = [[property_type,sector,builtup,bedRoom,bathroom,balcony,agePossession,furnish_type,servant_room,store_room,floorNum_category,luxury_score_category]]
    columns = ['property_type', 'sector', 'builtup', 'bedRoom', 'bathroom',
               'balcony', 'agePossession', 'furnish_type', 'servant_room',
               'store_room', 'floorNum_category', 'luxury_score_category']

    one_df = pd.DataFrame(data, columns=columns)
    actual_val = np.expm1(pipe.predict(one_df))
    min_val = np.expm1(pipe.predict(one_df)) - (53.16 / 2)
    max_val = np.expm1(pipe.predict(one_df)) + (53.16 / 2)

    st.text(f'The Predicted Price of the Property is {round(actual_val[0], 2)} lacs')
    st.text(f'The Price of the Property is expected in between {round(min_val[0],2)} lacs and {round(max_val[0],2)} lacs')
