import pandas as pd
from category_encoders import BinaryEncoder

class FeatureEngineer:
    def __init__(self, data):
        self.data = data
        self.binary_encoder = BinaryEncoder(cols=['server_header', 'domain'], drop_invariant=True)

    def encode_features(self):
        # Apply binary encoding
        self.data = self.binary_encoder.fit_transform(self.data)
        return self.data

    def get_encoded_data(self):
        return self.data

    def get_feature_names(self):
        # This will return the new feature names after binary encoding
        return self.data.columns.tolist()
