import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Initialise probability distribution dict
    prob_dist = {webpage: 0 for webpage in corpus}

    # If Webpage has no links, give equal probability to all pages
    if len(list(corpus.get(page))) == 0:
        equal_probability = 1 / len(corpus)
        for webpage in corpus.keys():
            prob_dist[webpage] = equal_probability
    else:
        # Probability of following a link from the current page
        link_follow_prob = damping_factor / len(corpus.get(page))

        # Probability of random page
        random_page_prob = (1 - damping_factor) / len(corpus)

        # Sum the possible probabilities to the distribution (Marginalization?)
        for webpage in corpus:
            prob_dist[webpage] += random_page_prob
            if webpage in corpus.get(page):
                prob_dist[webpage] += link_follow_prob

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    print ("Sample PageRank:")
    
    # For each webpage key in corpus, initialize hit count
    page_hits = {webpage: 0 for webpage in corpus}
    
    # Randomly choose first page
    current_page = random.choice(list(corpus.items()))[0]
    page_hits[current_page] += 1
    print (f"  Random Surfer starting on page '{current_page}'")

    # Travel the corpus rand only and/or conditionally based on the damping factor, logging page hit counts
    for sample in range(n-1):
        transit_model = transition_model(corpus, current_page, damping_factor)

        # Travel to next page based on the transition model probabilities
        rand_val = random.uniform(0, 1)
        total_prob = 0

        for webpage, probability in transit_model.items():
            total_prob += probability
            if rand_val <= total_prob:
                current_page = webpage
                break

        # log a page hit for the newly chosen page selected using the transition model probabilities
        page_hits[current_page] += 1

    # Get the final page rank probabilities by dividing the page hits by the total numbert of samples
    page_ranks = {webpage: (hits/n) for webpage, hits in page_hits.items()}

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    print ("Iterate PageRank:")

    # Initialize the Page Ranks with equal probability for each page
    page_ranks_dict = {webpage: 1/len(corpus) for webpage in corpus}

    # Threshold of PageRank value convergence
    threshold = 0.0005

    # Loop until all all page rank changes are negligable
    nothing_changed = False
    while (not nothing_changed):
        nothing_changed = True
        
        # For each page that we are ranking...
        for ranked_page in page_ranks_dict:

            sigma = 0
            # If we find a page in the corpus that links to it...
            for webpage, links in corpus.items():
                if ranked_page not in links:
                    continue

                # Summation part of the Iterative PageRank Algorithm Formula
                sigma += page_ranks_dict[webpage] / len(links)
            
            # Applying the Iterative PageRank Algorithm Formula
            iterative_algo_formula_part1 = (1 - damping_factor) / len(corpus)
            iterative_algo_formula_part2 = damping_factor * sigma
            iterative_algo_formula_result = iterative_algo_formula_part1 + iterative_algo_formula_part2

            if abs(page_ranks_dict[ranked_page] - iterative_algo_formula_result) > threshold:
                page_ranks_dict[ranked_page] = iterative_algo_formula_result
                nothing_changed = False

    return page_ranks_dict
    

if __name__ == "__main__":
    main()
