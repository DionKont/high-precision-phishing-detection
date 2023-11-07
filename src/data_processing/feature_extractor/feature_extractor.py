# feature_extractor.py

import json
import logging
from url_feature_extractor import extract_url_features  # Assuming this is a standalone function now
from html_content_feature_extractor import HTMLContentFeatureExtractor

class FeatureExtractor:
    """
    Main class for orchestrating feature extraction.
    """
    def __init__(self, phishing_urls_file, legitimate_urls_file):
        self.phishing_urls_file = phishing_urls_file
        self.legitimate_urls_file = legitimate_urls_file

    def read_urls_from_file(self, file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]

    def save_features_to_json(self, features, file_path):
        with open(file_path, 'w') as file:
            json.dump(features, file, indent=4)

    def run(self):
        # Read the collected URLs from files
        phishing_urls = self.read_urls_from_file(self.phishing_urls_file)
        legitimate_urls = self.read_urls_from_file(self.legitimate_urls_file)

        # Combine the URLs
        all_urls = phishing_urls + legitimate_urls

        # Extract features using the specific feature extractor
        features = []
        for url in all_urls:
            url_features = extract_url_features(url)
            html_features = HTMLContentFeatureExtractor.extract_html_features(url)
            combined_features = {**url_features, **html_features}
            features.append(combined_features)
        # Save features to JSON
        self.save_features_to_json(features, 'data/processed/features.json')

        logging.info("Features extracted and saved successfully.")

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Paths to the saved data files
    phishing_urls_file = 'data/raw/phishing_urls.txt'
    legitimate_urls_file = 'data/raw/legitimate_urls.txt'

    # Initialize the main feature extractor
    extractor = FeatureExtractor(phishing_urls_file, legitimate_urls_file)

    # Run the feature extraction process
    extractor.run()

if __name__ == "__main__":
    main()
