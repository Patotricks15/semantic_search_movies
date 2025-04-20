import streamlit as st
from generate_vectors import MoviesVectorDataBase
import os

db = MoviesVectorDataBase()
db.generate_vectors()

# Function to load a CSS file and inject its content into the page
def local_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load CSS files
css_path = os.path.join("css", "general.css")
local_css(css_path)

css_path = os.path.join("css", "components.css")
local_css(css_path)

def get_recommended_movies(search: str, n: int = 3):
    message = ''
    searches = db.client.query_points(
        collection_name="movies",
        query=db.encoder.encode(search).tolist(),
        limit=n
    ).points

    for search in searches:
        message += f"**{search.payload['title']}**\n"
        message += f"{search.payload['fullplot']}\n"
        message += '------\n'

    return message

st.title('Semantic movie recommentation')

search_term = st.text_input("Type a keyword to search:", "mars")

num_movies = st.slider("Number of movies:", 1, 10, 3)

if st.button('Generate recommendations'):
    result = get_recommended_movies(search_term, num_movies)
    st.text_area("Recommended movies:", result, height=300)
