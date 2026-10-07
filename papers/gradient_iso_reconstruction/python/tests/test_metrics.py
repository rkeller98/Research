import numpy as np
from numpy.testing import assert_allclose
from experiments import classification_metrics


def test_rank_endpoints_and_ties():
    labels = np.array([True, False, True, False])
    perfect, roc, _ = classification_metrics(labels, [4, 2, 3, 1], labels)
    assert perfect["auc"] == 1 and perfect["ap"] == 1
    assert roc[0][0] == 0 and roc[1][0] == 0
    assert roc[0][-1] == 1 and roc[1][-1] == 1
    tied, _, _ = classification_metrics(labels, np.ones(4), labels)
    assert_allclose([tied["auc"], tied["ap"]], [.5, .5])
    reversed_rank, _, _ = classification_metrics(labels, [1, 3, 2, 4], labels)
    assert reversed_rank["auc"] == 0
