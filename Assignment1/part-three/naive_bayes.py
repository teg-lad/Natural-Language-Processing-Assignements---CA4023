import json
import math
import sys
import io
from pathlib import Path
import string
import shutil


def main(training_dir, test_path):
    """
    This is the main function that runs when the script is run. It reads in the data and splits it into train and test.
    The NaiveBayes class is initialized and passed the classes and alpha value.
    The model is then passed the training data to get the counts of documents and words. The probabilities are computed.
    Finally, the model is passed the test data and then prints the accuracy and outputs the data into the results
    folder. The folder contains a correct and incorrect sub-folder for classifications that are correct and incorrect,
    allowing for analysis.
    """

    # Compile a dictionary with the training data, the keys are the class names and the elements in the list are files.
    training_data = return_files(training_dir)

    # We need to check if the test_path is a .txt file and if so pull out the reviews that we want.
    if test_path[-4:] == ".txt":
        test_dir = create_folder(test_path)

    # If it isn't, we can treat it as normal.
    else:
        test_dir = test_path

    # Compile a dictionary with the test data, the keys are either the subfolder names, which may be class names,
    # or just a list of files under the key "files".
    testing_data = return_files(test_dir)

    # Initialize the NaiveBayes class with the class list and an alpha value of 0.9 for smoothing.
    model = NaiveBayes(training_data.keys(), 0.9)

    # Train the model by passing the training dictionary, this computes the probabilities from the counts of words and
    # documents.
    model.train(training_data)

    # Pass the test dictionary to the model. If the keys match the classes we return the accuracy and results
    # folder, otherwise return the predictions in the predictions' folder.
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

        # Total words for each class, probabilities of classes and words in each class.
        self.total_words = {}
        self.class_probabilities = {}
        self.probabilities = {}
        self.log_probabilities = {}
        self.class_probabilities_for_prediction = {}

        # For every class, add a dictionary in the counts and probabilities. Initialize the doc count for a class at 0.
        for cls in self.classes:
            self.counts[cls] = {}
            self.probabilities[cls] = {}
            self.log_probabilities[cls] = {}
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
        if self.classes == file_dict.keys():
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
                predicted, probabilities = self.predict_class(data)

                # Add the probabilities form each class to a dictionary under the filename, so we can compare them
                # during analysis.
                self.class_probabilities_for_prediction[file.name] = probabilities

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

        # Write probabilities for each individual prediction to a json for use during analysis.
        with open(output_path / "prediction_probabilities.json", "w") as pp:
            json.dump(self.class_probabilities_for_prediction, pp)

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
                self.probabilities[cls][word] = (word_count + self.alpha) / (self.total_words[cls] + (self.alpha * total_unique_words))

                # The log of this is taken, so we can sum the probabilities to find the total for a class.
                self.log_probabilities[cls][word] = math.log(self.probabilities[cls][word])

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
                    probabilities[cls].append(self.log_probabilities[cls][word])

            # The probability of this class given the content is the sum of the log probabilities.
            cls_prob = sum(probabilities[cls])

            # Now, we need to consider the prior, which we need to convert to a log and add to the probability.
            cls_prob += math.log(self.class_probabilities[cls])

            probabilities[cls] = cls_prob

        # Return the class with the higher probability and the dictionary with probabilities for both classes.
        return max(probabilities, key=probabilities.get), probabilities


def create_folder(text_file):
    """
    This function takes a text file with a new review on each line and converts it to a folder with a subfolder called
    data that has the reviews in separate text files. This allows for the .txt file format to be changed to the format
    currently accepted by the model.
    :param text_file: The name of the text file in the current working directory
    :return: The folder created
    """

    # Create a path for the text file and the output folder.
    text_path = Path.cwd() / text_file
    output_folder = text_path.parent / text_path.name[:-4] / "data"

    # Make a directory for the files to be written to.
    output_folder.mkdir(parents=True, exist_ok=True)

    # Open the text file and read the data, splitting on new lines.
    # This will result in a list of reviews.
    with io.open(text_path, mode="r", encoding="utf-8") as t:
        data = t.read().split("\n")

    # Iterate through the reviews and write them to a file in the new folder.
    for i in range(len(data)):
        with open((output_folder / f"{i}.txt"), "w") as tmp:
            tmp.write(data[i])

    # Return the path to the new folder, which is the parent of the data folder.
    return output_folder.parent


def return_files(dir: Path):
    """
    Iterates through the data folder, taking the subdirectories as the class labels. If subfolders are available but do
    not match the class labels from the training data the model will make predictions only.
    :param dir: Path object for the directory that contains data.
    :return: data
    """

    # Dictionary to store the data
    data = {}

    # For every subdirectory
    for cls in Path(dir).iterdir():
        cls_files = []

        # Add every file in the subdirectory to a list.
        for file in cls.iterdir():
            cls_files.append(file)

        # Insert this list into the dictionary under the subdirectory name.
        data[cls.name] = cls_files

    return data


if __name__ == "__main__":
    training_dir = "training"
    test_dir = "test_with_gt" # This can be changed to the test directory for prediction only or a txt file to pass
    # reviews to be classified.

    if len(sys.argv) > 1: # If we have arguments, we can assign them.
        training_dir = sys.argv[1]
        test_dir = sys.argv[2]

    main(training_dir, test_dir)
