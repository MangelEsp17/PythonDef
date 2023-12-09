class Movie:
    # Class variables for table headings and field labels
    headings = ['ID', 'Title', 'Director', 'Release Year']
    fields = {
        '-ID-': 'Movie ID:',
        '-Title-': 'Movie Title:',
        '-Director-': 'Director:',
        '-ReleaseYear-': 'Release Year:'
    }

    def __init__(self, ID, title, director, release_year):
        # Instance variables for movie details
        self.ID = ID
        self.title = title
        self.director = director
        self.release_year = release_year
        self.erased = False

    def __eq__(self, other_movie):
        # Overriding the equality operator to compare movies based on their ID
        return other_movie.ID == self.ID

    def __str__(self):
        # Overriding the string representation of the movie object
        return f"{self.ID} {self.title} {self.director} {self.release_year}"

    def set_movie(self, title, director, release_year):
        # Method to update movie details
        self.title = title
        self.director = director
        self.release_year = release_year
