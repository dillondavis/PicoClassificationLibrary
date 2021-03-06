# PicoClassificationLibrary
Implementation of fundamental classification algorithms

  # Classifiers
  
    # Decision Tree (Python)
    Implemented with multi-way branching and Gini Index as the attribute selection measure.
    example usage: python src/DecisionTree.py training_data testing_data

    # Random Forest (Python)
    Implemented with the aforementioned decision tree, bagging, random sampling with replacement, 128 trees, and log(number of remaining attributes) attributes considered for branching.
    example usage: python src/RandomForest.py training_data testing_data

    # Naive Bayes (Clojure)
    Implementation of Gaussian Naive Bayes in Clojure
    
    # Neural Network (Clojure)
    In progress
    
  # Data<br>
    Python Classifiers are built assuming training and testing data are in LIBSVM format<br>
    Naive Bayes assumes basic CSV format
   
  # Results<br>
    Running classifiers will output a confusion matrix corresponding to classification of the testing data and a metrics file
    including Accuracy, Sensitivity, Specificity, Precision, Recall, F-1 Score, F-Half Score, and F-2 Score.
    
    
   
