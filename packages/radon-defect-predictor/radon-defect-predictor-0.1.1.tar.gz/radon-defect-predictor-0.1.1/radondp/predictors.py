import io
import numpy as np
import os
import pandas as pd
import joblib
import json

from typing import List

from imblearn.pipeline import Pipeline
from sklearn.metrics import make_scorer, matthews_corrcoef
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import RandomizedSearchCV

from .balancers import balancers_map
from .classifiers import classifiers_map
from .hyper_parameters import search_params_map
from .normalizers import normalizers_map
from .model_validation import walk_forward_release


def prepare_training_data(data: pd.DataFrame):
    assert 'failure_prone' in data.columns
    assert 'commit' in data.columns
    assert 'committed_at' in data.columns
    assert 'filepath' in data.columns

    data = data.fillna(0)

    # Create a column group to group observations of the same release (identified by the commit)
    data['group'] = data.commit.astype('category').cat.rename_categories(range(1, data.commit.nunique() + 1))

    # Make sure the data is sorted by commit time (ascending)
    data.sort_values(by=['committed_at'], ascending=True)
    data = data.reset_index(drop=True)

    # Remove metadata
    data = data.drop(['commit', 'committed_at', 'filepath'], axis=1)

    X, y = data.drop(['failure_prone'], axis=1), data.failure_prone.values.ravel()

    return X, y


class DefectPredictor:

    def __init__(self):
        """
        Initialize a new DefectPredictor
        """

        self._balancers = []
        self._classifiers = []
        self._normalizers = []

        self.cv_report_map = dict()
        self.best_estimator = None
        self.best_estimator_average_precision = 0
        self.selected_features = list()

    @property
    def balancers(self):
        return self._balancers

    @balancers.setter
    def balancers(self, balancers: List[str]):
        for balancer in balancers:
            if balancer not in ('none', 'rus', 'ros'):
                raise ValueError(f'{balancer} is not supported')

            self._balancers.append(balancers_map[balancer])

    @property
    def normalizers(self):
        return self._normalizers

    @normalizers.setter
    def normalizers(self, normalizers: List[str]):
        for normalizer in normalizers:
            if normalizer not in ('none', 'minmax', 'std'):
                raise ValueError(f'{normalizer} is not supported')

            self._normalizers.append(normalizers_map[normalizer])

    @property
    def classifiers(self):
        return self._classifiers

    @classifiers.setter
    def classifiers(self, classifiers: List[str]):
        for classifier in classifiers:
            if classifier not in ('dt', 'logit', 'nb', 'rf', 'svm'):
                raise ValueError(f'{classifier} is not supported')

            self._classifiers = classifiers

    def train(self, data: pd.DataFrame) -> Pipeline:
        """
        Return the best fitted estimator, that is, the one that maximizes the average_precision
        :yield: the cross-validation report for every classifier
        :return: an estimator of type Pipeline
        """

        X, y = prepare_training_data(data)
        releases = X.group.tolist()
        X = X.drop(['group'], axis=1)

        scoring = dict(
            roc_auc='roc_auc',
            average_precision='average_precision',
            accuracy='accuracy',
            balanced_accuracy='balanced_accuracy',
            precision='precision',
            recall='recall',
            f1='f1',
            mcc=make_scorer(matthews_corrcoef)
        )

        for classifier in self.classifiers:
            estimator = classifiers_map[classifier]

            pipe = Pipeline([
                ('variance', VarianceThreshold(threshold=0)),  # Remove constant features
                ('balancing', None),  # To balance the training data See search_params['balancing'] below)
                ('normalization', None),  # To scale (and center) data. See search_params['normalization'] below
                # TODO feature_selection here
                ('classification', estimator)
            ])

            search_params = search_params_map[classifier]

            if self.balancers:
                search_params['balancing'] = self.balancers

            if self.normalizers:
                search_params['normalization'] = self.normalizers

            search = RandomizedSearchCV(pipe, search_params, cv=walk_forward_release(X, y, releases),
                                        scoring=scoring, refit='average_precision', verbose=0)

            search.fit(X, y)

            # Add additional metadata to the cv_results
            search.cv_results_['best_index_'] = search.best_index_

            buffer = io.StringIO()
            pd.DataFrame(search.cv_results_).to_json(buffer, orient='table', index=False)
            self.cv_report_map[classifier] = json.loads(buffer.getvalue())

            # Get the highest average_precision for this randomized search
            local_best_average_precision = search.cv_results_['mean_test_average_precision'][search.best_index_]

            if (not self.best_estimator) or (local_best_average_precision > self.best_estimator_average_precision):
                self.cv_report_map['best_classifier'] = classifier
                self.best_estimator = search.best_estimator_
                selected_features_indices = self.best_estimator.named_steps['variance'].fit(X).get_support(indices=True)
                self.selected_features = X.iloc[:, selected_features_indices].columns.tolist()

        return self.best_estimator

    def predict(self, unseen_data: pd.DataFrame) -> bool:
        """
        Predict an unseen instance as failure-prone or clean.
        :param unseen_data: pandas DataFrame containing the observation to predict
        :return: True if failure-prone. False, otherwise.
        """
        if not self.best_estimator:
            raise Exception('No model has been loaded yet. Please, load a model using instance.load(path_to_model_dir)')

        # Select same model features
        unseen_data = unseen_data[np.intersect1d(unseen_data.columns, self.selected_features)]

        # Perform pre-process if any
        if self.best_estimator.named_steps['normalization']:
            unseen_data = pd.DataFrame(self.best_estimator.named_steps['normalization'].transform(unseen_data))

        clf = self.best_estimator.named_steps['classification']
        prediction = bool(clf.predict(unseen_data)[0])

        return prediction

    def load_model(self, path_to_dir: str):
        """
        :param path_to_dir: the path to the directory containing model-related files
        :return: None
        """
        model = joblib.load(os.path.join(path_to_dir, 'radondp_model.joblib'), mmap_mode='r')
        self.best_estimator = model['model']
        self.selected_features = model['features']

    def dump_model(self, path_to_dir: str):
        """
        :param path_to_dir: the path to the directory containing model-related files
        :return: None
        """
        joblib.dump({'model': self.best_estimator,
                     'features': self.selected_features,
                     'report': self.cv_report_map},
                    os.path.join(path_to_dir, 'radondp_model.joblib'))
