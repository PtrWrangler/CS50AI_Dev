import nltk
nltk.download('stopwords')
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    file_content_mapping = {}

    # 
    if not os.path.isdir(directory):
        print (f"Error: {directory} is not a valid directory")
        exit()

    # Process all .txt files in directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)

            # read file contents into string
            with open(filepath, 'r') as file:
                filedata = file.read()

            file_content_mapping[filename] = filedata

    return file_content_mapping

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    words = []

    # Process each token/word in document
    tokens = nltk.word_tokenize(document)
    for token in tokens:
        processed_token = ""

        # Drop all punctuation characters
        for char in token:
            # It seems some punctuation chars are slipping thru... but the instructions say to use string.punctuation. I would have rather used isalnum()
            if char in string.punctuation:
                continue
            processed_token += char

        # Drop empty tokens
        if len(processed_token) < 1:
            continue

        # Drop stopwords
        if processed_token in nltk.corpus.stopwords.words("english"):
            continue
            
        # Lowercase token and append to return list
        words.append(processed_token.lower())

    # print (words)

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    print ("Computing IDFs...")
    
    IDFs = {}

    # For each document and document contents
    for doc, words in documents.items():

        # Create a set of unique words from the content
        unique_words = set(words)

        # Initialize the IDFs dictionary that starts by keeping track of each word and how many of the documents it appears in
        for word in unique_words:
            if word not in IDFs:
                IDFs[word] = 1
            else:
                IDFs[word] += 1

    
    # Recall that the inverse document frequency of a word is defined by taking the natural logarithm 
    #   of the number of documents divided by the number of documents in which the word appears
    # For each word, finalize the IDF value
    num_docs = len(documents.keys())
    for word, num_occuring_docs in IDFs.items():
        IDFs[word] = math.log(num_docs / num_occuring_docs)

    # print (IDFs)
    return IDFs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    # If a query word does not exist in any document, dont process it
    applicable_query_tokens = []
    for query_token in query:
        if not query_token in idfs.keys():
            print (f"Term {query_token} does not exist in any document, skipping.")
            continue
        applicable_query_tokens.append(query_token)

    print ("Calculating term frequencies...")
    doc_metrics = []

    # For each doc and its content
    for doc, content in files.items():

        # Running total of tf_idf of each query term applicable in this doc
        doc_term_total_tf_idf = 0

        # For each term(token) in applicable query tokens, count the term frequency, calculate its tf_idf and keep a running total
        for query_token in applicable_query_tokens:
            term_freq = content.count(query_token)
            tf_idf = term_freq * idfs[query_token]
            doc_term_total_tf_idf += tf_idf

            # print (f"debugmr2: {doc} ({query_token}) {term_freq}")
            # All tf_idf of applicable query words that also appear in the file are to be summed up and placed in list of (docname, sum(tf_idf))

        if doc_term_total_tf_idf != 0:
            doc_metrics.append((doc, doc_term_total_tf_idf))
    
    print ("Computing top relevant documents...")

    # Sort doc_metrics by doc-term-total tf-idf rank:
    doc_metrics.sort(key=lambda tfidf: tfidf[1], reverse=True)

    ###
    print (f"doc_metrics: {doc_metrics}")

    # Keep top 'n' docs
    doc_metrics = doc_metrics[:n]

    # Return the list of just the top doc filenames
    top_docs = [doc[0] for doc in doc_metrics]

###
    print (f"top docs: {top_docs}")

    return top_docs

    


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    # [] query
    # {} sentence : words
    # {} word : IDF
    # n top sentences

    print ("Computing top sentences...")

    # If a query word does not exist in any document, dont process it
    applicable_query_tokens = []
    for query_token in query:
        if not query_token in idfs.keys():
            print (f"Term {query_token} does not exist in any document, skipping.")
            continue
        applicable_query_tokens.append(query_token)

###
    print (f"query: {query}") 

    matching_word_measures = []

    # i = 0

    # For each sentence and its words
    for sentence, words in sentences.items():
        # print (sentence)
        # print ("")

        # Keep track of how many query tokens 
        query_token_hits = 0
        # Keep a Running total of the IDF of each query term applicable in this sentence
        sentence_word_idf_sum = 0

###
        test = []
        if "ai" in words and "winter" in words:
            print ("---break---")
        
        # For each term(token) in query, accumulate the 'matching word measure'
        for query_token in applicable_query_tokens:

            # Only accumulate the IDF if the query token appears in the sentence words, also count number of appearances
            token_freq = words.count(query_token)
            if token_freq == 0:
                continue

            query_token_hits += token_freq
            sentence_word_idf_sum += idfs[query_token]

            test.append(idfs[query_token])
            
            # print (f"debugmr1: {doc} ({query_token}) {term_freq}")

        if sentence_word_idf_sum != 0:
            sentence_query_token_density = query_token_hits / len(words)
            matching_word_measures.append((sentence, sentence_word_idf_sum, sentence_query_token_density, query_token_hits, len(words)))

    print ("Computing top relevant sentences...")

    # matching_word_measures.sort(key=lambda idf_sum: idf_sum[1], reverse=True)

    # f = open("out1.txt", "w")
    # matching_word_measures = matching_word_measures[:10]
    # for sentence, measure, query_token_hits, test in matching_word_measures:
    #     print (f"{sentence}\n   {measure}\n   {query_token_hits}\n   {test}\n", file=f)
    # f.close()


    # Sort doc_metrics by doc-term-total tf-idf rank:
    matching_word_measures = sorted(matching_word_measures, key=lambda query_metrics: (query_metrics[1], query_metrics[2]), reverse=True)
    # matching_word_measures.sort(key=lambda idf_sum: idf_sum[1], reverse=True)


    # new_list = sorted(a_list, key=lambda x: (len(x), x))


    f = open("out2.txt", "w")
    matching_word_measures = matching_word_measures[:10]
    for sentence, measure, sentence_query_token_density, query_token_hits, num_words in matching_word_measures:
        print (f"{sentence}\n   {measure}\n   {sentence_query_token_density}\n   {query_token_hits}\n   {num_words}\n", file=f)
    f.close()

    # Keep top 'n' matching word measures
    matching_word_measures = matching_word_measures[:n]

    # Return the list of just the top doc filenames
    top_sentences = [sentence[0] for sentence in matching_word_measures]


        # if i == 10:
        #     break

        # i += 1

    return top_sentences


if __name__ == "__main__":
    main()
