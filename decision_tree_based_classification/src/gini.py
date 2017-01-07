import math
import random


label = 'label'


def get_frequency_dict(tup_dicts):
    '''
    Get a dictionary mapping a classification to the frequency
    of that classification in the dictionary
    '''
    frequency_dict = {}
    for tup in tup_dicts:
        if tup[label] in frequency_dict:
            frequency_dict[tup[label]] += 1
        else:
            frequency_dict[tup[label]] = 1
    
    return frequency_dict


def remove_attribute(tup_dicts, attr):
    for tup in tup_dicts:
        del tup[attr] 


def get_tups_with_val(tup_dicts, attr, val):
    '''
    Get all tuples in the dictionary with `val` for
    the `attr`
    '''
    new_tup_dicts = []
    for tup in tup_dicts:
        if tup[attr] == val:
            new_tup_dicts.append(tup)

    return new_tup_dicts


def get_split_groups(tup_dicts, attr):
    '''
    Partition tuples by the given attr
    '''
    val_set = set()
    split_groups = [] 
    for tup in tup_dicts:
        val = tup[attr]
        if frozenset(val) not in val_set:
            val_set.add(frozenset(val))
            split_groups.append(get_tups_with_val(tup_dicts, attr, val))

    return split_groups


def gini_set(tup_dicts):
    '''
    Calculate the gini index of the given set of tuples
    '''
    freq_dict = get_frequency_dict(tup_dicts)
    freq_sum = sum([(float(freq)/len(tup_dicts))**2 for freq in freq_dict.values()])

    return 1 - freq_sum


def gini_split(tup_dicts, attr):
    '''
    Calculate the gini index of splitting tuples by
    the given attribute
    Return the gini index and the groups
    '''
    split_groups = get_split_groups(tup_dicts, attr)
    gini = 0
    D = len(tup_dicts)

    for group in split_groups:
        Di = len(group)
        gini += float(Di)/float(D) * gini_set(group)

    return (gini, attr, split_groups)


def get_rand_attrs(attrs):
    '''
    Randomly choose sqrt(length(attrs)) attributes with replacement
    '''
    num_rand_attrs = int(math.sqrt(len(attrs)))
    rand_attrs = []

    for _ in range(num_rand_attrs):
        attr_num = random.randint(0, len(attrs) - 1)
        rand_attrs.append(attrs[attr_num])

    return rand_attrs


def get_split(tup_dicts, rand=False):
    '''
    Find the best attribute to split the given tuples by
    Return the attribute and the corresponding groups of tuples
    '''
    attrs = tup_dicts[0].keys()
    attrs.remove(label)
    if rand:
        attrs = get_rand_attrs(attrs)
    if not attrs:
        return None, None

    all_splits = [gini_split(tup_dicts, attr) for attr in attrs]
    least_impure = min(all_splits, key=lambda x: x[0])

    attr = least_impure[1]
    split_groups = least_impure[2]
    return (attr, split_groups)

