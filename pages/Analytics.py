import streamlit as st
import pandas as pd
import pickle
from wordcloud import WordCloud
import seaborn as sns
import matplotlib.pyplot as plt


st.set_page_config(page_title='Plotting Demo')
st.title('Analytics')

new_df=pd.read_csv('project_6_dataViz.csv')

with open('feature_text.pkl','rb') as file:
    feature_text=pickle.load(file)

group_df=new_df[['sector','price_in_lacs','price_per_sqft_inrs','builtup','latitude', 'longitude']].groupby('sector').mean()

st.header('Sector price per Sq.ft.')
import plotly.express as px
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft_inrs", size='builtup',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",text=group_df.index)
st.plotly_chart(fig, use_container_width=True)

st.header('Feature WordCloud')
plt.rcParams["font.family"] = "Arial"

wordcloud = WordCloud(width = 800, height = 800,
                      background_color ='white',
                      stopwords = set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(feature_text)

fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
plt.tight_layout(pad=0)
#plt.show()
st.pyplot(fig)

st.header('Propety type vs Price')

property_type=st.selectbox('Select Property type',new_df['property_type'].unique())

if property_type=='house':
    fig = px.scatter(new_df[new_df['property_type'] == 'house'], x="builtup", y="price_in_lacs", color="bedRoom", title="Area Vs Price")
    st.plotly_chart(fig, use_container_width=True)
else :
    fig = px.scatter(new_df[new_df['property_type'] == 'flat'], x="builtup", y="price_in_lacs", color="bedRoom",
                     title="Area Vs Price")
    st.plotly_chart(fig, use_container_width=True)

st.header('Side by Side BHK price comparison')

select_sector=new_df['sector'].unique().tolist()
select_sector.insert(0,'Over all')

selected_sector=st.selectbox('Select Sector',select_sector)

if selected_sector=='Over all':
    temp_df = new_df[new_df['bedRoom'] <= 4]
    # Create side-by-side boxplots of the total bill amounts by day
    fig = px.box(temp_df, x='bedRoom', y='price_in_lacs', title='BHK Price Range')
    st.plotly_chart(fig, use_container_width=True)

else :
    temp_df = new_df[(new_df['bedRoom'] <= 4)&(new_df['sector']==selected_sector)]
    # Create side-by-side boxplots of the total bill amounts by day
    fig = px.box(temp_df, x='bedRoom', y='price_in_lacs', title='BHK Price Range')
    st.plotly_chart(fig, use_container_width=True)


st.header('BHK Pie Chart')

selected_sector1=st.selectbox('Select one Sector',select_sector)

if selected_sector1=='Over all':
    fig = px.pie(new_df, names='bedRoom', title='Total Bedroom')
    st.plotly_chart(fig, use_container_width=True)

else :
    temp_df = new_df[new_df['sector']==selected_sector1]
    fig = px.pie(temp_df, names='bedRoom', title='Total Bedroom')
    st.plotly_chart(fig, use_container_width=True)


st.header('Side by Side Distplot for property type')

fig3 = plt.figure(figsize=(10, 4))
sns.histplot(new_df[new_df['property_type'] == 'house']['price_in_lacs'],label='house',kde=True)
sns.histplot(new_df[new_df['property_type'] == 'flat']['price_in_lacs'], label='flat',kde=True)
plt.legend()
st.pyplot(fig3)

