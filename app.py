import streamlit as st #bookreck
import pickle as pkl
import pandas as pd
import requests

st.title("PlotPilot:books::book:")

def fetchposter(movie_id):
    response = requests.get('https://bookcover-api.herokuapp.com/bookcover/{}'.format(movie_id))
    data = response.json()
    poster_path = data['poster_path']
    #print(data)
    return poster_path

def recommend(book):
    movie_index = movies[movies['title'] == book].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True, key = lambda x:x[1])

    reccmovies = []
    reccmoviesposter = []

    for i in movies_list[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        #
        reccmovies.append(movies.iloc[i[0]].title)
        reccmoviesposter.append(fetchposter(movie_id))

    return reccmovies,reccmoviesposter

movies_dict = pkl.load(open('movies_dict.pkl', 'rb'))
similarity = pkl.load(open('similaritymatrix.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

selectedmovie = st.selectbox(
    'Select a movie you like from the menu below',
    movies['title'].values)

#movies = movies['title'].values

if st.button('Recommend'):
    names, posters = recommend(selectedmovie)
    st.write(f"Since you like {selectedmovie}, you may also like:")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.write(names[0])
    with col2:
        st.image(posters[1])
        st.write(names[1])
    with col3:
        st.image(posters[2])
        st.write(names[2])
    with col4:
        st.image(posters[3])
        st.write(names[3])
    with col5:
        st.image(posters[4])
        st.write(names[4])