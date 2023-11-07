# html_content_feature_extractor.py

import requests
from bs4 import BeautifulSoup
import re
import time

class HTMLContentFeatureExtractor:
    @staticmethod
    def extract_html_features(url):
        features = {}
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            elapsed_time = time.time() - start_time

            soup = BeautifulSoup(response.content, 'html.parser')

            # Count the number of scripts
            features['script_count'] = len(soup.find_all('script'))

            # Count the number of hidden elements
            features['hidden_elements_count'] = len(soup.find_all(style=re.compile('display:\s*none')))

            # Presence of suspicious scripts
            features['suspicious_scripts_count'] = len([script for script in soup.find_all('script') if 'eval' in script.text or 'escape' in script.text])

            # Response Time
            features['response_time'] = elapsed_time

            # Server Headers
            features['server_header'] = response.headers.get('Server', 'Unknown')

            # Add more feature extractions as needed

        except requests.RequestException as e:
            # Handle any requests exceptions
            print(f"Error fetching {url}: {str(e)}")
        except Exception as e:
            # Handle any other exceptions
            print(f"An unexpected error occurred: {str(e)}")

        return features
