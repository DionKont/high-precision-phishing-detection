import logging
from sklearn.ensemble import RandomForestClassifier
from base_model import BaseModel
import pandas as pd
logger = logging.getLogger('RandomForestModel')
import numpy as np
import matplotlib.pyplot as plt
import os

class RandomForestModel(BaseModel):
    def __init__(self, n_estimators=100, random_state=10, model_name='RandomForest'):
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
        self.log_feature_importance(X_train.columns)

    def log_feature_importance(self, feature_names):
        """
        Log the feature importances of the model.
        """
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]

        # Log the feature importances
        logger.info("Feature importances:")
        for f in range(len(feature_names)):
            logger.info(f"{f + 1}. feature {feature_names[indices[f]]} ({importances[indices[f]]})")

        # Optionally, you can also plot the feature importances
        plt.figure()
        plt.title("Feature Importances")
        plt.bar(range(len(feature_names)), importances[indices], color="r", align="center")
        plt.xticks(range(len(feature_names)), feature_names[indices], rotation=90)
        plt.xlim([-1, len(feature_names)])
        plt.tight_layout()  # Adjust the plot to ensure labels are visible

        # Save the plot in the graphs folder
        graphs_folder = 'data/graphs'
        if not os.path.exists(graphs_folder):
            os.makedirs(graphs_folder)
        plt.savefig(os.path.join(graphs_folder, 'feature_importances.png'))
        plt.close()

    def predict(self, X_test):
        """
        Make predictions on the test data using the trained RandomForest model.
        """
        return self.model.predict(X_test)

    def run(self):
        # Load the preprocessed data
        data = self.load_data()

        # Create the train/validation/test split
        X_train, X_val, X_test, y_train, y_val, y_test = self.create_train_test_split(data)

        # Perform k-fold cross-validation
        cv_score = self.cross_validate(pd.concat([X_train, X_val], axis=0), cv=5)

        # Fit the model on the training data
        self.fit(X_train, y_train)

        # Plot the learning curves
        self.plot_learning_curves(X_train, y_train, X_val, y_val)

        # Evaluate the model on the validation set
        val_precision, val_accuracy, val_report = self.evaluate(X_val, y_val)
        logger.info(f"Validation Precision: {val_precision}\nValidation Accuracy: {val_accuracy}\n")
        logger.info(f'Validation report below:\n{val_report}')

        # Evaluate the model on the test set
        test_precision, test_accuracy, test_report = self.evaluate(X_test, y_test)
        logger.info(f"Test Precision: {test_precision}\nTest Accuracy: {test_accuracy}\n")
        logger.info(f'Test report below:\n{test_report}')

        return cv_score, val_precision, val_accuracy, test_precision, test_accuracy



# This would be outside the class, in the same file
if __name__ == "__main__":
    # Initialize the RandomForestModel
    rf_model = RandomForestModel()

    # Run the model process
    results = rf_model.run()
    print(f"Cross-validation Score: {results[0]}")
    print(f"Validation Precision: {results[1]}, Validation Accuracy: {results[2]}")
    print(f"Test Precision: {results[3]}, Test Accuracy: {results[4]}")
