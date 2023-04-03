# first py file.
import streamlit as st
import pandas as pd

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

st.multiselect("Pick some fruits:", list(my_fruit_list.index))

#Display table on the page
st. dataframe(my_fruit_list)
