import nltk
nltk.download('punkt')
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
NP -> N | N NP | N VP | P NP | Det Adj NP | Det N NP | Det N | Adj NP | Conj NP | Conj VP
VP -> V | V NP | V Adv NP | Adv V NP | Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # List of tokenized words from the sentence, to return
    words = []

    tokens = nltk.word_tokenize(sentence)
    for token in tokens:

        # Only keep words that have at least one alphabetic character
        if not any(c.isalpha() for c in token):
            continue

        # Make all letters lowercase before appending the tokenized word
        words.append(token.lower())

    return words

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    final_chunks = []

    # Do a NLR traversal of the nltk Tree keeping track of the lowest NP
    for node in tree:
        lowest_np = None
        # If current node is a NP node, keep track of it as the possible lowest NP node
        if isinstance(node, nltk.Tree) and node.label() == 'NP':
            lowest_np = node
        
        lower_chunks = []
        # Recursively call np_chunk to traverse each nltk tree node in the tree
        if isinstance(node, nltk.Tree) and len(node) > 0:
            lower_chunks = np_chunk(node)

        # keep track of the lowest NP chunk(s)
        if lower_chunks != []:
            final_chunks.extend(lower_chunks)
        elif lowest_np != None:
            final_chunks.append(lowest_np)

    return final_chunks


if __name__ == "__main__":
    main()
