#!/usr/bin/env python3
#
# Script to extract customers of a specific provider ASN from radar.qrator.net
# It retrieves clients that have only the specified provider as their active provider
# and have at least one active IPv4 prefix.
#
# Requirements:
# - selenium
# - webdriver-manager
#
# Install dependencies with:
# pip install selenium webdriver-manager
#

import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Output CSV file
output_file = 'output.txt'

# Provider ASN to analyze
provider_asn = '28260'

# Configure Chrome in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Headless mode

# Initialize the driver with ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Data to be written to the CSV
output_data = {}

# Open the initial page
url = f'https://radar.qrator.net/as/{provider_asn}/connectivity/neighbors/customers?page-size=100&p=1'
driver.get(url)

# Wait for the page to load
time.sleep(10)

# Extract ASN numbers from the initial page
asn_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/as/")]')

# Extract ASNs and build the list of client ASNs
asn_list = [asn.text.replace("AS", "").strip() for asn in asn_elements]

# Iterate over the client ASNs
for client_asn in asn_list:
    print(f'🔹 Processing client ASN {client_asn}...')
    
    # Build the URL for each client's providers
    customer_url = f'https://radar.qrator.net/as/{client_asn}/connectivity/neighbors/providers'
    driver.get(customer_url)

    time.sleep(10)
    
    try:
        # Check if the client has only one active provider and it's the specified provider ASN
        rows = driver.find_elements(By.XPATH, '//tr[not(contains(@class, "MuiTableRow-head"))]')

        active_providers = []
        active_names = []
        for row in rows:
            active_icon = row.find_element(By.XPATH, './/td[5]')
            active_icon_html = active_icon.get_attribute("outerHTML")

            # Check if the active_icon contains "CheckCircleIcon"
            # CheckCircleIcon is the class name for the green checkmark icon
            if active_icon_html and "CheckCircleIcon" in active_icon_html:
                provider_as_number = row.find_element(By.XPATH, './/td[1]/a').text.strip().replace("AS", "")
                provider_name = row.find_element(By.XPATH, './/td[2]').text.strip()
                active_providers.append(provider_as_number)
                active_names.append(provider_name)

        # Verify if the client has only one active provider and it is the specified provider ASN
        if len(active_providers) == 1 and active_providers[0] == provider_asn:
            as_number = active_providers[0]
            as_name = active_names[0]
            print(f'\t✅ Client {client_asn} has only provider AS{provider_asn}')
            
            # Fetch the client's active IPv4 prefixes
            prefixes_url = f'https://radar.qrator.net/as/{client_asn}/connectivity/prefixes?ip=4&p=1'
            print(f'\tFetching prefixes from: {prefixes_url}')
            driver.get(prefixes_url)
            time.sleep(10)

            rows = driver.find_elements(By.XPATH, '//tbody/tr')

            prefixes = []
            for row in rows:
                try:
                    active_icon = row.find_element(By.XPATH, './/td[7]')
                    active_icon_html = active_icon.get_attribute("outerHTML")

                    if active_icon_html and "CheckCircleIcon" in active_icon_html:
                        prefix = row.find_element(By.XPATH, './/td[1]').text.strip()
                        prefixes.append(prefix)
                        print(f'\t➕ Active IPv4 Prefix: {prefix}')
                except:
                    pass

            # Only add clients with at least one active IPv4 prefix
            if prefixes:
                output_data[client_asn] = {
                    'asn_number': client_asn,
                    'asn_name': as_name,
                    'customer_url': customer_url,
                    'prefixes': prefixes
                }
            else:
                print(f'\t❌ Client {client_asn} has no active IPv4 prefixes')

            print('')
        else:
            print(f'\t❌ Client {client_asn} does not meet criteria\n')

    except Exception as e:
        print(f"\t❌ Error processing ASN {client_asn}: {e}\n")

# Write the data to the CSV file
with open(output_file, mode='w', encoding='utf-8') as file:
    for client_asn, data in output_data.items():
        file.write(f"ASN Name: {data['asn_name']}\n")
        file.write(f"ASN Number: {data['asn_number']}\n")
        file.write("IPv4 Prefixes:\n")
        for prefix in data['prefixes']:
            file.write(f"{prefix}\n")
        file.write("\n")


# Close the browser
driver.quit()
