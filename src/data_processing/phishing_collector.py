# This class is responsible for collecting phishing URLs.

import requests
import logging

class PhishingCollector:
    def __init__(self, phishing_url):
        self.phishing_url = phishing_url

    def collect_urls(self):
        # Logic to collect phishing URLs
        response = requests.get(self.phishing_url)
        if response.status_code == 200:
            # Process and return the list of URLs
            return response.text.splitlines()
        else:
            print(f"Failed to retrieve phishing URLs. Status code: {response.status_code}")
            return []

    def save_urls(self, urls, filename):
        directory = 'data/raw'  # Adjust the path to your 'data/raw' directory
        filepath = f'{directory}/{filename}'
        try:
            with open(filepath, 'w') as file:
                for url in urls:
                    file.write(url + '\n')
            logging.info(f'Saved URLs to {filepath}')
        except Exception as e:
            logging.error(f'Failed to save URLs to {filepath}: {e}')

