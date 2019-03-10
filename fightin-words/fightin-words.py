#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from typing import List, Union, Optional, Sequence

import numpy as np
import sklearn.base as sk_base
import sklearn.feature_extraction.text as sk_text

__version__ = '1.0.5'

class FWExtractor(sk_base.BaseEstimator, sk_base.TransformerMixin):
    """Compute Monroe et. al's [Monroe2008] fightin' words result.

    Largely derived from Jack Hessel's original implementation [Hessel2015]
    but modified to be compliant with scikit-learn conventions (for use in
    pipelines, etc.). Also some small technical improvements.

    Parameters
    ----------
    prior: float or list, default=0.01

        Starting Dirichlet prior that is smoothed over the input. If a float is
        provided, a uniform distribution is created over the vocabulary
        extracted from the corpora. If a list is provided, it is assumed that
        the user will _also_ be passing in their own count vectorizer, and that
        the dimensionality of both items match each other.

    cv: sklearn.feature_extraction.text.CountVectorizer or
        sklearn.feature_extraction.text.TfidfVectorizer or None, optional

        The vectorizer used to construct the word-occurrence frequency
        dictionary. If not specified, uses the default parameters for a naive
        implementation of scikit-learn's `CountVectorizer`.

    References
    ----------
    .. [Monroe2008] `Monroe, B. L., Colaresi, M. P., & Quinn, K. M. (2008).
                     Fightin'words: Lexical feature selection and evaluation
                     for identifying the content of political conflict.
                     Political Analysis, 16(4), 372-403.`
    .. [Hessel2015] `https://github.com/jmhessel/FightingWords`
    """

    def __init__(self, prior=0.01, cv=None):
        # type: (Union[float, List[float]], Optional[sk_text.CountVectorizer, sk_text.TfidfVectorizer]) -> None

        if cv is None:
            # Use the default scikit-learn vectorizer with sane defaults
            self.cv = sk_text.CountVectorizer(decode_error='ignore', max_features=15000)
        elif not (isinstance(cv, sk_text.CountVectorizer) or isinstance(cv, sk_text.TfidfVectorizer)):
            raise TypeError(cv, 'Expected a scikit-learn CountVectorizer or TfidfVectorizer')
        else:
            self.cv = cv

        if not (isinstance(prior, list) or isinstance(prior, float)):
            raise TypeError(prior, 'Expected either a list or a float')
        else:
            self.prior = prior

    def fit(self, X, y=None, **params):
        """Unused"""
        return self

    def transform(self, X, **params):
        """Perform a comparison between two corpora, and compute/rank the z-scores for word tokens

        Parameters
        ----------
        X: list, [str, str]

            Pair of text corpora to be compared.
        """
        # type Sequence[str, str] -> List[Sequence[str, float]]

        # Compute Bag-of-words Model.
        counts = self.cv.fit_transform([' '.join(X)]).toarray()
        vocab_size = len(self.cv.vocabulary_)

        # Create a reverse-LUT to remap the vocabulary to human-readable words.
        index_to_term = {v: k for k, v in self.cv.vocabulary_.items()}

        if isinstance(self.prior, float):
            # Generate uniform prior distribution
            self.priors = [self.prior for i in xrange(vocab_size)]
        else:
            # Guaranteed to be dealing with a list in this block because the
            # class constructor would have caught bad types at initialization.
            if (len(self.prior) == vocab_size):
                self.priors = self.prior
            else:
                raise AssertionError(self.prior, 'Number of priors must match vocabulary size')

        z_scores = np.empty(np.array(self.priors).shape[0])
        count_matrix = np.empty([2, vocab_size], dtype=np.float32)

        count_matrix[0, :] = np.sum(counts[:len(X[0]), :], axis=0)
        count_matrix[1, :] = np.sum(counts[len(X[0]):, :], axis=0)

        a0 = np.sum(self.priors)

        n1 = np.sum(count_matrix[0, :], dtype=np.float32)
        n2 = np.sum(count_matrix[1, :], dtype=np.float32)

        for i in xrange(vocab_size):
            # Compute delta.
            term1 = np.log((count_matrix[0, i] + self.priors[i]) / (n1 + a0 - count_matrix[0, i] - self.priors[i]))
            term2 = np.log((count_matrix[1, i] + self.priors[i]) / (n2 + a0 - count_matrix[1, i] - self.priors[i]))
            delta = term1 - term2

            # Compute variance and standardize the z-score.
            var = 1 / (count_matrix[0, i] + self.priors[i]) + 1 / (count_matrix[1, i] + self.priors[i])
            z_scores[i] = delta / np.sqrt(var)

        # Return the results in descending order.
        return [(index_to_term[i], z_scores[i]) for i in np.argsort(z_scores)]
