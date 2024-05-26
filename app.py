import streamlit as st
import pickle
import pandas as pd
import requests

def fetchPoster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4adfbf9ae034c42098a91cfaa878864d'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/ "+data['poster_path']
def recommend(movie):
    movieIdx = movies_list[movies_list['title'] == movie].index[0]
    recommend_list = sorted(list(enumerate(similarity[movieIdx])), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movie_posters = []
    for i in recommend_list:
        movie_id = movies_list.iloc[i[0]]['movie_id']
        recommended_movie_posters.append(fetchPoster(movie_id))
        recommended_movies .append(movies_list.iloc[i[0]]['title'])
    return recommended_movies, recommended_movie_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movies_list = pd.DataFrame(movies_dict)
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies_list['title'].values)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i,col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])
