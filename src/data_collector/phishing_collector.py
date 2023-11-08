import requests
import logging
import os
import pandas as pd

class PhishingCollector:
    def __init__(self, phishing_url):
        self.phishing_url = phishing_url
        self.github_url = "https://github.com/ESDAUNG/PhishDataset/raw/main/data_bal%20-%2020000.xlsx"
        self.directory = 'data/raw'
        self.filename = 'phishing_urls.txt'
        self.filepath = os.path.join(self.directory, self.filename)

    def collect_urls(self):
        logging.info(f"Making GET request to {self.phishing_url}")
        response = requests.get(self.phishing_url)
        if response.status_code == 200:
            urls = response.text.splitlines()
            return urls
        else:
            logging.error(f"Failed to retrieve phishing URLs. Status code: {response.status_code}")
            return []

    def collect_github_urls(self):
        logging.info(f"Fetching phishing URLs from GitHub Excel file at {self.github_url}")
        try:
            # Ignore SSL certificate verification by setting verify=False
            response = requests.get(self.github_url, verify=False)
            if response.status_code == 200:
                # Write the content of the response to a temporary Excel file
                with open('temp_phishing_data.xlsx', 'wb') as file:
                    file.write(response.content)

                # Read the Excel file into a pandas DataFrame
                df = pd.read_excel('temp_phishing_data.xlsx')
                phishing_urls = df[df['Labels'] == 1]['URLs'].tolist()

                # Clean up the temporary file
                os.remove('temp_phishing_data.xlsx')

                return phishing_urls
            else:
                logging.error(f"Failed to retrieve phishing URLs from GitHub. Status code: {response.status_code}")
                return []
        except Exception as e:
            logging.error(f"Failed to retrieve phishing URLs from GitHub. Error: {e}")
            return []

    def save_urls(self, new_urls):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        existing_urls = set()
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                existing_urls.update(url.strip().split(',')[0] for url in file.readlines())

        new_unique_urls = [url for url in new_urls if url not in existing_urls]
        with open(self.filepath, 'a') as file:
            for url in new_unique_urls:
                file.write(f"{url},1\n")  # 1 indicates phishing
            logging.info(f'Appended {len(new_unique_urls)} new unique labeled URLs to {self.filepath}')

    def run(self):
        new_urls = self.collect_urls()
        self.save_urls(new_urls)
        github_urls = self.collect_github_urls()
        self.save_urls(github_urls)
