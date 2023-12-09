# Importaciones de módulos necesarios
from idlelib import window

import Movie
from SerializeFile import *
import PySimpleGUI as sg
import re
import operator
import pandas as pd

# List that will store the Movie objects read from the CSV file
movie_list2 = []

# Definition of regular expression patterns for validation
pattern_ID = r"\d{3}"
pattern_release_year = r"\d{4}"

def purgeMovies(movie_list, t_MovieInterfaz):
    # Read the CSV file and store the data in a DataFrame
    df = pd.read_csv('Movie.csv')

    # Delete rows that have 'erase' set to True
    df = df[df['erase'] != True]

    # Save the DataFrame back to the CSV file
    df.to_csv('Movie.csv', index=False)

# Function to add a new movie to the list and save the data in a CSV file.
def add_movie(movie_list, t_MovieInterfaz, oMovie, window):
    # Verify if the ID already exists
    if check_id_exists('Movie.csv', oMovie.ID):
        sg.popup_error('The ID already exists.')
        return

    # Si no hay una película con el mismo ID, procede a añadir la nueva película
    save_movie_csv('Movie.csv', oMovie)
    movie_list.append(oMovie)
    t_MovieInterfaz.append([oMovie.ID, oMovie.title, oMovie.director, oMovie.release_year])

    # Print statements for debugging
    print("Movie added successfully:")
    print("ID:", oMovie.ID)
    print("Title:", oMovie.title)
    print("Director:", oMovie.director)
    print("Release Year:", oMovie.release_year)

    # Update the table in the GUI
    window['-Table-'].update(t_MovieInterfaz)


# Function to remove a movie from the list and update the interface and the CSV file.
def delMovie(movie_list, t_MovieInterfaz, posinTable):
    # Read the CSV file and store the data in a DataFrame
    df = pd.read_csv('Movie.csv')

    # Search for the row that has the same ID as the movie to be deleted
    movie_id = t_MovieInterfaz[posinTable][0]
    mask = df['ID'] == movie_id

    # If such row is found, set the 'erase' value to True
    df.loc[mask, 'erase'] = True

    # Save the DataFrame back to the CSV file
    df.to_csv('Movie.csv', index=False)

    # Search for the movie in the list and delete it
    for o in movie_list:
        if o.ID == movie_id:
            o.erased = True
            break

    # Delete the movie from the interface list
    for i, movie in enumerate(t_MovieInterfaz):
        if movie[0] == movie_id:
            del t_MovieInterfaz[i]
            break

def check_id_exists(csv_filename, id_to_check):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_filename)

    # Convert the ID column to string
    df['ID'] = df['ID'].astype(str)

    # Check if the ID exists in the ID column
    if str(id_to_check) in df['ID'].values:
        return True
    else:
        return False

# Function to update a movie in the list and update the interface and the CSV file.
def updateMovie(movie_list, t_row_MovieInterfaz):
    # Read the CSV file and store the data in a DataFrame
    df = pd.read_csv('Movie.csv')

    # Get the ID of the movie to be updated
    movie_id = str(t_row_MovieInterfaz[0])
    df['ID'] = df['ID'].astype(str)

    # Search for the row that has the same ID as the movie to be updated
    mask = df['ID'] == movie_id

    # If such row is found, update the values of the columns
    if df.loc[mask].shape[0] > 0:
        df.loc[mask, 'title'] = t_row_MovieInterfaz[1]
        df.loc[mask, 'director'] = t_row_MovieInterfaz[2]
        df.loc[mask, 'release_year'] = t_row_MovieInterfaz[3]

        # Save the DataFrame back to the CSV file
        df.to_csv('Movie.csv', index=False)

        # Search for the movie in the list and update it
        for o in movie_list:
            if o.ID == movie_id:
                o.set_movie(t_row_MovieInterfaz[1], t_row_MovieInterfaz[2], t_row_MovieInterfaz[3])
                o.erased = False  # Set the 'erased' value to False
                break
    else:
        print("Error: No se encontró una película con el ID proporcionado.")

def handle_add_event(event, values, movie_list2, table_data, window):
    # Check if all fields have been filled
    if all([values['-ID-'], values['-Title-'], values['-Director-'], values['-ReleaseYear-']]):
        # Additional validations if needed
        valida = True  # Assuming valida is True for simplicity, you can add your validations here

        if valida:
            # Add the new movie to the list and update the interface
            new_movie = Movie(values['-ID-'], values['-Title-'], values['-Director-'], values['-ReleaseYear-'])
            add_movie(movie_list2, table_data, new_movie, window)

            # Clear the input fields after adding a movie
            window['-ID-'].update('')
            window['-Title-'].update('')
            window['-Director-'].update('')
            window['-ReleaseYear-'].update('')

    else:
        # Show an error message if any of the fields is empty
        sg.popup_error('Todos los campos deben estar rellenados')



def handle_delete_event(event, values, movie_list2, table_data, window):
    if len(values['-Table-']) > 0:
        delMovie(movie_list2, table_data, values['-Table-'][0])

        # Update the table in the GUI
        table_data.clear()
        for o in movie_list2:
            if not o.erased:
                table_data.append([o.ID, o.title, o.director, o.release_year])

        # Update the table in the GUI
        window['-Table-'].update(table_data)


def handle_modify_event(event, values, movie_list2, table_data, window):
    valida = False
    if re.match(pattern_ID, values['-ID-']):
        if re.match(pattern_release_year, values['-ReleaseYear-']):
            valida = True
    if valida:
        rowToUpdate = None
        for t in table_data:
            if str(t[0]) == values['-ID-']:
                rowToUpdate = t
                t[1], t[2], t[3] = values['-Title-'], values['-Director-'], values['-ReleaseYear-']
                break
        if rowToUpdate is None:
            print("Error: No se encontró una película con el ID proporcionado EN EL EVENTO.")
            return
        updateMovie(movie_list2, rowToUpdate)
        window['-Table-'].update(table_data)
        window['-ID-'].update(disabled=False)


# Function to read the data from the CSV file and store it in a list of Movie objects.
def interfaz():
    # Definición de fuentes para la interfaz
    font1, font2 = ('Calibri', 16), ('Calibri', 18)

    # Configure the PySimpleGUI theme
    sg.theme('DarkBlue3')
    sg.set_options(font=font1)

    # List that will store the data to be displayed in the table
    table_data = []

    # List that will store the data of the row to be updated
    rowToUpdate = []

    # Read the CSV file and store the data in a list of Movie objects
    movie_list2 = read_movie_csv('Movie.csv')

    # Store the data of the Movie objects in the list to be displayed in the table
    for o in movie_list2:
        table_data.append([o.ID, o.title, o.director, o.release_year])

    # Definition of the layout of the GUI
    layout = [
                 [sg.Push(), sg.Text('Movie CRUD'), sg.Push()]] + [
                 [sg.Text(text), sg.Push(), sg.Input(key=key)] for key, text in Movie.fields.items()] + [
                 [sg.Push()] +
                 [sg.Button(button) for button in ('Add', 'Delete', 'Modify', 'Clear')] +
                 [sg.Push()],
                 [sg.Table(values=table_data, headings=Movie.headings, max_col_width=50, num_rows=10,
                           display_row_numbers=False, justification='center', enable_events=True,
                           enable_click_events=True, vertical_scroll_only=False,
                           select_mode=sg.TABLE_SELECT_MODE_BROWSE, expand_x=True, bind_return_key=True,
                           key='-Table-')],
                 [sg.Button('Purge'), sg.Push(), sg.Button('Sort File')],
             ]
    sg.theme('DarkBlue3')
    # Create the window
    window = sg.Window('Movie Management with CSV', layout, finalize=True)

    window['-Table-'].bind("<Double-Button-1>", " Double")

    # Event loop. Read buttons, make callbacks
    while True:
        event, values = window.read()

        # Manage the window closing event
        if event == sg.WIN_CLOSED:
            break

        # Manage the event of adding a new movie
        if event == 'Add':
            handle_add_event(event, values, movie_list2, table_data, window)

        # Manage the event of deleting a movie
        if event == 'Delete':
            handle_delete_event(event, values, movie_list2, table_data, window)

        # Manage the event of double clicking on a row in the table
        if event == '-Table- Double':
            if len(values['-Table-']) > 0:
                row = values['-Table-'][0]
                window['-ID-'].update(disabled=True)
                window['-ID-'].update(str(table_data[row][0]))
                window['-Title-'].update(str(table_data[row][1]))
                window['-Director-'].update(str(table_data[row][2]))
                window['-ReleaseYear-'].update(str(table_data[row][3]))

        # Manage the event of clearing the fields
        if event == 'Clear':
            window['-ID-'].update(disabled=False)
            window['-ID-'].update('')
            window['-Title-'].update('')
            window['-Director-'].update('')
            window['-ReleaseYear-'].update('')

        # Manage the event of modifying a movie
        if event == 'Modify':
            handle_modify_event(event, values, movie_list2, table_data, window)

        # Manage the event of sorting the file
        if event == 'Sort File':
            # New window to select the value to sort by
            layout = ([[sg.Text('Select a value to sort by')],
                       [sg.Combo(['ID', 'title', 'director', 'release_year'], key='-COMBO-', default_value='release_year')],
                       [sg.Button('OK')]])
            sort_window = sg.Window('Sort File', layout)

            while True:  # Event Loop
                sort_event, sort_values = sort_window.read()
                if sort_event == 'OK':
                    sort_window.close()

                    df = pd.read_csv('Movie.csv')

                    # Order the DataFrame by the selected value
                    df.sort_values(by=sort_values['-COMBO-'], inplace=True)

                    # Write the sorted DataFrame back to the CSV file
                    df.to_csv('Movie.csv', index=False)
                    break
                elif sort_event == sg.WIN_CLOSED:
                    break
                else:
                    break

        # Manage the event of purging the file
        if event == 'Purge':
            purgeMovies(movie_list2, table_data)
            window['-Table-'].update(table_data)

    # close the window
    window.close()

# call the function
interfaz()

# End of GUIp.py
