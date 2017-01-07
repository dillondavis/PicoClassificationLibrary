import sys
from parse import *
from tree import *
from metrics import *
import random


def run_forest_classifier():
    train_file = sys.argv[1] 
    test_file = sys.argv[2]
    
    train_tup_dicts = process_data(train_file)
    num_labels = len(set([tup[label] for tup in train_tup_dicts]))
    trees = build_forest(train_tup_dicts)

    test_tup_dicts = process_data(test_file)
    result_labels = []
    for tup_dict in test_tup_dicts:
        labels = []
        for tree in trees:
            tree_label = classify(tup_dict, tree) 
            labels.append(tree_label)
        mode_label = max(labels, key=lambda x:labels.count(x))
        result_labels.append(mode_label) 

    real_labels = [tup[label] for tup in test_tup_dicts]
    get_confusion_matrix(real_labels, result_labels, num_labels)
    get_all_metrics(real_labels, result_labels, '{}.RandomForest'.format(test_file))


if __name__ == '__main__':    
    run_forest_classifier()
