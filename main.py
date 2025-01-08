# Import necessary modules
import os
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup

# Data Functions
# Function to load previously sampled species from the file
def load_sampled_spp(sampled_spp_file, possible_spp_file):
    with open(sampled_spp_file, "r") as file:
        sampled_spp = {int(line.strip()) for line in file}
    with open(possible_spp_file, "r") as file:
        possible_spp = {int(line.strip()) for line in file}
    remaining_spp = possible_spp - sampled_spp
    return sampled_spp, remaining_spp

# Function to select a new unique species
def unique_random_spp(remaining_spp, sampled_spp_file, number_file):
    # Generate a species that isn't in sampled_spp
    random_sp = random.choice(list(remaining_spp))
    with open(number_file, "r") as file:
        number = int(file.read().strip())
        number = number + 1

    # Add the new species to possible_spp file
    with open(sampled_spp_file, "a") as file:
        file.write(f"{random_sp}\n")

    # Track species number
    with open(number_file, "w") as file:
        file.write(f"{number}\n")
    return random_sp, number

# Define filenames for funtions sampling
sampled_spp_file = "bsky_fauna_bot/sampled_spp.txt"
possible_spp_file = "bsky_fauna_bot/possible_spp.txt"
number_file = "bsky_fauna_bot/iteration_number.txt"

# Retrieve sampled and remaining spp IDs
sampled_spp, remaining_spp = load_sampled_spp(sampled_spp_file, possible_spp_file)

# Sample Unique Species
random_sp, number = unique_random_spp(remaining_spp, sampled_spp_file, number_file)

# Read the tab-delimited file into a DataFrame
df = pd.read_csv('bsky_fauna_bot/amphib_names.txt', sep='\t')

# Retriece the information for the selected species
sp_name = df.iloc[random_sp].loc['genus'] + " " + df.iloc[random_sp].loc['species']
web_id = df.iloc[random_sp].loc['uri/guid']
iucn_status = df.iloc[random_sp].loc['iucn']
common_name = df.iloc[random_sp].loc['common_name']

# Structure the Post text
post = f"#{number} Today species, {sp_name}, commonly called {common_name} is considered {iucn_status} by IUCN. "


# Dowload Imagee

# Send an HTTP GET request to the URL
response = requests.get(web_id)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the <img> tag
    img_tag = soup.find("img", alt=sp_name)
    if img_tag:
        # Extract the src attribute from the <img> tag
        img_src = img_tag['src']
        print(f"Image Source URL: {img_src}")
        img_data = requests.get(img_src).content
        with open('today_sp.jpg', 'wb') as handler:
            handler.write(img_data)

    else:
        print("No <img> tag with 'src' found inside the <a> tag.")

else:
    print(f"Failed to access the webpage. Status code: {response.status_code}")
