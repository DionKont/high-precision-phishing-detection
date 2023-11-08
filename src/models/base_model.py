import logging
import pandas as pd
from sklearn.model_selection import train_test_split

# Configure logging for the model
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BaseModel:
    """
    A base class for all models that defines the common interface and includes logging.
    """

    def __init__(self, model_name):
        self.model = None
        self.model_name = model_name
        logger.info(f"{self.model_name} instance is created.")

    def load_data(self, data_path='data/processed/processed_data.h5'):
        """
        Load the processed data from the specified path.
        """
        try:
            data = pd.read_hdf(data_path, 'data')
            logger.info(f"Data loaded from {data_path}")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise e

    def create_train_test_split(self, data, test_size=0.2, random_state=42):
        # Assume the last column is the target labeled 'label'
        X = data.iloc[:, :-1]  # all columns except the last
        y = data.iloc[:, -1]   # the last column

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        return X_train, X_test, y_train, y_test
