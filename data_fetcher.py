"""
main.py

This script samples a species from a list of amphibians and retrieves information from the AmphibiaWeb website.

Functions:
    load_sampled_spp(sampled_spp_file, possible_spp_file):
        Loads previously sampled species from a file and returns the sampled and remaining species.

    unique_random_spp(remaining_spp, sampled_spp_file, number_file):
        Selects a new unique species that hasn't been sampled before, updates the sampled species file, and tracks the species number.

Variables:
    sampled_spp_file (str): Path to the file containing sampled species IDs.
    possible_spp_file (str): Path to the file containing possible species IDs.
    number_file (str): Path to the file containing the iteration number.
    df (DataFrame): DataFrame containing amphibian species information.

Execution:
    The script attempts to sample a unique species up to a maximum number of attempts. For each attempt, it retrieves the species information,
    structures a post text, and downloads an image of the species from the AmphibiaWeb website.
    If the image is successfully downloaded, the process stops; otherwise, it retries with a new species.
"""

# Import necessary modules
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree

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

    # Add the new species to possible_spp file
    with open(sampled_spp_file, "a") as file:
        file.write(f"{random_sp}\n")

    # Track species number
    with open(number_file, "r") as file:
        number = int(file.read().strip())
        number = number + 1
    with open(number_file, "w") as file:
        file.write(f"{number}\n")
    return random_sp, number

# Define filenames for funtions sampling
sampled_spp_file = "resources/sampled_spp.txt"
possible_spp_file = "resources/possible_spp.txt"
number_file = "resources/iteration_number.txt"

# Read the tab-delimited file into a DataFrame
df = pd.read_csv('resources/amphib_names.txt', sep='\t')

# Set the maximum number of attempts to sample a species
attempts = 0
max_attempts = 10

while attempts < max_attempts:
    check = 1
    attempts = attempts + 1
    print(f"Attempt {attempts}")
    # Retrieve sampled and remaining spp IDs
    sampled_spp, remaining_spp = load_sampled_spp(sampled_spp_file, possible_spp_file)

    # Sample Unique Species
    random_sp, number = unique_random_spp(remaining_spp, sampled_spp_file, number_file)

    # Retriece the information for the selected species
    sp_name = df.iloc[random_sp].loc['genus'] + " " + df.iloc[random_sp].loc['species']
    web_id = df.iloc[random_sp].loc['uri/guid']
    iucn_status = df.iloc[random_sp].loc['iucn']
    common_name = df.iloc[random_sp].loc['common_name']
    if len(common_name) > 45:
        common_name =  common_name[:40] + "..."
    print(f"species selected {random_sp} {sp_name}")

    # Dowload Image
    # Send an HTTP GET request to the URL
    response = requests.get(web_id)
    # Check for an Image
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the <img> tag
        img_tag = soup.find("img", alt = sp_name)
        if img_tag:
            # Extract the src attribute from the <img> tag
            img_src = img_tag['src']
            print(f"Image URL: {img_src}")
        else:
            print("No <img> tag with 'src' found inside the <a> tag.")
            check = 0
        
        # Get the calphotos image bank
        if check == 1:
            # Send an HTTP GET request for the next URL
            # XPath to locate the href tag
            tree = etree.HTML(str(soup))
            xpath_expression = f'//img[@alt="{sp_name}"]/parent::a'
            a_tag = tree.xpath(xpath_expression)

            # Extract the href attribute
            if a_tag and 'href' in a_tag[0].attrib:
                href = a_tag[0].attrib['href']
                print(f"Step 1: URL {href}")
            else:
                check = 0
                print("Step 1: No matching <a> tag found.")
            
            if check == 1:
                response = requests.get(href)
                if response.status_code == 200:
                    # Parse the HTML content again
                    soup = BeautifulSoup(response.text, "html.parser")
                    tree = etree.HTML(str(soup))

                    # XPath to locate the href tag in High Resolution
                    xpath_expression = f'//img[@alt="{sp_name}"]/parent::a'
                    a_tag = tree.xpath(xpath_expression)

                    # Extract the href attribute
                    if a_tag and 'href' in a_tag[0].attrib:
                        href2 = a_tag[0].attrib['href']
                        print(f"Step 2: URL https://calphotos.berkeley.edu/{href2}")
                    else:
                        check = 0
                        print("Step 2: No matching <a> tag found.")
                    
                    if check == 1:
                        response = requests.get(f"https://calphotos.berkeley.edu/{href2}")
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.text, "html.parser")
                            # Find the <img> tag
                            img_tag = soup.find("img", alt = sp_name)
                            if img_tag:
                                # Extract the src attribute from the <img> tag
                                img_src = img_tag['src']
                                # Send an HTTP GET request for the image URL
                                img_data = requests.get(f"https://calphotos.berkeley.edu/{img_src}").content
                                with open('resources/today_sp.jpg', 'wb') as handler:
                                    handler.write(img_data)
                                print(f"Final Image downloaded successfully: https://calphotos.berkeley.edu/{img_src}")
                                # Parse the HTML using etree
                                tree = etree.HTML(str(soup))
                                # XPath to locate the <td> containing the copyright info
                                xpath_expression = '//td[contains(text(), "©")]'
                                # Locate the <td> tag
                                copyright_tag = tree.xpath(xpath_expression)
                                copyright_text = copyright_tag[0].text.strip()
                                print(f"Copyright: {copyright_text}")
                            else:
                                print("No <img> tag with 'src' found inside the <a> tag.")
                                check = 0
    else:
        print(f"Failed to access the webpage. Status code: {response.status_code}")
        check = 0
        
    if check == 1:
        # Structure the Post text
        if isinstance(iucn_status, str):
            if isinstance(common_name, str):
                post = f"#{number} Today species {sp_name}, commonly called {common_name}, is considered {iucn_status} by IUCN. For more, check {web_id} Copyright:{copyright_text}"
            else:
                post = f"#{number} Today species {sp_name} is considered {iucn_status} by IUCN. For more, check {web_id} Copyright:{copyright_text}"
        else:
            if isinstance(common_name, str):
                post = f"#{number} Today species {sp_name}, commonly called {common_name}, is considered {iucn_status} by IUCN. For more, check {web_id} Copyright:{copyright_text}"
            else:
                post = f"#{number} Today species {sp_name} is currently not evaluated by IUCN. For more, check {web_id} Copyright:{copyright_text}"
        with open("resources/today_text.txt", "w") as file:
                file.write(f"{post}\n")
        break

    else: 
        print("trying a new species")

    

if attempts == max_attempts:
    print("Maximum attempts reached. Exiting.")