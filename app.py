import os
import glob
import pandas as pd
import streamlit as st
import json

def load_data():
    with open("data/pokemon_file_paths.json") as p:
        data = json.load(p)
    return data

data = load_data()

inv_data = {value:key for key, value in data.items()}

range_limit = st.slider("Select the range you want to search in", min_value=0, max_value=255, step=5)

pokemon_selector = st.selectbox("Select the Pokémon you want to use for comparison", data.keys())

def is_within_range(value, target_value):
    return abs(value - target_value) <= range_limit

matching_files = []

submit = st.button("Find my Pokémon!")

if submit:

    # Read File A into a DataFrame using pandas (assuming it's also a CSV)
    df_file_a = pd.read_csv(data[pokemon_selector])

    # Iterate over all files in the folder path
    for file in list(data.values()):

        try:
            
            # Check if it's a CSV file (optional)
            if file != data[pokemon_selector]:
            
                # Read another CSV file into a DataFrame using pandas 
                df_other_file = pd.read_csv(file)
            
                # Flag variable to track if all values are within range for this file 
                all_within_range = True
            
                # Iterate over each column/data point and check if it's within range 
                column_data_other_file = df_other_file["val"].values
            
                # Get corresponding value from File A DataFrame based on column name 
                target_value_file_a = df_file_a["val"].values
            
                # Check if any value in this column is outside of the specified range limit
                for val1, val2 in zip(column_data_other_file, target_value_file_a):
                    if not is_within_range(val1, val2).any():
                        all_within_range = False
            
                # If all values are within their respective ranges, add this file name to matching_files list
                if all_within_range:
                    pokemon_name = inv_data[file]
                    matching_files.append(pokemon_name.capitalize())
        
        except Exception as e:
            st.error(e)
    
    # Print the matching file names
    if not matching_files:
        st.warning("Sorry, we couldn't find any Pokémon within that base stat range. Maybe try increasing it?")
    else:
        st.subheader(f"Congratulations! We found {len(matching_files)} matching Pokémon:")
        for filename in matching_files:
            st.markdown(filename)