import logging
import pandas as pd
from abc import ABC, abstractmethod
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, learning_curve
from sklearn.metrics import precision_score, accuracy_score, classification_report, make_scorer, f1_score
import numpy as np
import matplotlib.pyplot as plt
import os
# Configure logging for the model
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BaseModel(ABC):
    """
    An abstract base class for all models that defines the common interface and includes logging.
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

    def create_train_test_split(self, data, test_size=0.3, random_state=19):
        """
        Split the data into training, validation, and testing sets.
        """
        # First, split the data into training and remaining data with test_size
        X = data.iloc[:, :-1]  # all columns except the last
        y = data.iloc[:, -1]  # the last column
        X_train, X_remaining, y_train, y_remaining = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        # Now split the remaining data equally into validation and test sets
        X_val, X_test, y_val, y_test = train_test_split(
            X_remaining, y_remaining, test_size=0.5, random_state=random_state
        )

        return X_train, X_val, X_test, y_train, y_val, y_test

    def cross_validate(self, data, cv=5):
        """
        Perform k-fold cross-validation.
        """
        X = data.iloc[:, :-1]  # all columns except the last
        y = data.iloc[:, -1]  # the last column
        kfold = StratifiedKFold(n_splits=cv, shuffle=True, random_state=self.random_state)

        scores = cross_val_score(self.model, X, y, cv=kfold, scoring='accuracy')

        logger.info(f"Cross-validation scores: {scores}")
        logger.info(f"Average cross-validation score: {scores.mean()}")
        return scores.mean()
    @abstractmethod
    def fit(self, X_train, y_train):
        """
        Fit the model on the training data.
        """
        pass

    @abstractmethod
    def predict(self, X_test):
        """
        Make predictions on the test data.
        """
        pass

    def evaluate(self, X_test, y_test):
        """
        Evaluate the model on the test data and print out the classification report,
        including precision and accuracy.
        """
        predictions = self.predict(X_test)
        precision = precision_score(y_test, predictions)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)
        # logger.info(f"Evaluation results for {self.model_name}:\nPrecision: {precision}\nAccuracy: {accuracy}\n{report}")
        return precision, accuracy, report

    def plot_learning_curves(self, X_train, y_train, X_val, y_val, train_sizes=np.linspace(0.1, 1.0, 10)):
        """
        Plot the learning curves of the model for both training and validation sets for accuracy, precision, and f1-score.
        """
        metrics = {'accuracy': 'accuracy', 'precision': make_scorer(precision_score), 'f1_score': make_scorer(f1_score)}
        graphs_folder = 'data/graphs'
        if not os.path.exists(graphs_folder):
            os.makedirs(graphs_folder)

        for metric_name, scorer in metrics.items():
            train_sizes, train_scores, validation_scores = learning_curve(
                self.model, X_train, y_train, train_sizes=train_sizes, cv=5,
                scoring=scorer, n_jobs=-1, shuffle=True, random_state=self.random_state
            )

            # Calculate the mean and standard deviation of the training and validation scores
            train_scores_mean = np.mean(train_scores, axis=1)
            train_scores_std = np.std(train_scores, axis=1)
            validation_scores_mean = np.mean(validation_scores, axis=1)
            validation_scores_std = np.std(validation_scores, axis=1)

            # Plot the learning curves
            plt.figure()
            plt.title(f"Learning Curves ({self.model_name} - {metric_name})")
            plt.xlabel("Training examples")
            plt.ylabel(f"{metric_name.capitalize()} score")
            plt.grid()

            # Plot the bands for the standard deviation
            plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                             train_scores_mean + train_scores_std, alpha=0.1, color="r")
            plt.fill_between(train_sizes, validation_scores_mean - validation_scores_std,
                             validation_scores_mean + validation_scores_std, alpha=0.1, color="g")

            # Plot the average training and validation scores
            plt.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training score")
            plt.plot(train_sizes, validation_scores_mean, 'o-', color="g", label="Cross-validation score")

            plt.legend(loc="best")

            # Save the plot
            graph_path = os.path.join(graphs_folder, f"{self.model_name}_{metric_name}_learning_curve.png")
            plt.savefig(graph_path)
            logger.info(f"Saved learning curve plot for {metric_name} to {graph_path}")
            plt.close()

        return graphs_folder  # Return the path where the graphs are saved
