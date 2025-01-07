# Import necessary modules
import os
from dotenv import load_dotenv
import pandas as pd
import random
# Import atproto
from atproto import Client

# Function to load previously sampled species from the file
def load_sampled_spp(sampled_spp_file, possible_spp_file):
    with open(sampled_spp_file, "r") as file:
        sampled_spp = {int(line.strip()) for line in file}
    with open(possible_spp_file, "r") as file:
        possible_spp = {int(line.strip()) for line in file}
    remaining_spp = possible_spp - sampled_spp
    return sampled_spp, remaining_spp

# Function to select a new unique species
def unique_random_spp(remaining_spp, sampled_spp_file):
    # Generate a species that isn't in sampled_spp
    random_sp = random.choice(list(remaining_spp))

    # Add the new species to possible_spp file
    with open(sampled_spp_file, "a") as file:
        file.write(f"{random_sp}\n")
    return random_sp


# Define filenames for funtions sampling
sampled_spp_file = "bsky_fauna_bot/sampled_spp.txt"
possible_spp_file = "bsky_fauna_bot/possible_spp.txt"

# Retrieve sampled and remaining spp IDs
sampled_spp, remaining_spp = load_sampled_spp(sampled_spp_file, possible_spp_file)

# Sample Unique Species
random_sp = unique_random_spp(remaining_spp, sampled_spp_file)

# Read the tab-delimited file into a DataFrame
df = pd.read_csv('bsky_fauna_bot/amphib_names.txt', sep='\t')

# Retriece the information for the selected species
sp_name = (df.iloc[random_sp])

# Load the .env file and get the login for API
load_dotenv()
BLUESKY_USER = os.getenv("BLUESKY_USER")
BLUESKY_PASS = os.getenv("BLUESKY_PASS")

# Connect to Bluesky
bs_client = Client()
profile = bs_client.login(BLUESKY_USER, BLUESKY_PASS)
response = bs_client.send_post("Posting this from atproto! New project to come in 2025...")
print(response)
