import json
import math
from pathlib import Path
import string
import shutil


def main():
    """
    This is the main function that runs when the script is run. It reads in the data and splits it into train and test.
    The NaiveBayes class is initialized and passed the classes and alpha value.
    The model is then passed the training data to get the counts of documents and words. The probabilities are computed.
    Finally, the model is passed the test data and then prints the accuracy and outputs the data into the results
    folder. The folder contains a correct and incorrect sub-folder for classifications that are correct and incorrect,
    allowing for analysis.
    """

    # The classes we wish to use, can be changed to use the naive bayes for other classification tasks.
    sentiment_classes = ["positive", "negative"]

    # Split the data into the train and test for the 2 classes.
    pos_train, pos_test, neg_train, neg_test = split_and_return_files(900)

    # Create a dictionary with the training data and testing data as the values with the classes as the keys.
    training_data = {"positive": pos_train, "negative": neg_train}
    testing_data = {"positive": pos_test, "negative": neg_test}

    # The alternative is to pass the training data as a list with ground truth labels
    # testing_data = {"test": pos_test + neg_test}

    # Initialize the NaiveBayes class with the class list and an alpha value of 0.9 for smoothing.
    model = NaiveBayes(sentiment_classes, 0.9)

    # Train the model by passing the training dictionary, this computes the probabilities from the counts of words and
    # documents.
    model.train(training_data)

    # Pass the test dictionary to the model. If the keys match the classes we return the accuracy and results
    # folder, otherwise return the predictions in the predictions folder.
    model.test(testing_data)


class NaiveBayes:
    """
    This is the NaiveBayes class that is used to create a NaiveBayes classifier. It accepts a list of classnames and an
    alpha value for smoothing. The training data should be structured as a dictionary with the classes as keys and the
    files as a list. The test data is in the same format, if the keys match the classes then we can perform evaluation,
    otherwise prediction is carried out.
    """

    def __init__(self, classes: list, alpha: float = None):
        """
        This init method creates the class variables for tracking the counts, unique words, probabilities and smoothing.
        :param classes: List of classes to be used
        :param alpha: Value of alpha for smoothing
        """
        # List of classes for this classification task
        self.classes = classes

        # Set of unique words, count of words and documents of each class. Used to compute the probability
        self.unique = set()
        self.counts = {}
        self.doc_count = {}

        # Set alpha to one, this is laplace smoothing
        self.alpha = 1

        # If alpha has been specified we will set it to that value
        if alpha:
            self.alpha = alpha

        # Total words for each class, probabilites of classes and words in each class.
        self.total_words = {}
        self.class_probabilities = {}
        self.probabilities = {}

        # For every class, add a dictionary in the counts and probabilities. Initialize the doc count for a class at 0.
        for cls in self.classes:
            self.counts[cls] = {}
            self.probabilities[cls] = {}
            self.doc_count[cls] = 0

    def train(self, file_dict: dict):
        """
        This method takes a file dictionary and loops through the classes and files, getting the counts of words and
        documents. The probabilities can then be computed.
        :param file_dict: Dictionary with keys as classes and file paths as values
        """

        # For each class
        for cls in self.classes:
            # Get the reviews for that class
            files = file_dict[cls]

            # Open each file and pass the cls and data to the process_document method to get the counts.
            for file in files:
                with open(file) as f:
                    data = f.read()
                self.process_document(cls, data)

        # Once all the documents are processed we can compute all the probabilities.
        self.compute_probabilities()

    def test(self, file_dict: dict):
        """
        This method takes a dictionary of files, if the keys match the class list we can perform evaluation. Otherwise,
        we just perform prediction.
        :param file_dict: A dictionary with class labels as keys and file paths as values.
        """

        # Can we perform evaluation on this test data?
        evaluation = False

        # If the classes are keys in the file_dictionary we can:
        if self.classes == list(file_dict.keys()):
            evaluation = True

            # Keep track of the classifications we get correct for each class
            correct = {}

            # Set the count for each class to 0
            for cls in self.classes:
                correct[cls] = 0

        # If we are evaluating write to results, otherwise write to predictions
        if evaluation:
            output_path = Path.cwd() / "results"
        else:
            output_path = Path.cwd() / "prediction"

        # For every key and set of files in the file dictionary
        for k, files in file_dict.items():

            # For each file
            for file in files:

                # Open the file and read the data
                with open(file) as f:
                    data = f.read()

                # Our predicted class is returned from the predict_class function
                predicted = self.predict_class(data)

                # If we are evaluating, see if the class label matches the predicted. (k is the ground truth key).
                if evaluation:

                    # If they match, increment the correct value
                    if k == predicted:
                        correct[k] += 1

                        # This file will be output to the correct folder with the class a sub-folder.
                        file_output_path = output_path / "correct" / k

                    else:
                        # If it is incorrect, it will go to the incorrect folder.
                        file_output_path = output_path / "incorrect" / k

                else:
                    # If we are not evaluating, put the file into the prediction folder under the class it was predicted
                    # as.
                    file_output_path = output_path / predicted

                # Make sure that the directory the file will be written to exist, and the parents of the directory.
                file_output_path.mkdir(exist_ok=True, parents=True)

                # Copy the file from the path given to this output path.
                shutil.copyfile(file, file_output_path / file.name)

        # If we are evaluating
        if evaluation:

            # Write the results to our file.
            with open(output_path / "results.txt", "w") as r:

                # If we have more than one key we can find the accuracy for each group
                if len(file_dict.keys()) > 1:

                    # For each item in the dictionary
                    for k, v in file_dict.items():

                        # The accuracy of the item with key k is the correct for that key / number of files in that
                        # item.
                        cls_accuracy = f"The accuracy for {k} is {correct[k] / len(v)}"

                        # Print the string to stdout
                        print(cls_accuracy)

                        # Write the string to our results file.
                        r.write(cls_accuracy + "\n")

                # Get the total number of files and the total correct to find the total accuracy.
                total_files = sum([len(v) for k, v in file_dict.items()])
                total_correct = sum(correct.values())

                # Compute the overall accuracy
                accuracy = f"The overall accuracy is {total_correct / total_files}"

                # Print the accuracy to stdout
                print(accuracy)

                # Write the accuracy to our results file.
                r.write(accuracy + "\n")

        # Write the class probabilities to a json file for use during analysis.
        with open(output_path / "class_probabilities.json", "w") as c:
            json.dump(self.class_probabilities, c)

        # Write the word probabilities for each class to a json for use during analysis.
        with open(output_path / "probabilities.json", "w") as p:
            json.dump(self.probabilities, p)

    def increment_count(self, cls: str, word: str):
        """
        This function increments the count of a word in the counts dictionary for a class.
        :param cls: Class the word occurred in.
        :param word: The word that we increase the count for.
        """

        # If the word is already in the dictionary just increase the count.
        if word in self.counts[cls].keys():
            self.counts[cls][word] += 1

        # If it isn't, add it and set the count to 1
        else:
            self.counts[cls][word] = 1

    def process_document(self, cls: str, doc: str):
        """
        This function takes a document and the class and counts the words, tracks the unique words and increase the
        document count for this class.
        :param cls: The class the document belongs to.
        :param doc: The contents of the document.
        """

        # Increase the document count by 1 for the current class.
        self.doc_count[cls] += 1

        # Split the doc on whitespace and strip and set the values to lower case.
        words = [w.strip().lower() for w in doc.split(" ")]

        # For each word
        for word in words:

            # If the word is punctuation, we want to ignore it.
            if word in string.punctuation:
                continue

            # If it isn't punctuation, add it to the unique words and increase the count for this class.
            self.unique.add(word)
            self.increment_count(cls, word)

    def compute_probabilities(self):
        """
        This function computes the class probabilities and the probabilities for each word for that class. This makes
        use of the counts from processing the documents.
        """

        # Get the total number of unique words.
        total_unique_words = len(self.unique)

        # For every class
        for cls in self.classes:

            # The total words in this class
            self.total_words[cls] = sum(self.counts[cls].values())

            # Calculate the class probability.
            self.class_probabilities[cls] = self.doc_count[cls] / sum(self.doc_count.values())

            # For every word in the unique set of words.
            for word in self.unique:

                # If we have the word in the counts for this class, use the count to determine the probability.
                if word in self.counts[cls].keys():
                    word_count = self.counts[cls][word]

                # Otherwise, we have no count of this word for this class.
                else:
                    word_count = 0

                # Determine the probability of this word given this class using the counts and considering the alpha.
                # The log of this is taken, so we can sum the probabilities to find the total for a class.
                self.probabilities[cls][word] = math.log(
                    (word_count + self.alpha) / (self.total_words[cls] + (self.alpha * total_unique_words)))

    def predict_class(self, doc: str):
        """
        This function takes a document and predicts a sentiment class.
        :param doc: The document for a prediction to be made on.
        :return: class of prediction.
        """
        # A dictionary for capturing the probabilities of both classes.
        probabilities = {}

        # For each class.
        for cls in self.classes:

            # Set up a list for storing the probabilities.
            probabilities[cls] = []

            # Split the document as before during training, on the whitespace and strip the word and put it in
            # lowercase.
            words = [w.strip().lower() for w in doc.split(" ")]

            # For each word
            for word in words:

                # If we have seen the word before, we will add the probability to the list for this class.
                if word in self.unique:
                    probabilities[cls].append(self.probabilities[cls][word])

            # The probability of this class is the sum of the log probabilities in the list.
            cls_prob = sum(probabilities[cls])
            probabilities[cls] = cls_prob

        # Return the class with the higher probability.
        return max(probabilities, key=probabilities.get)


def split_and_return_files(index: int):
    """
    Splits the files in the positive and negative folder and returns the files before the index as train and the files
    after for test.
    :param index: The index at which to split the files, using < and >=
    :return: pos_train, pos_test, neg_train, neg_test
    """

    # Create the base path
    base_path = Path.cwd() / "review_polarity" / "txt_sentoken"

    # Create both the positive and negative paths
    pos = base_path / "pos"
    neg = base_path / "neg"

    # Create a list with the Path objects for the files before the index for the positive folder
    pos_train = [file for file in pos.iterdir() if int(file.name[2:5]) < index]
    pos_test = [file for file in pos.iterdir() if int(file.name[2:5]) >= index]

    # Create a list with the Path objects for the files before the index for the negative folder
    neg_train = [file for file in neg.iterdir() if int(file.name[2:5]) < index]
    neg_test = [file for file in neg.iterdir() if int(file.name[2:5]) >= index]

    return pos_train, pos_test, neg_train, neg_test


if __name__ == "__main__":
    main()
