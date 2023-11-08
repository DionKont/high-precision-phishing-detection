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
            return [line.strip().split(',') for line in file]  # Split each line by comma to separate URL and label

    def save_features_to_json(self, features, file_path):
        with open(file_path, 'w') as file:
            json.dump(features, file, indent=4)

    def run(self):
        # Read the collected URLs and labels from files
        phishing_data = self.read_urls_from_file(self.phishing_urls_file)
        legitimate_data = self.read_urls_from_file(self.legitimate_urls_file)

        # Combine the URLs and labels
        all_data = phishing_data + legitimate_data

        # Extract features using the specific feature extractor
        features = []
        for url_data in all_data:  # url_data is a list containing [url, label]
            url = url_data[0]  # The URL is the first element
            label = url_data[1] if len(
                url_data) > 1 else '0'  # The label is the second element, default to '0' if missing
            url_features = extract_url_features(url)
            html_features = HTMLContentFeatureExtractor.extract_html_features(url)

            # Check if response_time is -1 and skip this datapoint if so
            if html_features['response_time'] != -1:
                combined_features = {**url_features, **html_features,
                                     'label': int(label)}  # Add the label to the features
                features.append(combined_features)
            else:
                logging.info(f"Skipping URL due to failed response: {url}")

        # Save features to JSON
        self.save_features_to_json(features, 'data/raw/features.json')

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
