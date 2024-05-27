import pandas as pd
import os
import gzip

def read_zipped_csv(input_file):
    if input_file.endswith('.gz'):
        with gzip.open(input_file, 'rt', encoding='utf-8') as file:
            df = pd.read_csv(file)
    else:
        df = pd.read_csv(input_file)
    return df

def merge_df(input1, input2, output_file, name):
    df = pd.read_csv(input1)
    df2 = pd.read_csv(input2)

    # Select columns to use
    columns_to_merge = ['id', 'last_scraped', 'property_type', 'accommodates', 'bathrooms', 'bedrooms', 'beds', 'amenities', 'maximum_nights', 'review_scores_rating','review_scores_accuracy','review_scores_cleanliness','review_scores_checkin','review_scores_communication','review_scores_location','review_scores_value']

    # Merge selected columns from df to df2 based on the 'id' column
    df2_merged = pd.merge(df2, df[columns_to_merge], on='id', how='left')

    # Add an Area column to distinguish between states and cities
    df2_merged['Area'] = name

    df2_merged.to_csv(output_file, index=False)
    print("Merged data saved to:", output_file)

# Merge full listings file with listings file of each state folder
def merge_listings_of_each_state(state_folder):
    state_name = os.path.basename(state_folder)
    
    input_file1 = os.path.join(state_folder, 'listings_full.csv')
    input_file2 = os.path.join(state_folder, 'listings.csv')
    output_file = os.path.join(state_folder, 'merged_listings.csv')

    merge_df(input_file1, input_file2, output_file, state_name)

def merge_all_states_files_into_final(data_folder, file_name):
    merged_files = [] 
    
    for name in os.listdir(data_folder):
        folder = os.path.join(data_folder, name)
        if os.path.isdir(folder):
            merged_files.append(os.path.join(folder, file_name))
    
    # Merge all the merged listings files into one DataFrame
    merged_df = pd.concat([pd.read_csv(file) for file in merged_files], ignore_index=True)
    
    # Save the merged DataFrame to a single CSV file
    output_file = os.path.join(data_folder, 'all_states_listings.csv')
    merged_df.to_csv(output_file, index=False)
    print("All states merged data saved to:", output_file)

def merge_all_neighbourhoods(data_folder):
    merged_files = [] 
    
    for name in os.listdir(data_folder):
        folder = os.path.join(data_folder, name)
        if os.path.isdir(folder):
            file_path = os.path.join(folder, 'neighbourhoods.csv')
            if os.path.exists(file_path):  # Ensure the file exists before appending
                df = pd.read_csv(file_path)
                df['State'] = name  # Add a new column 'State' with the folder name
                merged_files.append(df)
    
    # Merge all the DataFrames into one DataFrame
    merged_df = pd.concat(merged_files, ignore_index=True)
    
    # Save the merged DataFrame to a single CSV file
    output_file = os.path.join(data_folder, 'all_states_merged_neighbourhoods.csv')
    merged_df.to_csv(output_file, index=False)
    print("All states merged data saved to:", output_file)

# Path to the directory containing state folders
data_folder = "data"

# Merge two listings for each folder
# Loop through each state folder
for name in os.listdir(data_folder):
    folder = os.path.join(data_folder, name)
    if os.path.isdir(folder):
        merge_listings_of_each_state(folder)    

merge_all_states_files_into_final(data_folder, 'merged_listings.csv')
merge_all_neighbourhoods(data_folder)
