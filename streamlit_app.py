# first py file.
import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

st.title("My parents new healthy Diner")

st.header("Breakfast Favorites:")
st.write("🥣 Omega 3 & blueberry oatmeal")
st.write("🥗 Kale, Spinach and Rocket smoothie")
st.write("🐔 Hard-boiled free-range egg")
st.write("🥑🍞 Avacado Toast")

st.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# set fruit name column as index
my_fruit_list = my_fruit_list.set_index('Fruit')

#set default values
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display table on the page
st. dataframe(fruits_to_show)


#fetch data from API- Fruityvice
# st.header('Fruityvice Fruit Advice!')
#take input from user to send a GET request through API call

# fruit_choice = st.text_input('What fruit would you like to know about?', 'Kiwi')
# st.write('The user entered: ', fruit_choice)



# New Section
st.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error('Please select a fruit to get inofrmation.')
  else:
    # pass user input into API call
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)
    # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    # st.text(fruityvice_response.json()) #just writes the data to the screen
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json()) #normalize the data
    # print as table
    st.dataframe(fruityvice_normalized)
except URLError as e:
  st.error()

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_rows)

# add secondary text input
add_my_fruit = st.text_input('Waht fruit would you like to add?' ,'jackfruit')
st.write('Thanks for adding ', add_my_fruit)

