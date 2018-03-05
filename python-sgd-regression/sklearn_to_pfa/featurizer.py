import numpy as np


class Featurizer:
    """Class for preprocessing input data to numerical format required for scikit-learn. Can transform
    input dataframe and also generate PrettyPFA code.
    Inspired by fit_transform from scikit-learn.
    """

    def __init__(self, transforms):
        self.transforms = transforms

    def transform(self, data):
        return np.hstack([tf.transform(data) for tf in self.transforms])

    def generate_pretty_pfa(self):
        """Generate string for PrettyPFA that converts input to array of doubles."""
        transforms_pfa = ',\n    '.join([t.pfa() for t in self.transforms])
        return """
new(array(double),
    {transforms}
);
        """.format(transforms=transforms_pfa).strip()


class Transform:
    """Transform implements methods `transform` and `pfa`.
    transform: X -> 2dim array
    pfa: generates PrettyPFA code
    """

    pass


class Standardize(Transform):

    def __init__(self, col, mu, sigma):
        self.col = col
        self.mu = mu
        self.sigma = sigma

    def transform(self, X):
        return ((X[self.col] - self.mu) / self.sigma)[:, np.newaxis]

    def pfa(self):
        return 'arr((x.{col} - {mu}) / {sigma})'.format(col=self.col, mu=self.mu, sigma=self.sigma)


class OneHotEncoding(Transform):

    def __init__(self, col, enumerations):
        self.col = col
        self.enumerations = enumerations

    def transform(self, X):
        Y = np.zeros((len(X), len(self.enumerations)))
        for i, val in enumerate(self.enumerations):
            Y[:, i] = X[self.col] == val
        return Y

    def pfa(self):
        return 'C(x.{col})'.format(col=self.col)
