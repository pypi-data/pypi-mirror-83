""" Custom models. """
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin


class RandomClassifier(BaseEstimator, ClassifierMixin):
    """
    Random classifier that computes the classes and their distribution from the trainings data.
    Predicts classes according to calculated probabilities or with uniform distribution.
    """

    def __init__(self, uniform=False):
        """
        Constructor for random classifier.
        Args:
            uniform: if False, uses class distribution in training data as probability for
            prediction.
        """
        self.classes = [0, 1, 2]
        self.probabilites = []
        self.uniform = uniform

    def fit(self, X, y, **fit_args):
        """
        Uses the unique targets as classes and calculates the distribution in the data, and stores
        that in form of probabilities.
        Args:
            X: the training data
            y: the target values, corresponding to X
            **fit_args:

        Returns: self
        """
        # figure out distribution of classes in the data
        self.classes, counts = np.unique(y, return_counts=True)
        self.probabilites = counts / len(y)
        return self

    def predict(self, X):
        """
        Chooses a class randomly which appear in training data. Depending on parameter uniform in
        constructor, uses uniform distribution or based on probabilities calculated from training
        data.
        Args:
            X: list of cases for which we want a prediction

        Returns:

        """
        if self.uniform:
            return [np.random.choice(self.classes) for x in X]
        else:
            return [np.random.choice(self.classes, p=self.probabilites) for x in X]
