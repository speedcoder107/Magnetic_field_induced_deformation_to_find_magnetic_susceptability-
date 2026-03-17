import csv
import os
from PIL import Image
import pandas as pd
import numpy as np

def find_red_circle_diameters_and_distances(folder_path):
    # Initialize lists to store diameters and distances
    diameters = []
    distances_to_bottom = []
    
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".JPG") or filename.endswith(".jpeg"):
            # Open the image
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            # Convert image to RGB mode
            image_rgb = image.convert("RGB")
            
            # Get image size
            width, height = image.size
            
            # Initialize variables to store the top and bottom boundaries of the circle
            top_boundary = None
            bottom_boundary = None
            
            # Scan from top to bottom to find the red circle
            for y in range(height):
                for x in range(width):
                    # Get pixel color
                    r, g, b = image_rgb.getpixel((x, y))
                    
                    # Check if the pixel is red
                    if r > 200 and g > 82 and b > 120:
                        try:
                            r_1, g_1, b_1 = image_rgb.getpixel((x+1, y))
                            r_2, g_2, b_2 = image_rgb.getpixel((x-1, y))
                            r_3, g_3, b_3 = image_rgb.getpixel((x+1, y+1))
                            r_4, g_4, b_4 = image_rgb.getpixel((x+1, y-1))
                            r_5, g_5, b_5 = image_rgb.getpixel((x, y+1))
                            r_6, g_6, b_6 = image_rgb.getpixel((x, y-1))
                            r_7, g_7, b_7 = image_rgb.getpixel((x-1, y-1))
                            r_8, g_8, b_8 = image_rgb.getpixel((x-1, y+1))
                            counter = 0
                            if r_1 > 200 and g_1 > 82 and b_1 > 120:
                                counter += 1
                            if r_2 > 200 and g_2 > 82 and b_2 > 120:
                                counter += 1
                            if r_3 > 200 and g_3 > 82 and b_3 > 120:
                                counter += 1
                            if r_4 > 200 and g_4 > 82 and b_4 > 120:
                                counter += 1
                            if r_5 > 200 and g_5 > 82 and b_5 > 120:
                                counter += 1
                            if r_6 > 200 and g_6 > 82 and b_6 > 120:
                                counter += 1
                            if r_7 > 200 and g_7 > 82 and b_7 > 120:
                                counter += 1
                            if r_8 > 200 and g_8 > 82 and b_8 > 120:
                                counter += 1
                        except:
                            counter = 0
                        if counter > 3:
                            # If top boundary is not set, set it
                            if top_boundary is None:
                                top_boundary = y
                            # Update bottom boundary on each iteration
                            bottom_boundary = y
            print("image processed ", filename)

            # Calculate diameter and center
            if top_boundary is not None and bottom_boundary is not None:
                diameter = bottom_boundary - top_boundary
                center_y = (top_boundary + bottom_boundary) // 2
                
                # Calculate distance from center to bottom of the image
                distance_to_bottom = height - center_y
                
                # Append diameter and distance to lists
                diameters.append(diameter)
                distances_to_bottom.append(distance_to_bottom)
            else:
                # If red circle not found, append None values
                diameters.append(None)
                distances_to_bottom.append(None)
    

    return diameters, distances_to_bottom

def convert_pxl_to_m(list, conv_factor):
    for index, item in enumerate(list):
        list[index] = item / conv_factor
    return True

def create_csv_file(filename, *columns):
    # Open the CSV file in write mode
    with open(filename, 'w', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)
        
        # Write the column headers
        headers = [column[0] for column in columns]
        csv_writer.writerow(headers)
        
        # Determine the number of rows based on the length of the lists
        num_rows = max(len(column[1]) for column in columns)
        
        # Iterate over the rows
        for i in range(num_rows):
            # Extract values from each list and write them as a row
            row = [column[1][i] if i < len(column[1]) else None for column in columns]
            csv_writer.writerow(row)

def an_average(df, quantity_col, x):
    # Check if provided columns exist in the dataframe
    if quantity_col not in df.columns:
        raise KeyError("Quantity column or Error column not found in the DataFrame.")
    
    # Delete all columns except quantity_col and error_col
    df = df[[quantity_col]]
    
    # Initialize variables
    error_col = 'err_'+quantity_col
    result_df = pd.DataFrame(columns=[quantity_col, error_col])
    num_rows = len(df)
    start_index = 0
    
    # Process dataframe in chunks of size x
    while start_index < num_rows:
        end_index = min(start_index + x, num_rows)
        
        # Calculate average for quantity column
        avg_quantity = df.iloc[start_index:end_index][quantity_col].mean()
        
        # Calculate error using root mean square
        error_values = df.iloc[start_index:end_index][quantity_col]                
        minimum_value = error_values.min()


        rms_error = avg_quantity - minimum_value 
        
        # Append result to result_df
        result_df = pd.concat([result_df, pd.DataFrame({quantity_col: [avg_quantity], error_col: [rms_error]})], ignore_index=True)
        
        # Move to next chunk
        start_index += x
    
    return result_df

def average(df, quantity_col, error_col, x):
    # Check if provided columns exist in the dataframe
    if quantity_col not in df.columns or error_col not in df.columns:
        raise KeyError("Quantity column or Error column not found in the DataFrame.")
    
    # Delete all columns except quantity_col and error_col
    df = df[[quantity_col, error_col]]
    
    # Initialize variables
    result_df = pd.DataFrame(columns=[quantity_col, error_col])
    num_rows = len(df)
    start_index = 0
    
    # Process dataframe in chunks of size x
    while start_index < num_rows:
        end_index = min(start_index + x, num_rows)
        
        # Calculate average for quantity column
        avg_quantity = df.iloc[start_index:end_index][quantity_col].mean()
        
        # Calculate error using root mean square
        error_values = df.iloc[start_index:end_index][quantity_col] - avg_quantity
        
        rms_error = np.sqrt(np.mean(error_values ** 2)) / x
        
        # Append result to result_df
        result_df = pd.concat([result_df, pd.DataFrame({quantity_col: [avg_quantity], error_col: [rms_error]})], ignore_index=True)
        
        # Move to next chunk
        start_index += x
    
    return result_df

def another_average(df, quantity_col, nil, x):
    # Delete all columns except the quantity column
    df = df[[quantity_col]]
    
    result_df = pd.DataFrame(columns=[quantity_col, 'err_' + quantity_col])
    num_rows = len(df)
    start_index = 0
    
    # Process dataframe in chunks of size x
    while start_index < num_rows:
        end_index = min(start_index + x, num_rows)
        
        # Calculate average for quantity column
        avg_quantity = df.iloc[start_index:end_index][quantity_col].mean()
        
        # Calculate standard deviation
        std_dev = df.iloc[start_index:end_index][quantity_col].std()
        
        # Append result to result_df
        result_df = pd.concat([result_df, pd.DataFrame({quantity_col: [avg_quantity], 'err_' + quantity_col: [std_dev]})], ignore_index=True)
        
        # Move to next chunk
        start_index += x
    
    return result_df