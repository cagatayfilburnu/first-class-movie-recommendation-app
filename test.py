import streamlit as st
from PIL import Image
import warnings
import datetime
from datetime import datetime
import numpy as np
import pandas as pd
import random

warnings.filterwarnings("ignore")
pd.set_option("display.float_format", lambda x: "%.1f" % x)

# Main title
st.set_page_config(page_title="First-Class Movie Recommendation App", page_icon=":First-Class", layout="centered")


# Importing Movie Dataset and IMDB Top 250 Movies Dataset
@st.cache
def load_data():
    user_df = pd.read_csv("dataset/user_df_dataset.csv")
    return user_df


top_movies_list = pd.read_csv("dataset/IMDB Top 250 Movies.csv")
df = load_data()

# Creating movie list with df.columns
movies_list = list()
for col in df.columns:
    if col == "userId":
        continue
    else:
        movies_list.append(col)


# Creating random select according to movie list
class MovieSelector:
    def __init__(self, movies):
        self.movies = movies

    def select_movie(self, movie_list):
        index = random.randint(0, 3158)
        selected_movie = movie_list[index]
        if st.sidebar.button('Click'):
            st.sidebar.info(f"Random film: {selected_movie}")


selector = MovieSelector(movies_list)

# Main Header Settings
image_1 = Image.open("images/first_film_image.jpg")
image_2 = Image.open("images/216423409-b19f9c54-a1c9-475d-a6d0-77da7073595c.png")
st.title("First-Class Movie Recommendation App")
st.image(image_2)
st.subheader("Hi there! Welcome to YetGen First-Class Project App 👋")

# Page Tabs Settings and Random Movie Part
current_time = datetime.now().strftime("%d-%m-%Y")
tabs = ["Introduction", "Movie List", "Top 250 Movie in IMDB", "Movie Recommendation System", "Contributors"]
page = st.sidebar.radio("Pages", tabs)
st.sidebar.info(f"Today's Date: {current_time}")
name = st.sidebar.text_input("Please enter a name: ")


selector.select_movie(movies_list)

# This code provides to hide index column in st.table
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """


# Functions for Recommendation System
def creating_user_df(movies_data, ratings_data):
    df = movies_data.merge(ratings_data, how="left", on="movieId")
    comments_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comments_counts.loc[(comments_counts["title"] <= 1000)].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_df


def basic_recommender(movie, dataframe):
    try:
        if movie not in dataframe.columns:
            raise KeyError("Oh, something was wrong, please control your movie ID in Movie List!")
        movie = dataframe[movie]
        return dataframe.corrwith(movie).sort_values(ascending=False).head(10)
    except ValueError:
        return f"Oh, something was wrong, please control your movie ID in Movie List!"


# Pages Part
if page == "Introduction":
    st.subheader("Introduction")
    st.image(image_1)
    st.markdown("- This webapp was created for a final project week in YetGen Core Python Program.")
    st.markdown("""
    - There are five pages that are Introduction, Movie List, Top 250 Movie in IMDB, 
    Movie Recommendation System and Contributors.
    """)
    st.markdown("""
    - This study aims to recommend ten movie for user according to dataset and item-based collaborative filtering. 
    Besides, using streamlit package to interaction with potential users who want to watch a film based on user's 
    similar movie.
    """)
    st.markdown("""- Please note that, movie recommendation system based on a old dataset. Also there is a Top 250 Movies 
    but it does not include in recommendation system.
    """)
    st.markdown("""- For use the recommendation system, please set the page 'Movie Recommendation System'""")

    st. markdown("""- In addition, there is a bonus feature that provides random movies according to Top 250 Movies in 
    IMDB and movie dataset. You can access this part app's left side and only click the button.
    """)

elif page == "Movie List":
    st.info('This is a sweetie informational message ℹ️')
    st.markdown("""In this page, you can access our movie dataset. There are 3159 movie and if you watched someone,
    you can take the movie name that has to be same in this list then, enter your movie name movie recommendation 
    system. After that, get our recommend movies for you! 
    """)
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(df.columns[1:3158])

elif page == "Top 250 Movie in IMDB":
    st.markdown("""In this page, you can see the top 250 Movie in IMDB according to users' ratings. 
    Recommendation System does not contain these movies. However, you can see a random top tier IMDB movie if you click
    a button left side!
    """)
    col_list = ["rank", "name", "rating"]
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(top_movies_list[col_list])

elif page == "Movie Recommendation System":
    st.subheader("Movie Recommendation System")
    user_film = st.text_input('Enter your movie name, and see our 10 recommendations based on your movie!')
    rec_film = basic_recommender(user_film, df)
    recommend_table = pd.DataFrame(rec_film)
    st.write("Our recommends: ", recommend_table)


elif page == "Contributors":
    st.subheader("Contributors")

    st.subheader("References")
    st.markdown("""
    1. https://docs.streamlit.io/
    2. https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset
    3. https://www.kaggle.com/datasets/rajugc/imdb-top-250-movies-dataset
    """)
    st.subheader("Thanks")
    st.markdown("")
