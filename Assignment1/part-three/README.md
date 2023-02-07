## Naive Bayes Sentiment Polarity Classifier

The code in the naive_bayes Python file is split into a main function for
calling the high-level function, and a NaiveBayes class that implements the
NaiveBayes classifier. The NaiveBayes classifier is first trained on the training
corpus, this involves getting the counts of words and documents of each sentiment. 
With these counts the probability of the class and a word given a class can be
computed. Add-alpha smoothing is used to introduce low probabilities for words
that don't occur in one of the classes. The format of the training data is set
out in main. The files for training are read in, inserted as values into a
dictionary with the key as the class. This means NaiveBayes accepts as dictionary
in the form training_data = {"positive": pos_train, "negative": neg_train}.

Once the model is trained, we are ready to make predictions. The test function
accepts 2 types of input. The test data in the same form as the training data, 
with the class labels as keys. The NaiveBayes will use the class labels provided
to determine the accuracy of each class and overall. Otherwise, with no class
labels, the model just predicts for each instance of a file in the dictionary.
Even if they are split amongst different items in the dictionary.

Changes can be made to the main function to introduce these changes, and change
the value of alpha for smoothing.

Folder contents:

+ [Naive Bayes - Python file](naive_bayes.py)
+ [Review Polarity Folder](review_polarity) - Raw data for training and evaluating
+ [Results](results) - Evaluation results, includes accuracy, correct and incorrect predictions
+ [Predictions](prediction) - Prediction results only when no class labels are passed.