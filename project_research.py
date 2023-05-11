import numpy as np
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)

rating = pd.read_csv("dataset/rating.csv")
movies = pd.read_csv("dataset/movie.csv")

def creating_user_df(movies_data, ratings_data):
    df = movies_data.merge(ratings_data, how="left", on="movieId")
    comments_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comments_counts.loc[(comments_counts["title"] <= 1000)].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_df


df = creating_user_df(movies, rating)
# noinspection PyBroadException
def basic_recommender(movie, dataframe):
    try:
        movie = dataframe[movie]
        return dataframe.corrwith(movie).sort_values(ascending=False).head(10)
    except:
        print(f"There is a mistake for film ID!")


basic_recommender("X-Men (2000)", df)

# Export user_df to csv
df.to_csv("user_df_dataset.csv", header=True, index=True)
