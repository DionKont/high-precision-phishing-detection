import os
import logging
import pandas as pd
from data_cleaner import DataCleaner
from feature_engineer import FeatureEngineer
class DataPreprocessor:
    def __init__(self, input_filepath, output_folder='data/processed'):
        self.input_filepath = input_filepath
        self.output_folder = output_folder
        self.setup_logging()

    def setup_logging(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('data_preprocessor.log')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def preprocess(self):
        try:
            # Load data
            data = pd.read_json(self.input_filepath)
            # Clean data
            cleaner = DataCleaner(data)
            data = cleaner.clean()
            # Engineer features
            engineer = FeatureEngineer(data)
            data = engineer.encode_features()
            # Balance the dataset
            data = self.balance_classes(data)
            # Save processed data
            self.save_processed_data(data)
        except Exception as e:
            self.logger.error(f"Error during preprocessing: {e}", exc_info=True)

    def save_processed_data(self, data):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        # Save as HDF5
        hdf5_output_path = os.path.join(self.output_folder, 'processed_data.h5')
        data.to_hdf(hdf5_output_path, key='data', mode='w')
        self.logger.info(f"Processed data saved to {hdf5_output_path}")

        # Save as CSV
        csv_output_path = os.path.join(self.output_folder, 'processed_data.csv')
        data.to_csv(csv_output_path, index=False)
        self.logger.info(f"Processed data saved to {csv_output_path}")

    def balance_classes(self, data):
        # Separate majority and minority classes
        data_minority = data[data.label == 1]
        data_majority = data[data.label == 0]

        # Find the number of instances in the smaller class
        minority_class_len = len(data_minority)
        majority_class_len = len(data_majority)

        # Use the smaller number to sample from the larger class
        balanced_majority_class = data_majority.sample(minority_class_len)

        # Concatenate the minority class with the downsampled majority class
        data_balanced = pd.concat([data_minority, balanced_majority_class])

        # Shuffle the dataset to prevent the model from learning any order
        data_balanced = data_balanced.sample(frac=1).reset_index(drop=True)

        self.logger.info(f"Balanced dataset with {len(data_balanced)} instances per class.")

        return data_balanced

if __name__ == "__main__":
    input_file = 'data/raw/features.json'  # Replace with your actual input file path
    preprocessor = DataPreprocessor(input_file)
    preprocessor.preprocess()
