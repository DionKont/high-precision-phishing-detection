import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, accuracy_score, classification_report
from base_model import BaseModel

logger = logging.getLogger('RandomForestModel')

class RandomForestModel(BaseModel):
    def __init__(self, n_estimators=100, random_state=42, model_name='RandomForest'):
        super().__init__(model_name)
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.model = RandomForestClassifier(n_estimators=self.n_estimators, random_state=self.random_state)
        logger.info(f"{self.model_name} model initialized with {self.n_estimators} estimators.")

    def fit(self, X_train, y_train):
        """
        Fit the RandomForest model on the training data.
        """
        self.model.fit(X_train, y_train)
        logger.info(f"{self.model_name} model trained.")

    def predict(self, X_test):
        """
        Make predictions on the test data using the trained RandomForest model.
        """
        return self.model.predict(X_test)

    def evaluate(self, X_test, y_test):
        """
        Evaluate the model on the test data and print out the classification report,
        including precision and accuracy.
        """
        predictions = self.predict(X_test)
        precision = precision_score(y_test, predictions)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)
        logger.info(f"Evaluation results for {self.model_name}:\nPrecision: {precision}\nAccuracy: {accuracy}\n{report}")
        return precision, accuracy, report

# Usage example:
if __name__ == "__main__":
    # Initialize the RandomForestModel
    rf_model = RandomForestModel()

    # Load the preprocessed data
    data = rf_model.load_data()

    # Create the train/test split
    X_train, X_test, y_train, y_test = rf_model.create_train_test_split(data)

    # Fit the model
    rf_model.fit(X_train, y_train)

    # Evaluate the model
    precision, accuracy, report = rf_model.evaluate(X_test, y_test)
    print(f"Precision: {precision}\nAccuracy: {accuracy}\n")
    print(report)
