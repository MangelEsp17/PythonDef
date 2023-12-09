from Movie import Movie

# CSV
import pandas as pd

def save_movie_csv(csv_filename, movie):
    # Create a Pandas DataFrame from the Movie object
    movie_data = {
        "ID": [movie.ID],
        "title": [movie.title],
        "director": [movie.director],
        "release_year": [movie.release_year],
        "erased": [movie.erased]
    }
    df = pd.DataFrame(movie_data)

    # 'a' mode to append at the end of the file if it already exists
    df.to_csv(csv_filename, mode='a', index=False, header=not pd.io.common.file_exists(csv_filename))

def modify_movie_csv(csv_filename, movie):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_filename)

    # Find the row that has the same ID as the movie to be updated
    mask = df['ID'] == movie.ID

    # If such a row is found, update the values of that row with the new values of the movie
    df.loc[mask, ['ID', 'title', 'director', 'release_year']] = [movie.ID, movie.title, movie.director, movie.release_year]

    # Save the DataFrame back to the CSV file
    df.to_csv(csv_filename, index=False)

def read_movie_csv(csv_filename):
    try:
        # Try to read the CSV file into a DataFrame
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        # Print an error message if the file is not found
        print(f"Error: The file {csv_filename} was not found.")
        return []

    if df is None or df.empty:
        # Print a warning if the DataFrame is empty
        print("Warning: The DataFrame is empty.")
        return []

    # List that will store the Movie objects
    movie_list: list[Movie] = []

    # Iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        # Only add to the list if 'erase' is False
        if row['erase'] == False:
            movie_list.append(Movie(row['ID'], row['title'], row['director'], row['release_year']))

    return movie_list
