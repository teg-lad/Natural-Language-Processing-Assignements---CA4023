import io
import re
import sys


# This script makes use of the io, re and sys libraries in Python. The io library is used to read in the file in utf-8 format
# to correctly load characters. The re library is used to find the occurrences of periods, quotation marks and
# exclamation marks that are not the end of a sentence. This allows for the text to then be split into the constituent
# sentences. The sys module is used to read in command line arguments as an option of running the script

def main(filename):
    """
    This function is the main body of the script. It opens the input file, finds where to split the text into sentences
    and writes the output to output.txt.
    """
    # We need to first read in the data from our input file
    with io.open(filename, mode="r", encoding="utf-8") as f:
        data = f.read()

    # Next we can call our function to find and replace the occurrences of periods, quotation and exclamation marks
    # that are not the end of a sentence.
    split_data = split_sentences(data)

    # Take the input filename, remove the .txt and add _split.txt. So the output file is the same name with _split
    output_filename = filename.rsplit(".", 1)[0] + "_split.txt"
    with io.open(output_filename, mode="w", encoding="utf-8") as o:
        o.write(split_data)


def split_sentences(text):
    """
    This function takes the text and finds the use of . ? and ! and replaces them with a placeholder, <False>, <False_q>
    and <False_e>. The text can then be split and these false occurrences replaced, this processed text is then
    returned.
    :param text: The body of text to be split into sentences
    :return: the body of text with each sentence on a new line
    """

    # These are a set of possible occurrences of a period in context that is likely not the end of a sentence
    prefixes = "(Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|Mt|www)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)[.]"
    websites = "[.](ie|com|net|org|io|gov|me|edu)"

    # Unfortunately, this method will fail to split a sentence when one of these possibilties occurs as the end of a
    # sentence.
    # E.g. Last week he travelled to the U.S. He flew in to New York on a jet.

    # Remove newline characters and join all the text together if it is disjoint.
    text = re.sub("\n", " ", text)

    # replace the times when a period is not the end with a placeholder "<false>"
    # Here we replace for prefixes such as Dr., suffixes such as Co. and web addresses
    text = re.sub(prefixes, "\\1<False>", text)
    text = re.sub(suffixes, "\\1<False>", text)
    text = re.sub(websites, "<False>\\1", text)
    text = re.sub("\.co\.uk", "<False>co<False>uk", text)  # .co.uk requires a different search than the generic

    # Now we can catch periods and abbreviations, this covers 2 and 3 letter long acronyms.
    text = re.sub("(\w)\.(\w)", "\\1<False>\\2", text)
    text = re.sub("(\w)[.](\w)[.](\w)[.]?", "\\1<False>\\2<False>\\3<False>", text)
    text = re.sub("(\w)[.](\w)[.]?", "\\1<False>\\2<False>", text)

    # This takes into account that the . ? or ! that happen at the end of quotation marks.
    text = re.sub("\.([\"|\'])", "<False>\\1", text)
    text = re.sub("\?([\"|\'])", "<False_q>\\1", text)
    text = re.sub("!([\"|\'])", "<False_e>\\1", text)

    # Let us say all remaining occurrences are true occurrences.
    text = re.sub("\.", ".<Split>", text)
    text = re.sub("\?", "?<Split>", text)
    text = re.sub("!", "!<Split>", text)

    # Replace the false occruences with the original character again as we know where to split the text,
    text = re.sub("<False>", ".", text)
    text = re.sub("<False_q>", "?", text)
    text = re.sub("<False_e>", "!", text)

    # Split the text at the split points, drop the last split as it is empty and strip each element of the list.
    text = text.split("<Split>")[:-1]
    striped = [sent.strip() for sent in text]

    # Return the text joined with newlines so that the sentences are each on a separate line.
    return "\n".join(striped)


if __name__ == "__main__":
    filename = ""  # Filename goes here

    if filename == "":
        filename = sys.argv[1]
        print(filename)

    main(filename)
