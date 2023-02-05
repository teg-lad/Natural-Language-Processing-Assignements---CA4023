## Bigram Language Model

The bigram language model implemented here takes the counts of the words and bigrams
and computes the probability of each bigram using the conditional probability
P(w2|w1) = P(w1, w2) / P(w1).

Running the Python file will produce the probabilities for all the sentences in the
test data. The contents of the training and test text files can be changed to get
new results. The filenames can be changed in the run method of bigram.py to use
different text files if needed. Though the desired output is produced by running
the script with no changes.

Folder contents:

+ [Bigram model - Python file](bigram.py)
+ [Training corpus](training.txt)
+ [Test sentences](test.txt)