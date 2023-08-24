import re
import pandas as pd

# Function to process the .RAD file content and return a DataFrame
def process_rad_file(file_path):
    # Extracting year from the file name
    year_from_file = re.search(r"(\d{2})", file_path).group(1)
    
    # Reading the contents of the file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Processing each line and extracting required data
    all_data = []
    for line in lines:
        # Extracting date
        date_match = re.match(r":(\d{2}/\d{2})", line)
        date_with_year = f"{date_match.group(1)}/{year_from_file}" if date_match else None
        
        # Extracting values
        values_part = re.split(r"\)", line)[-1].strip()
        values_found = re.findall(r"(\d+| {5})", values_part)
        values_processed = [val if val != "     " else "" for val in values_found]
        
        # Appending the data to all_data list
        hour_index = 0
        for value in values_processed:
            time_stamp = f"{date_with_year} {hour_index:02d}:00"
            all_data.append([time_stamp, value])
            hour_index += 1

    # Creating a DataFrame from the extracted data
    df = pd.DataFrame(all_data, columns=["Timestamp", "Value"])
    return df

# Example usage
file_path = "ARTK21.RAD"
df_processed = process_rad_file(file_path)
csv_path = "processed_data_with_year.csv"
df_processed.to_csv(csv_path, index=False)
