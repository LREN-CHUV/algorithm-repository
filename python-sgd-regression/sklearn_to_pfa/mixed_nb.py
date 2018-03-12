from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB


class MixedNB:
    """Naive Bayes for mix of continuous and nominal features. For continuous variables
    the likelihood of the features is assumed to be Gaussian and for nominal features the
    likelihood is multinomial."""

    def __init__(self, is_nominal, alpha=1., class_prior=None):
        """
        :param is_nominal: boolean array indicating which columns are nominal
        :param alpha: see MultinomialNB
        :param class_prior: see MultinomialNB
        """
        self.is_nominal = is_nominal
        self.multi_nb = MultinomialNB(alpha=alpha, class_prior=class_prior, fit_prior=class_prior is None)
        self.gauss_nb = GaussianNB(priors=class_prior)

    def fit(self, X, y, sample_weight=None):
        assert X.shape[1] == len(self.is_nominal), 'length of is_nominal array is not the same as number of features'
        self.multi_nb.fit(X[:, self.is_nominal], y, sample_weight=sample_weight)
        self.gauss_nb.fit(X[:, ~self.is_nominal], y, sample_weight=sample_weight)
        return self

    def partial_fit(self, X, y, sample_weight=None):
        assert X.shape[1] == len(self.is_nominal), 'length of is_nominal array is not the same as number of features'
        self.multi_nb.partial_fit(X[:, self.is_nominal], y, sample_weight=sample_weight)
        self.gauss_nb.partial_fit(X[:, ~self.is_nominal], y, sample_weight=sample_weight)
        return self

    def predict_proba(self):
        pass
