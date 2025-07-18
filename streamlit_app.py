# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd
# Write directly to the app
st.title("🥤Customize Your Own Smoothie!🥤")
st.write(
  """
Chooese the fruits you want in your custome smoothie
  """
)
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:' ,name_on_order )
cnx = cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col ('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
pd_df= my_dataframe.to_pandas()


ingredients_list = st.multiselect(

    'Chooes up to 5 ingredients',
    my_dataframe, max_selections=5
)

ingredients_string= ''

for fruit_chosen in ingredients_list:
     ingredients_string += fruit_chosen + ' '
     search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
     #st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
     st.subheader(fruit_chosen + ' Nutrition Information')
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
     fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width= True)
   
#st.write(ingredients_string)


my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
values('""" + ingredients_string + """', '""" + name_on_order+ """')"""
time_to_insert = st.button('Submit Order')

#st.write(my_insert_stmt)
#st.stop()

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!'+', '+ name_on_order, icon="✅"
              )

