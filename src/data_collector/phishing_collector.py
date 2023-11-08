# This class is responsible for collecting phishing URLs.

import requests
import logging
import os

class PhishingCollector:
    def __init__(self, phishing_url):
        self.phishing_url = phishing_url

    def collect_urls(self):
        # Logic to collect phishing URLs
        response = requests.get(self.phishing_url)
        if response.status_code == 200:
            # Process and return the list of URLs with label
            urls = response.text.splitlines()
            labeled_urls = [(url, 1) for url in urls]  # 1 indicates phishing
            return labeled_urls
        else:
            print(f"Failed to retrieve phishing URLs. Status code: {response.status_code}")
            return []

    def save_urls(self, labeled_urls, filename):
        directory = 'data/raw'
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'w') as file:
                for url, label in labeled_urls:
                    file.write(f"{url},{label}\n")  # Save as comma-separated values
            logging.info(f'Saved labeled URLs to {filepath}')
        except Exception as e:
            logging.error(f'Failed to save labeled URLs to {filepath}: {e}')

