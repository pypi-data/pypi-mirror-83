"""
The :mod:`sklearn.model_selection._validation` module includes classes and
functions to validate the model.
"""

import warnings

import numpy as np
import scipy.sparse as sp
from joblib import Parallel, delayed

from ..base import is_classifier, clone
from ..utils import indexable
from ..utils.validation import _check_fit_params
from ..utils.validation import _deprecate_positional_args
from ..utils.metaestimators import _safe_split
from ._split import check_cv
from ._label import LabelEncoder


@_deprecate_positional_args
def cross_val_predict(estimator, X, y=None, *, groups=None, cv=None,
                      n_jobs=None, verbose=0, fit_params=None,
                      pre_dispatch='2*n_jobs', method='predict'):
    """Generate cross-validated estimates for each input data point

    The data is split according to the cv parameter. Each sample belongs
    to exactly one test set, and its prediction is computed with an
    estimator fitted on the corresponding training set.

    Passing these predictions into an evaluation metric may not be a valid
    way to measure generalization performance. Results can differ from
    :func:`cross_validate` and :func:`cross_val_score` unless all tests sets
    have equal size and the metric decomposes over samples.

    Read more in the :ref:`User Guide <cross_validation>`.

    Parameters
    ----------
    estimator : estimator object implementing 'fit' and 'predict'
        The object to use to fit the data.

    X : array-like of shape (n_samples, n_features)
        The data to fit. Can be, for example a list, or an array at least 2d.

    y : array-like of shape (n_samples,) or (n_samples, n_outputs), \
            default=None
        The target variable to try to predict in the case of
        supervised learning.

    groups : array-like of shape (n_samples,), default=None
        Group labels for the samples used while splitting the dataset into
        train/test set. Only used in conjunction with a "Group" :term:`cv`
        instance (e.g., :class:`GroupKFold`).

    cv : int, cross-validation generator or an iterable, default=None
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:

        - None, to use the default 5-fold cross validation,
        - int, to specify the number of folds in a `(Stratified)KFold`,
        - :term:`CV splitter`,
        - An iterable yielding (train, test) splits as arrays of indices.

        For int/None inputs, if the estimator is a classifier and ``y`` is
        either binary or multiclass, :class:`StratifiedKFold` is used. In all
        other cases, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validation strategies that can be used here.

        .. versionchanged:: 0.22
            ``cv`` default value if None changed from 3-fold to 5-fold.

    n_jobs : int, default=None
        Number of jobs to run in parallel. Training the estimator and
        predicting are parallelized over the cross-validation splits.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.

    verbose : int, default=0
        The verbosity level.

    fit_params : dict, defualt=None
        Parameters to pass to the fit method of the estimator.

    pre_dispatch : int or str, default='2*n_jobs'
        Controls the number of jobs that get dispatched during parallel
        execution. Reducing this number can be useful to avoid an
        explosion of memory consumption when more jobs get dispatched
        than CPUs can process. This parameter can be:

            - None, in which case all the jobs are immediately
              created and spawned. Use this for lightweight and
              fast-running jobs, to avoid delays due to on-demand
              spawning of the jobs

            - An int, giving the exact number of total jobs that are
              spawned

            - A str, giving an expression as a function of n_jobs,
              as in '2*n_jobs'

    method : {'predict', 'predict_proba', 'predict_log_proba', \
              'decision_function'}, default='predict'
        The method to be invoked by `estimator`.

    Returns
    -------
    predictions : ndarray
        This is the result of calling `method`. Shape:

            - When `method` is 'predict' and in special case where `method` is
              'decision_function' and the target is binary: (n_samples,)
            - When `method` is one of {'predict_proba', 'predict_log_proba',
              'decision_function'} (unless special case above):
              (n_samples, n_classes)
            - If `estimator` is :term:`multioutput`, an extra dimension
              'n_outputs' is added to the end of each shape above.

    See also
    --------
    cross_val_score : calculate score for each CV split

    cross_validate : calculate one or more scores and timings for each CV split

    Notes
    -----
    In the case that one or more classes are absent in a training portion, a
    default score needs to be assigned to all instances for that class if
    ``method`` produces columns per class, as in {'decision_function',
    'predict_proba', 'predict_log_proba'}.  For ``predict_proba`` this value is
    0.  In order to ensure finite output, we approximate negative infinity by
    the minimum finite float value for the dtype in other cases.

    Examples
    --------
    >>> from sklearn import datasets, linear_model
    >>> from sklearn.model_selection import cross_val_predict
    >>> diabetes = datasets.load_diabetes()
    >>> X = diabetes.data[:150]
    >>> y = diabetes.target[:150]
    >>> lasso = linear_model.Lasso()
    >>> y_pred = cross_val_predict(lasso, X, y, cv=3)
    """
    X, y, groups = indexable(X, y, groups)

    cv = check_cv(cv, y, classifier=is_classifier(estimator))

    # If classification methods produce multiple columns of output,
    # we need to manually encode classes to ensure consistent column ordering.
    encode = method in ['decision_function', 'predict_proba',
                        'predict_log_proba'] and y is not None
    if encode:
        y = np.asarray(y)
        if y.ndim == 1:
            le = LabelEncoder()
            y = le.fit_transform(y)
        elif y.ndim == 2:
            y_enc = np.zeros_like(y, dtype=int)
            for i_label in range(y.shape[1]):
                y_enc[:, i_label] = LabelEncoder().fit_transform(y[:, i_label])
            y = y_enc

    # We clone the estimator to make sure that all the folds are
    # independent, and that it is pickle-able.
    parallel = Parallel(n_jobs=n_jobs, verbose=verbose,
                        pre_dispatch=pre_dispatch)
    prediction_blocks = parallel(delayed(_fit_and_predict)(
        clone(estimator), X, y, train, test, verbose, fit_params, method)
        for train, test in cv.split(X, y, groups))

    # Concatenate the predictions
    predictions = [pred_block_i for pred_block_i, _ in prediction_blocks]
    test_indices = np.concatenate([indices_i
                                   for _, indices_i in prediction_blocks])

    if not _check_is_permutation(test_indices, _num_samples(X)):
        raise ValueError('cross_val_predict only works for partitions')

    inv_test_indices = np.empty(len(test_indices), dtype=int)
    inv_test_indices[test_indices] = np.arange(len(test_indices))

    if sp.issparse(predictions[0]):
        predictions = sp.vstack(predictions, format=predictions[0].format)
    elif encode and isinstance(predictions[0], list):
        # `predictions` is a list of method outputs from each fold.
        # If each of those is also a list, then treat this as a
        # multioutput-multiclass task. We need to separately concatenate
        # the method outputs for each label into an `n_labels` long list.
        n_labels = y.shape[1]
        concat_pred = []
        for i_label in range(n_labels):
            label_preds = np.concatenate([p[i_label] for p in predictions])
            concat_pred.append(label_preds)
        predictions = concat_pred
    else:
        predictions = np.concatenate(predictions)

    if isinstance(predictions, list):
        return [p[inv_test_indices] for p in predictions]
    else:
        return predictions[inv_test_indices]


def _fit_and_predict(estimator, X, y, train, test, verbose, fit_params,
                     method):
    """Fit estimator and predict values for a given dataset split.

    Read more in the :ref:`User Guide <cross_validation>`.

    Parameters
    ----------
    estimator : estimator object implementing 'fit' and 'predict'
        The object to use to fit the data.

    X : array-like of shape (n_samples, n_features)
        The data to fit.

        .. versionchanged:: 0.20
            X is only required to be an object with finite length or shape now

    y : array-like of shape (n_samples,) or (n_samples, n_outputs) or None
        The target variable to try to predict in the case of
        supervised learning.

    train : array-like of shape (n_train_samples,)
        Indices of training samples.

    test : array-like of shape (n_test_samples,)
        Indices of test samples.

    verbose : int
        The verbosity level.

    fit_params : dict or None
        Parameters that will be passed to ``estimator.fit``.

    method : str
        Invokes the passed method name of the passed estimator.

    Returns
    -------
    predictions : sequence
        Result of calling 'estimator.method'

    test : array-like
        This is the value of the test parameter
    """
    # Adjust length of sample weights
    fit_params = fit_params if fit_params is not None else {}
    fit_params = _check_fit_params(X, fit_params, train)

    X_train, y_train = _safe_split(estimator, X, y, train)
    X_test, _ = _safe_split(estimator, X, y, test, train)

    if y_train is None:
        estimator.fit(X_train, **fit_params)
    else:
        estimator.fit(X_train, y_train, **fit_params)
    func = getattr(estimator, method)
    predictions = func(X_test)

    encode = method in ['decision_function', 'predict_proba',
                        'predict_log_proba'] and y is not None

    if encode:
        if isinstance(predictions, list):
            predictions = [_enforce_prediction_order(
                estimator.classes_[i_label], predictions[i_label],
                n_classes=len(set(y[:, i_label])), method=method)
                for i_label in range(len(predictions))]
        else:
            # A 2D y array should be a binary label indicator matrix
            n_classes = len(set(y)) if y.ndim == 1 else y.shape[1]
            predictions = _enforce_prediction_order(
                estimator.classes_, predictions, n_classes, method)
    return predictions, test


def _enforce_prediction_order(classes, predictions, n_classes, method):
    """Ensure that prediction arrays have correct column order

    When doing cross-validation, if one or more classes are
    not present in the subset of data used for training,
    then the output prediction array might not have the same
    columns as other folds. Use the list of class names
    (assumed to be ints) to enforce the correct column order.

    Note that `classes` is the list of classes in this fold
    (a subset of the classes in the full training set)
    and `n_classes` is the number of classes in the full training set.
    """
    if n_classes != len(classes):
        recommendation = (
            'To fix this, use a cross-validation '
            'technique resulting in properly '
            'stratified folds')
        warnings.warn('Number of classes in training fold ({}) does '
                      'not match total number of classes ({}). '
                      'Results may not be appropriate for your use case. '
                      '{}'.format(len(classes), n_classes, recommendation),
                      RuntimeWarning)
        if method == 'decision_function':
            if (predictions.ndim == 2 and
                    predictions.shape[1] != len(classes)):
                # This handles the case when the shape of predictions
                # does not match the number of classes used to train
                # it with. This case is found when sklearn.svm.SVC is
                # set to `decision_function_shape='ovo'`.
                raise ValueError('Output shape {} of {} does not match '
                                 'number of classes ({}) in fold. '
                                 'Irregular decision_function outputs '
                                 'are not currently supported by '
                                 'cross_val_predict'.format(
                                    predictions.shape, method, len(classes)))
            if len(classes) <= 2:
                # In this special case, `predictions` contains a 1D array.
                raise ValueError('Only {} class/es in training fold, but {} '
                                 'in overall dataset. This '
                                 'is not supported for decision_function '
                                 'with imbalanced folds. {}'.format(
                                    len(classes), n_classes, recommendation))

        float_min = np.finfo(predictions.dtype).min
        default_values = {'decision_function': float_min,
                          'predict_log_proba': float_min,
                          'predict_proba': 0}
        predictions_for_all_classes = np.full((_num_samples(predictions),
                                               n_classes),
                                              default_values[method],
                                              dtype=predictions.dtype)
        predictions_for_all_classes[:, classes] = predictions
        predictions = predictions_for_all_classes
    return predictions


def _check_is_permutation(indices, n_samples):
    """Check whether indices is a reordering of the array np.arange(n_samples)

    Parameters
    ----------
    indices : ndarray
        int array to test
    n_samples : int
        number of expected elements

    Returns
    -------
    is_partition : bool
        True iff sorted(indices) is np.arange(n)
    """
    if len(indices) != n_samples:
        return False
    hit = np.zeros(n_samples, dtype=bool)
    hit[indices] = True
    if not np.all(hit):
        return False
    return True