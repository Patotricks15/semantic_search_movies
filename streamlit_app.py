import streamlit as st
from generate_vectors import MoviesVectorDataBase
import os
import streamlit as st


db = MoviesVectorDataBase()
db.generate_vectors()

# Function to load a CSS file and inject its content into the page
def local_css(file_name):
    """
    Load a CSS file and inject its content into the page.

    Args:
        file_name (str): Path to the CSS file
    """
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load CSS files
css_path = os.path.join("css", "general.css")
local_css(css_path)

css_path = os.path.join("css", "components.css")
local_css(css_path)

# Initialize the movie database
db = MoviesVectorDataBase()
db.generate_vectors()

# Function to get recommended movies based on search term
def get_recommended_movies(search: str, n: int = 3):
    """
    Retrieve a list of recommended movies based on the semantic similarity to a search term.

    Args:
        search (str): The search term used to find similar movie plots.
        n (int, optional): The number of recommended movies to retrieve. Defaults to 3.

    Returns:
        list: A list of dictionaries, each containing details of a recommended movie,
        including title, plot, genres, runtime, cast, number of comments, poster URL,
        IMDb rating, IMDb votes, and directors.
    """

    recommended_movies = []
    searches = db.client.query_points(
        collection_name="movies",
        query=db.encoder.encode(search).tolist(),
        limit=n
    ).points

    # Extract relevant movie data and append to the list
    for search in searches:
        movie = {
            "title": search.payload["title"],
            "plot": search.payload["fullplot"],
            "genres": search.payload["genres"],
            "runtime": search.payload["runtime"],
            "cast": search.payload["cast"],
            "num_mflix_comments": search.payload["num_mflix_comments"],
            "poster": search.payload["poster"],
            "imdb_rating": search.payload["imdb"]["rating"],
            "imdb_votes": search.payload["imdb"]["votes"],
            "directors": search.payload["directors"]
        }
        recommended_movies.append(movie)

    return recommended_movies

# Function to display the movie carousel
def display_carousel(data):
    for movie in data:
        col1, col2, col3 = st.columns([3, 7, 2])  # Defines two columns for layout
        with col1:
            # Display the movie poster
            st.image(movie['poster'], use_container_width=True)
        with col2:
            st.subheader(movie['title'])
            st.markdown(movie['plot'][:400] + "...")
            
        with col3:
            # Display movie title and relevant information
            st.markdown(f"**Rating**: {movie['imdb_rating']}/10 ({movie['imdb_votes']})")
            st.markdown(f"**Genres**: {', '.join(movie['genres'])}")
            st.markdown(f"**Runtime**: {movie['runtime']} mins")
            st.markdown(f"**Cast**: {', '.join(movie['cast'])}")
            st.markdown(f"**Directors**: {', '.join(movie['directors'])}")
        st.markdown("---")

# Title of the carousel
st.title("Movie Semantic Search")

# Text input for the user to enter a search term
search_term = st.text_input("Enter a search term for movie recommendations:", "mars")

# Slider to let the user choose how many movies to display
num_movies = st.slider("Number of movies to display:", 1, 10, 3)

# Button to generate recommendations and display the carousel
if st.button('Generate Recommendations'):
    # Get recommended movies based on the search term
    recommended_movies = get_recommended_movies(search_term, num_movies)
    # Display the movie carousel
    display_carousel(recommended_movies)

