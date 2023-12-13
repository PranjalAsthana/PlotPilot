import streamlit as st #bookreck
import pickle as pkl
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

st.title("PlotPilot:books::book:")

st.sidebar.markdown(":orange[App made by] :orange[-] :orange[[Pranjal Asthana](https://github.com/PranjalAsthana)]")
st.sidebar.markdown(":orange[[Please Support PlotPilot on Github](https://github.com/PranjalAsthana/PlotPilot)]")

books = pkl.load(open("booksdata.pkl", "rb"))
book_pivot = pkl.load(open("book_pivot.pkl", "rb")) #pd.read_pickle("book_pivot.pkl")
book_indices = pkl.load(open("book_indices.pkl", "rb")) #pd.read_pickle("book_indices.pkl")

model = NearestNeighbors(algorithm='brute')
model.fit(book_pivot) 


def recommend(book_name):
    #book_id=np.where(book_pivot.index==book_name)[0][0]
    book_id= book_indices[book_name]
    #suggestions = sorted(list(enumerate(book_pivot[book_id])), reverse=True, key=lambda x: x[1])
    distances, suggestions = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6)
    suggbooks = []
    suggposters = []
    suggauthors = []
    for i in range(len(suggestions)):
    # if i==0:
    #   print("The suggestions for",book_name, "are: ")
        if not i:
            for j in range(1,6):
                bookname = book_pivot.index[suggestions[i]][j]
                print(suggestions[i][j])
                suggbooks.append(bookname)
                suggposters.append(books['poster'][suggestions[i][j]])
                suggauthors.append(books['author'][suggestions[i][j]])
                #print(books['poster'][])
                #postid = np.where(book_pivot.index[suggestions[i]][j])
                #suggposters.append(postid
    # for i in range(len(suggbooks)):
    #   print(suggbooks[i])
    #   print(suggposters[i])
    return suggbooks, suggposters, suggauthors


def fetchposter(book_name):
    #response = requests.get('https://bookcover-api.herokuapp.com/bookcover/{}'.format(movie_id))
    #data = response.json()
    book_id=np.where(book_pivot.index==book_name)[0][0]
    poster_path = books['poster'][book_id]
    #print(data)
    return poster_path


def drop_after_brace(input_string):
    result = ''
    brace_encountered = False

    for char in input_string:
        if char == '{':
            brace_encountered = True
        if not brace_encountered:
            result += char

    return result


def getAuthor(song):
    index = books[books['title'] == song].index[0]
    author = books.iloc[index].author
    return author


booklist = books['title'].values,'{ ', books['author'].values, ' }'
selected_book = st.selectbox(
    "Select a song you like from the menu below",
    books['title'].values#booklist
) 

#selectedtype = st.selectbox("What do you want to do?", books['author'].values)
#selected_book = drop_after_brace(selected_book)

#st.button("check clicking")

if st.button('Recommend'):
    recommended_book_names, recommended_book_posters, recommended_author_names = recommend(selected_book)
    author = getAuthor(selected_book)
    # = fetchposter(selected_book)
    st.write(f"Since you like {selected_book} by {author}, you may also like:")
    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        st.image(recommended_book_posters[0])
        st.write(recommended_book_names[0],"by",recommended_author_names[0])
    with col2:
        st.image(recommended_book_posters[1])
        st.write(recommended_book_names[1],"by",recommended_author_names[1])
    with col3:
        st.image(recommended_book_posters[2])
        st.write(recommended_book_names[2],"by",recommended_author_names[2])
    with col4:
        st.image(recommended_book_posters[3])
        st.write(recommended_book_names[3],"by",recommended_author_names[3])
    with col5:
        st.image(recommended_book_posters[4])
        st.write(recommended_book_names[4],"by",recommended_author_names[4])