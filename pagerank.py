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
    prob_dist = {webpage : 0 for webpage in corpus}

    # Probability of following a link from the current page
    link_follow_prob = damping_factor / len(corpus.get(page))

    # Probability of random page
    random_page_prob = (1 - damping_factor) / len(corpus)

    # If Webpage has no links, give equal probability to all pages
    if len(list(corpus.get(page))) == 0:
        print ("webpage has no links, equal probability for all pages.")
        equal_probability = 1 / len(corpus)
        for webpage in corpus.keys():
            prob_dist[webpage] = equal_probability
    else:
        # Sum the possible probabilities to the distribution (Marginalization?)
        for webpage in corpus:
            prob_dist[webpage] += random_page_prob
            if webpage in list(corpus.get(page)):
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
    
    # For each webpage key in corpus, initialize hit count
    page_hits = {webpage : 0 for webpage in corpus}
    
    # Randomly choose first page
    cur_page = random.choice(list(corpus.items()))[0]
    page_hits[cur_page] += 1

    # Travel the corpus rand only and/or conditionally based on the damping factor, logging page hit counts
    for sample in range(n-1):

        transit_model = transition_model(corpus, cur_page, DAMPING)

        # -----------------

        # Travel to next page based on the transition model probabilities
        rand_val = random.uniform(0,1)
        total_prob = 0

        for webpage, probability in transit_model.items():
            total_prob += probability
            if rand_val <= total_prob:
                curr_page = webpage
                break

        page_hits[curr_page] += 1

    # Get the final page rank probabilities by dividing the page hits by the total numbert of samples
    page_ranks = {webpage: (hits/n) for webpage, hits in page_hits.items()}

    return page_ranks

    #     damping_variable = random.uniform(0, 1)
    #     if damping_variable > damping_factor:
    #         # Choose random page from all pages in corpus
    #         cur_page = random.choice(list(corpus.items()))[0]
    #         page_hits[cur_page] += 1
    #         # print ("Random choice from all corpus: " + str(cur_page))
    #     else:
    #         # Follow random page from this page links
    #         # prev_page = cur_page
    #         cur_page = random.choice(list(corpus.get(cur_page)))
    #         page_hits[cur_page] += 1
    #         # print ("Random follow from " + str(prev_page) + ": " + str(cur_page))

    # print (str(page_hits))

    # # Turn the page hitcounts into a probability table
    # for key, val in page_hits.items():
    #     probability = {key : val/SAMPLES}
    #     page_hits.update(probability)
    #     # page_hits.get(key)[1] = val/SAMPLES

    # print (str(page_hits))

    # return page_hits



    # for page in corpus:
    #     print ("prob table starting from page " + str(page))
    #     transition_model(corpus, page, damping_factor)

    # return dict()



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    #Initialize the Page Ranks with equal probability for each page
    page_ranks_dict = {webpage : 1/len(corpus) for webpage in corpus}
    # print (str(page_ranks_dict))

    threshold = 0.001

    # Loop until all all page rank changes are negligable
    while (True):
        nothing_changed = True
        sum = 0
        # For each page that we are ranking...
        for ranked_page in page_ranks_dict:

            # If we find a page in the corpus that links to it...
            for webpage, links in corpus.items():
                if ranked_page not in links:
                    continue

                sum += page_ranks_dict[webpage] / len(links)
            
            new_page_rank = (1 - damping_factor) / len(corpus) + (damping_factor * sum)
            print ("ranked_page: " + str(ranked_page) + ", new_page_rank: " + str(new_page_rank) + ", page_ranks_dict[ranked_page]:" + str(page_ranks_dict[ranked_page]) + ", current sum: " + str(sum))
            if abs(page_ranks_dict[ranked_page] - new_page_rank) > threshold:
                page_ranks_dict[ranked_page] = new_page_rank
                nothing_changed = False

        if nothing_changed == True:
            break


    return page_ranks_dict




    # # Calculate some constants from the corpus for further use:
    # num_pages = len(corpus)
    # init_rank = 1 / num_pages
    # random_choice_prob = (1 - damping_factor) / len(corpus)
    # iterations = 0

    # # Initial page_rank gives every page a rank of 1/(num pages in corpus)
    # page_ranks = {page_name: init_rank for page_name in corpus}
    # new_ranks = {page_name: None for page_name in corpus}
    # max_rank_change = init_rank

    # # Iteratively calculate page rank until no change > 0.001
    # while max_rank_change > 0.001:

    #     iterations += 1
    #     max_rank_change = 0

    #     for page_name in corpus:
    #         surf_choice_prob = 0
    #         for other_page in corpus:
    #             # If other page has no links it picks randomly any corpus page:
    #             if len(corpus[other_page]) == 0:
    #                 surf_choice_prob += page_ranks[other_page] * init_rank
    #             # Else if other_page has a link to page_name, it randomly picks from all links on other_page:
    #             elif page_name in corpus[other_page]:
    #                 surf_choice_prob += page_ranks[other_page] / len(corpus[other_page])
    #         # Calculate new page rank
    #         new_rank = random_choice_prob + (damping_factor * surf_choice_prob)
    #         new_ranks[page_name] = new_rank

    #     # Normalise the new page ranks:
    #     norm_factor = sum(new_ranks.values())
    #     new_ranks = {page: (rank / norm_factor) for page, rank in new_ranks.items()}

    #     # Find max change in page rank:
    #     for page_name in corpus:
    #         rank_change = abs(page_ranks[page_name] - new_ranks[page_name])
    #         if rank_change > max_rank_change:
    #             max_rank_change = rank_change

    #     # Update page ranks to the new ranks:
    #     page_ranks = new_ranks.copy()

    # print('Iteration took', iterations, 'iterations to converge')
    # print('Sum of iteration page ranks: ', round(sum(page_ranks.values()), 4))

    # return page_ranks


if __name__ == "__main__":
    main()
