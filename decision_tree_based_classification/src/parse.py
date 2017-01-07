import csv


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def process_data(file_name):
    ''' 
    Process data into tuple_dicts assuming LIBSVM format
    '''
    with open(file_name, 'rb') as f:
        reader = csv.reader(f)
        data = [tup[0].split() for tup in list(reader) if tup]
        f.close()
    labels = [tup[0] for tup in data]
    tups = [tup[1:] for tup in data]

    tup_dicts = []
    for tup, label in zip(tups, labels):
        tup_dict = {}
        for key_val in tup:
            key = key_val.split(':')[0]
            val = key_val.split(':')[1]
            if is_number(val):
                val = float(val)
                
            if key in tup_dict:
                tup_dict[key].append(val)
            else:
                tup_dict[key] = [val]

        tup_dict['label'] = int(label)
        tup_dicts.append(tup_dict)
    return tup_dicts
        
