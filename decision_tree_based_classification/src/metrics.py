

def write_metrics(accuracy, all_metrics, labels, classifier):
    '''
    Print out metrics for classification in readable format
    '''
    f = open('{}.metrics'.format(classifier), 'w')
    f.write('{} Metrics\n'.format(classifier))
    f.write('Accuracy: {}\n\n'.format(accuracy))
    
    for label_metrics, label in zip(all_metrics, labels):
        f.write('Target Label: {}\n'.format(label))
        metrics_names = label_metrics[0]
        metrics = label_metrics[1]
        for metric_name, metric in zip(metrics_names, metrics):
            f.write('\t{}: {}\n'.format(metric_name, metric))
        f.write('\n')

    f.close()


def get_accuracy(real_labels, result_labels):
    '''
    Calculate the accuracy of classified tuples
    '''
    correct_labels = 0
    
    for real, result in zip(real_labels, result_labels):
        if real == result:
            correct_labels += 1

    accuracy = float(correct_labels) / len(real_labels)

    return accuracy


def laplace_adjust(results):
    ''' 
    Add one to all values if a zero exists to avoid divide by zero errors
    '''
    if 0 in results:
        for i in range(4):
            results[i] += 1

def get_confusion_derivations(real_labels, result_labels, target):
    '''
    Find the number of true positives, false positives, true negatives, and false negatives
    '''
    tp = 0
    fp = 0
    tn = 0
    fn = 0

    for real, result in zip(real_labels, result_labels):
        if real == result:
            if real == target:
                tp += 1
            else:
                tn += 1
        else:
            if real == target:
                fn += 1
            else:
                fp += 1 

    results = [tp, fp, tn, fn]    
    laplace_adjust(results)
    return results


def get_metrics(real_labels, result_labels, target, classifier):
    '''
    Calculate relevant metrics for given classification results
    '''
    tp, fp, tn, fn = get_confusion_derivations(real_labels, result_labels, target)

    sensitivity = float(tp) / (tp + fn)
    specificity = float(tn) / (tn + fp)
    precision = float(tp) / (tp + fp)
    recall = sensitivity
    f1 = float(2*tp) / (2*tp + fp + fn)
    fhalf = float(1 + 0.5**2) * (precision * recall) / (0.5**2 * precision + recall)  
    f2 = float(1 + 2**2) * (precision * recall) / (2**2 * precision + recall)  

    metric_names = ['Sensitivity', 'Specificity', 'Precision', 'Recall', 'F1 Score', 'FHalf Score', 'F2 Score']
    metrics = [sensitivity, specificity, precision, recall, f1, fhalf, f2]

    return metric_names, metrics


def get_all_metrics(real_labels, result_labels, classifier):
    '''
    Calculate related metrics for classification results with each label as the target
    '''
    accuracy = get_accuracy(real_labels, result_labels)
    metrics = []
    label_set = list(set(real_labels))
      
    for label in label_set:
        label_metrics = get_metrics(real_labels, result_labels, label, classifier) 
        metrics.append(label_metrics)

    write_metrics(accuracy, metrics, label_set, classifier)


def get_confusion_matrix(real_labels, result_labels, num_labels):
    '''
    Find confusion matrix associated with classification results
    '''
    confusion = [[0]*num_labels for _ in range(num_labels)]
     
    for real, result in zip(real_labels, result_labels):
        confusion[real-1][result-1] += 1

    for row in confusion:
        for cell in row:
            print cell,
        print '\n',
