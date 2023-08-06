import numpy as np
from sklearn.utils import indexable
from sklearn.utils.validation import _num_samples


def walk_forward_release(X, y, releases):
    """
    Generate train and test splits fro TimeSeriesSplit on releases.
    Train consists of a release or a list of successive releases, and
    the test set consist of the next release in time

    :param X: array-like of shape (n_samples, m_features)
    :param y: array-like of shape (n_samples,)
    :param releases : array-like of shape (n_samples,)
        Group labels for the samples used while splitting the dataset into
        train/test set.
        Must be an ordered list of integer, i.e., [1, 1, 1, 2, 2, 3, 4, 4, etc.].
        Each integer denote a given release. Files within the same release have the same
        group id.
    """
    X, _, releases = indexable(X, y, releases)
    n_samples = _num_samples(X)
    n_folds = len(set(releases))  # Number of distinct groups (releases)
    if n_folds > n_samples:
        raise ValueError(
            ("Cannot have number of folds ={0} greater"
             " than the number of samples: {1}.").format(n_folds, n_samples))

    indices = np.arange(n_samples)
    offset = 0

    for _ in range(0, n_folds - 1):
        train_indices = [i for i, x in enumerate(releases) if x == releases[offset]]
        offset += len(train_indices)
        test_indices = [i for i, x in enumerate(releases) if x == releases[offset]]

        yield indices[:offset], indices[offset: offset + len(test_indices)]
