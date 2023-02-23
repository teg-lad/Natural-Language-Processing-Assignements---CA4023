## Naive Bayes Sentiment Polarity Classifier

#### Running this script

This script can be run on the commandline by passing the names of folder in the
current directory as input for training and testing. e.g. python naive_bayes.py <training_dir> <test_dir>.
Note that the training directory should have a subdirectory for each class with the
corresponding examples in the folder for that class. The test directory should follow
the same format if evaluation is desired, if the subdirectories do not match the class
labels only prediction will occur. 

NOTE: The script has been changed to accommodate .txt file input. These can be input in place of the
test dir above. python naive_bayes.py <training_dir> <test_dir/test.txt>. The text file is expected to
have a review on each line so that splitting on \n character returns a list of reviews. The reviews
from the .txt file are converted into singular reviews and stored in a folder format as previously was
accepted. The predictions are written to the prediction folder as before.



#### Script overview

The code in the naive_bayes Python file is split into a main function for
calling the high-level function, and a NaiveBayes class that implements the
NaiveBayes classifier. The NaiveBayes classifier is first trained on the training
corpus, this involves getting the counts of words and documents of each sentiment. 
With these counts the probability of the class and a word given a class can be
computed. Add-alpha smoothing is used to introduce low probabilities for words
that don't occur in one of the classes.

The data is read in from a folder structure by the return_files function. This
takes a path to a directory and takes all the subdirectories to be classes with
the related files listed. This returns a dictionary with {"classname": [list of files]}.
The training, test and test_with_gt folders are available in the repo. training 
contains the class labels as subdirectories, as does test_with_gt. Test contains
a subdirectory that does not match the classes from the training set, so only
predictions can be made.

Once the model is trained, we are ready to make predictions. The test function
accepts 2 forms of input. If the test data contains class labels as keys then we
can compute the accuracy of all classes and the total accuracy. If the data dictionary
keys do not match the class labels from training then we can only predict for each
example in the test set.

Changes can be made in the main function to adjust the alpha value for smoothing and
the program can be called from the command line with the training directory and test
directory passed as arguments. e.g. python naive_bayes <training_dir> <test_dir>

Folder contents:

+ [Naive Bayes - Python file](naive_bayes.py) - python file for my NaiveBayes implementation.
+ [ANALYSIS.md](ANALYSIS.md) - Analysis markdown file.
+ [Review Polarity Folder](review_polarity) - Raw data for training and evaluating
+ [Training Folder](training) - Contains the class labels as subdirectories which contain the training examples of that class.
+ [Test Folder](test) - Folder with all test samples together, allowing for prediction only
+ [Test with Ground Truth](test_with_gt) - Folder with test samples split by class, allowing for accuracy to be computed.
+ [Sample Text](sample.txt) - Text file containing a review on each line for classification.
+ [Sample](sample) - Folder containing the sample.txt data in the format for the model.
+ [Results](results) - Evaluation results, includes accuracy, correct and incorrect predictions
+ [Predictions](prediction) - Prediction results only when no class labels are passed.
+ [Analysis Reviews](analysis_reviews) - Folder containing the reviews used during the analysis.
+ [Images](images) - Snippets of the reviews from the analysis for use in ANALYSIS.md.