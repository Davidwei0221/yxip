import requests
from bs4 import BeautifulSoup
import re
import os

# A set to store unique IP addresses to avoid duplicates.
unique_ips = set()

# The list of URLs to scrape for IP addresses.
# Notes on URLs:
# - 'https://stock.hostmonit.com/CloudFlareYes' is excluded because it requires JavaScript to render.
urls = [
    'https://ip.164746.xyz',                     # Provides IPs in an HTML table
    'https://api.uouin.com/cloudflare.html',    # Provides IPs in an HTML table
    'https://cf.090227.xyz',                     # Provides IPs in plain text
    'https://cf.vvhan.com/'                      # Provides IPs in plain text, requires a common User-Agent
]

# Regular expression to find IPv4 addresses.
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# Set a common user-agent to avoid being blocked by some sites.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Loop through each URL to fetch and parse IP addresses.
for url in urls:
    try:
        print(f"Fetching IPs from {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        # Raise an exception for bad status codes (4xx or 5xx).
        response.raise_for_status()

        # For plain text responses, we can find all IPs directly.
        if url in ['https://cf.090227.xyz', 'https://cf.vvhan.com/']:
            ip_matches = re.findall(ip_pattern, response.text)
            for ip in ip_matches:
                unique_ips.add(ip)
        # For HTML responses, we parse the table rows.
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            # The relevant IPs are in table rows for the HTML sites.
            elements = soup.find_all('tr')
            for element in elements:
                element_text = element.get_text()
                ip_matches = re.findall(ip_pattern, element_text)
                for ip in ip_matches:
                    unique_ips.add(ip)

    except requests.exceptions.RequestException as e:
        print(f"Could not fetch or read URL {url}. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while processing {url}. Error: {e}")

# Write the collected unique IP addresses to ip.txt.
# The file is opened in 'w' mode, so it's cleared on every run.
try:
    with open('ip.txt', 'w') as file:
        for ip in sorted(list(unique_ips)): # Sorting for consistent output
            file.write(ip + '\n')
    print(f"\nSuccessfully saved {len(unique_ips)} unique IP addresses to ip.txt.")
except IOError as e:
    print(f"Error writing to file ip.txt. Error: {e}")
