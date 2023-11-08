import pandas as pd

class DataCleaner:
    def __init__(self, data):
        self.data = pd.DataFrame(data)

    def remove_duplicates(self):
        self.data.drop_duplicates(inplace=True)

    def handle_missing_values(self):
        numeric_cols = self.data.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            self.data[col].fillna(self.data[col].median(), inplace=True)

    def correct_formats(self):
        if 'server_header' in self.data.columns:
            self.data['server_header'] = self.data['server_header'].str.lower()

    def clean(self):
        self.remove_duplicates()
        self.handle_missing_values()
        self.correct_formats()
        return self.data
