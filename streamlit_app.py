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
def get_fruityvice_data(this_fruit_choice):
  # pass user input into API call
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +this_fruit_choice)
    # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    # st.text(fruityvice_response.json()) #just writes the data to the screen
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json()) #normalize the data
    return fruityvice_normalized
st.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error('Please select a fruit to get inofrmation.')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # print as table
    st.dataframe(back_from_function)
except URLError as e:
  st.error()
  
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute('select * from fruit_load_list')
    return my_cur.fetchall()
# add a button to load the fruit
if st.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
# my_cur = my_cnx.cursor()
# my_cur.execute("select * from fruit_load_list")
# my_data_rows = my_cur.fetchall()
# st.header("The fruit load list contains:")
  st.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit
# add secondary text input
add_my_fruit = st.text_input('Waht fruit would you like to add?')
if st.button('Add a Fruit to the list'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  st.text(back_from_function)
# st.write('Thanks for adding ', add_my_fruit)

