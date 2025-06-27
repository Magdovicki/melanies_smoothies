# Import python packages
import streamlit as st
import requests

# Write directly to the app
st.title("🥤Customize Your Own Smoothie!🥤")

st.write(
  """
Chooese the fruits you want in your custome smoothie
  """
)

cnx= st.connection("snowflake")
session = cnx.session()
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:' ,name_on_order )
from snowflake.snowpark.functions import col
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(

    'Chooes up to 5 ingredients',
    my_dataframe, max_selections=5
)

ingredients_string= ''

for fruit_chosen in ingredients_list:
     ingredients_string += fruit_chosen + ' '
   
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

st.title("🍉 Watermelon Nutrition Info")

try:
    response = requests.get("https://www.fruityvice.com/api/fruit/watermelon")
    response.raise_for_status()
    data = response.json()
    st.json(data)
except requests.exceptions.RequestException as e:
    st.error(f"API call failed: {e}")
