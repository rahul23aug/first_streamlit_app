import streamlit
import pandas
import requests
from urllib.error import URLError
import snowflake.connector

streamlit.title("MY FIRST STREAMLIT APP")
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.dataframe(my_fruit_list)
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
streamlit.header("Fruityvice Fruit Advice!")
#streamlit.text(fruityvice_response)
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("Please select a fruit")
    else:
      streamlit.write('The user entered ', fruit_choice)
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      #normalize json 
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # get df
      streamlit.dataframe(fruityvice_normalized)
except URLError as e:
      streamlit.error()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load text contains:")
streamlit.dataframe(my_data_row)
#allow end user to add fruit to the list 
add_fruit = streamlit.text_input('What fruit would you like to add?')
print(add_fruit)
my_cur.execute("INSERT INTO  FRUIT_LOAD_LIST VALUES ('{}')".format(add_fruit))

