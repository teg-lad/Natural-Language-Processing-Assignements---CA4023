import math
import sys


def run(train_file, test_file):
    """
    This function is the main function of the script. It reads in the train and test data. Initializes the BigramModel
    class and calls its train method, computing the counts for the training corpus. The test data is then passed one
    sentence at a time to the BigramModel's predict_sentence method to compute the probability for the given sentence.
    :return:
    """
    # Read in the data and create a list with each training sentence as an element
    with open(train_file) as train:
        train_data = train.read().split("\n")

    # Initialize the BigramModel class which tracks the counts of words and bigrams
    model = BigramModel()

    # Pass the train data to the model to fill the counts dictionary
    model.train(train_data)

    # Read in the test data and split it the same way as the train data, on newlines
    with open(test_file) as test:
        test_data = test.read().split("\n")

    # For each test sentence, compute and print the probability to stdout
    for sentence in test_data:
        print(f"The probability for {sentence} is {model.predict_sentence(sentence)}")


class BigramModel:
    """
    The BigramModel class stores the counts for a given corpus of text. These can then be used to compute the
    probability of a new sentence.
    """

    def __init__(self):
        # Dictionary for storing the counts of both uni and bigrams
        self.counts = {}

    def increment_dict(self, word):
        """
        This function increments the counts dictionary for the given word/bigram, if a word/bigram is not already
        in the dictionary it is added.
        :param word: The word whose count we would like to increase
        """

        # Check if the word is in the dictionary keys
        if word in self.counts.keys():

            # If it is we increase the count
            self.counts[word] += 1
        else:

            # If it isn't, we add it to the dictionary.
            self.counts[word] = 1

    def train(self, corpus):
        """
        This function fills the counts dictionary using the given corpus.
        :param corpus: The text to be added to the counts dictionary
        """
        # For each sentence in the corpus
        for sentence in corpus:

            # Split the sentence into individual words
            words = sentence.split()

            # Count the occurrence of each word
            for word in words:
                self.increment_dict(word)

            # Count the occurrence of each bigram, moving a sliding window along one place each time.
            for i in range(len(words) - 1):
                self.increment_dict(" ".join(words[i:i + 2]))

    def predict_sentence(self, sentence):
        """
        This function takes a new sentence and computes the probability of this sentence using the counts from the
        train corpus.
        :param sentence: The sentence for which a probability should be computed.
        """

        # List to store the probabilities of all bigrams in the sentence
        probabilities = []

        # Split the sentence into the constituent words
        words = sentence.split()

        # For every bigram (we include the start and end tag of the sentence as this is additional information)
        # If we wished to drop this we could remove it from the training data and test data and treat the first word as
        # just P(w1)
        for i in range(len(words) - 1):
            count_of_bigram = self.counts[" ".join(words[i:i + 2])]
            count_of_prior = self.counts[words[i]]

            # Add the probability of this bigram to the list we have
            probabilities.append(count_of_bigram / count_of_prior)

        # Compute the probability for the sentence
        probability = math.prod(probabilities)

        # Note: As this example is small this is sufficient. For larger scale bigram models it may be worth getting the
        # sum of the log probabilites. This can be done as shown below using math.log and summing the list.

        # for i in range(len(words) - 1):
        #
        #     count_of_bigram = self.counts[" ".join(words[i:i + 2])]
        #     count_of_prior = self.counts[words[i]]
        #
        #     # Add the probability of this bigram to the list we have
        #     probabilities.append(math.log(count_of_bigram / count_of_prior))
        #
        # # Compute the probability for the sentence
        # probability = sum(probabilities)

        return probability


if __name__ == "__main__":
    # Run the script. Reads in training data, trains the model (gets counts). Reads the test data and computes the probs
    train_file = "training.txt"
    test_file = "test.txt"

    if len(sys.argv) > 1:
        train_file = sys.argv[1]
        test_file = sys.argv[2]

    run(train_file, test_file)
