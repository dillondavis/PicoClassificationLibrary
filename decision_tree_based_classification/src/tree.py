from gini import *
import random
import copy


label = 'label'


class DTNode():
    def __init__(self, attr_val, tups):
        self.attr_val = attr_val
        self.tups = tups
        self.label = None
        self.children = None

root = None


def all_same_label(tup_dicts):
    '''
    Check if all tuples have the same label
    '''
    curr_label = None
    for tup in tup_dicts:
        if not curr_label:
            curr_label = tup[label]
        if tup[label] != curr_label:
            return False

    return True


def build_tree(tup_dicts, attr_val, rand=False):
    '''
    Build a decision tree from the given training nodes
    '''
    node = DTNode(attr_val, tup_dicts)
    if all_same_label(tup_dicts):
        node.label = tup_dicts[0][label]
        node.children = None
        return node

    # Remove split attribute used to create this node
    if attr_val:
        remove_attribute(tup_dicts, attr_val[0])

    split_attr, split_groups = get_split(tup_dicts, rand)
    if not split_attr:
        label_freqs = get_frequency_dict(node.tups)
        node.label = max(label_freqs.items(), key=lambda x : x[1])[0]
        node.children = None
    else:
        node.children = [build_tree(tup_dicts, (split_attr, tup_dicts[0][split_attr]), rand) for tup_dicts in split_groups]

    return node


def get_random_subset(tup_dicts):
    subset_tups = []
    num_tups = len(tup_dicts)
    used_tup_nums = set() 

    for i in range(num_tups):
        tup_index = random.randint(0, num_tups - 1)
        if tup_index not in used_tup_nums:
            subset_tups.append(tup_dicts[tup_index])
            used_tup_nums.add(tup_index)

    return subset_tups


def build_forest(tup_dicts):
    '''
    Build a random forest with the given training data 
    '''
    num_trees = 128
    trees = []

    for _ in range(num_trees): 
        subset_sample = get_random_subset(tup_dicts)
        new_root = build_tree(copy.deepcopy(get_random_subset(tup_dicts)), None, rand=True)
        trees.append(new_root)

    return trees
    

def classify(tup_dict, node):
    '''
    Determine the label of a tuple using the decision tree
    '''
    if not node and not root:
        return None

    if not node.children:
        tup_class = node.tups[0][label]
        return tup_class

    for child in node.children:
        attr, val = child.attr_val

        if tup_dict[attr] == val:
            return classify(tup_dict, child)

    max_node = max(node.children, key=lambda x:len(x.tups))
    return classify(tup_dict, max_node)

