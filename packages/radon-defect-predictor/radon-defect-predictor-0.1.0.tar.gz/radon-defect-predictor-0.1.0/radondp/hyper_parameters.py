import numpy as np

decision_tree_params = dict(
    classification__criterion=['gini', 'entropy'],
    classification__splitter=['best', 'random'],
    classification__max_features=['auto', 'sqrt', 'log2', None],
    classification__class_weight=['balanced', None]
)

naive_params = dict(classification__var_smoothing=np.logspace(start=-10, stop=-8, num=10))

logistic_params = dict(
    classification__penalty=['l2', 'none'],
    classification__tol=np.logspace(-5, -3, 10),
    classification__C=np.linspace(0, 2, 10),
    classification__class_weight=[None, 'balanced'],
    classification__solver=['lbfgs', 'sag', 'saga'],
    classification__fit_intercept=[False, True]
)

max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
max_depth.append(None)

random_forest_params = dict(
    classification__n_estimators=[int(x) for x in np.linspace(start=100, stop=2000, num=10)],
    classification__max_features=['auto', 'sqrt'],
    classification__max_depth=max_depth,
    classification__bootstrap=[True, False]
)

svc_params = dict(
    classification__C=[int(x) for x in np.linspace(start=1, stop=1000, num=100)],
    classification__gamma=['scale', 'auto'],
    classification__kernel=['rbf', 'sigmoid', 'poly'],
    classification__degree=[1, 2, 3, 4, 5],
    classification__shrinking=[False, True],
    classification__tol=[x for x in np.logspace(start=-5, stop=-1, num=10)],
    classification__class_weight=[None, 'balanced']
)

search_params_map = {
    'dt': decision_tree_params,
    'nb': naive_params,
    'logit': logistic_params,
    'rf': random_forest_params,
    'svm': svc_params
}
