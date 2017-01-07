import sys
from parse import *
from tree import *
from metrics import *


def run_classifier():
    train_file = sys.argv[1]
    test_file = sys.argv[2]

    train_tup_dicts = process_data(train_file)
    num_labels = len(set([tup[label] for tup in train_tup_dicts]))
    root = build_tree(train_tup_dicts, None)

    test_tup_dicts = process_data(test_file)
    real_labels = [tup[label] for tup in test_tup_dicts]
    result_labels = [classify(tup_dict, root) for tup_dict in test_tup_dicts]

    get_confusion_matrix(real_labels, result_labels, num_labels)
    get_all_metrics(real_labels, result_labels, '{}.DecisionTree'.format(test_file))

if __name__ == '__main__':
    run_classifier()
