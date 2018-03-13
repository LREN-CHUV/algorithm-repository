import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from scipy.misc import logsumexp


class MixedNB(BaseEstimator, ClassifierMixin):
    """Naive Bayes for mix of continuous and nominal features. For continuous variables
    the likelihood of the features is assumed to be Gaussian and for nominal features the
    likelihood is multinomial."""

    def __init__(self, is_nominal=None, alpha=1., class_prior=None):
        """
        :param is_nominal: boolean array indicating which columns are nominal.
            For technical reasons, continuous variables must go first in X matrix!
        :param alpha: see MultinomialNB
        :param class_prior: see MultinomialNB
        """
        self.is_nominal = is_nominal
        self.multi_nb = MultinomialNB(alpha=alpha, class_prior=class_prior, fit_prior=class_prior is None)
        self.gauss_nb = GaussianNB(priors=class_prior)

    def _is_nominal(self, X):
        is_nominal = np.array(self.is_nominal)
        assert X.shape[1] == len(is_nominal), 'length of is_nominal array is not the same as number of features'
        assert all(sorted(is_nominal) == is_nominal), 'Continuous variables must go first in X matrix'
        return is_nominal

    def fit(self, X, y, **kwargs):
        is_nominal = self._is_nominal(X)
        if any(is_nominal):
            self.multi_nb.fit(X[:, is_nominal], y, **kwargs)
        if any(~is_nominal):
            self.gauss_nb.fit(X[:, ~is_nominal], y, **kwargs)
        return self

    def partial_fit(self, X, y, **kwargs):
        is_nominal = self._is_nominal(X)
        if any(is_nominal):
            self.multi_nb.partial_fit(X[:, is_nominal], y, **kwargs)
        if any(~is_nominal):
            self.gauss_nb.partial_fit(X[:, ~is_nominal], y, **kwargs)
        return self

    def _multi_joint_log_likelihood(self, X):
        is_nominal = self._is_nominal(X)
        if all(~is_nominal):
            return 0

        return X[:, is_nominal].dot(self.multi_nb.feature_log_prob_.T)

    def _gauss_joint_log_likelihood(self, X):
        is_nominal = self._is_nominal(X)
        if all(is_nominal):
            return 0

        X = X[:, ~is_nominal]
        joint_log_likelihood = []
        for i in range(np.size(self.gauss_nb.classes_)):
            n_ij = - 0.5 * np.sum(np.log(2. * np.pi * self.gauss_nb.sigma_[i, :]))
            n_ij -= 0.5 * np.sum(((X - self.gauss_nb.theta_[i, :]) ** 2) /
                                 (self.gauss_nb.sigma_[i, :]), 1)
            joint_log_likelihood.append(n_ij)

        joint_log_likelihood = np.array(joint_log_likelihood).T
        return joint_log_likelihood

    @property
    def classes_(self):
        if hasattr(self.multi_nb, 'classes_'):
            return self.multi_nb.classes_
        else:
            return self.gauss_nb.classes_

    @property
    def class_log_prior_(self):
        if hasattr(self.multi_nb, 'class_log_prior_'):
            return self.multi_nb.class_log_prior_
        else:
            return np.log(self.gauss_nb.class_prior_)

    def predict_proba(self, X):
        loglike = self._multi_joint_log_likelihood(X) + self._gauss_joint_log_likelihood(X) + self.class_log_prior_
        norm = logsumexp(loglike, axis=1)
        probs = np.exp(loglike - norm[:, np.newaxis])
        return probs

    def predict(self, X):
        probs = self.predict_proba(X)
        return self.classes_[np.argmax(probs, 1)]
