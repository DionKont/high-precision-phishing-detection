import requests
import zipfile
import os
import logging

class LegitimateCollector:
    def __init__(self, legitimate_url, limit= None):
        self.legitimate_url = legitimate_url
        self.limit = limit
    def collect_urls(self):
        # Logic to collect legitimate URLs
        try:
            response = requests.get(self.legitimate_url, stream=True)
            response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code

            # Save the zip file locally
            zip_path = 'data/raw/top-1m.csv.zip'
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall('data/raw')

            # Read the extracted CSV file
            csv_path = os.path.join('data/raw', 'top-1m.csv')
            urls = []
            with open(csv_path, 'r') as file:
                for i, line in enumerate(file):
                    if self.limit is not None and i >= self.limit:
                        break  # Stop reading if the limit is reached
                    domain = line.strip().split(',')[1]
                    # Ensure each URL starts with 'https://'
                    url = f'https://{domain}' if not domain.startswith('http://') and not domain.startswith(
                        'https://') else domain
                    urls.append(url)

            # Clean up the zip file and the extracted CSV
            os.remove(zip_path)
            os.remove(csv_path)

            return urls

        except requests.exceptions.HTTPError as errh:
            logging.error(f"Http Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            logging.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            logging.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            logging.error(f"Oops: Something Else: {err}")
        except zipfile.BadZipFile as errz:
            logging.error(f"Bad Zip File: {errz}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        return []

    def save_urls(self, urls, filename):
        directory = 'data/raw'
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'w') as file:
                for url in urls:
                    file.write(url + '\n')
            logging.info(f'Saved URLs to {filepath}')
        except Exception as e:
            logging.error(f'Failed to save URLs to {filepath}: {e}')
