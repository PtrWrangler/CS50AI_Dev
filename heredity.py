import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        ### Calculating the probabilities of the set of all people having genes/trait
        #   given all the possible permutations/combinations of people having possible one/two/zero genes 
        #   Observing each persons parents and/or using the std PROBS table in the process

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.
    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    
    joint_people_probability = 1.0
    
    for person in people:

        person_num_genes = 1 if person in one_gene else 2 if person in two_genes else 0
        person_has_trait = person in have_trait

        mother = people[person]['mother']
        father = people[person]['father']

        if mother is not None and father is not None:
            # person has rents and we need to calc the prob they have X gene(s) based on their rents

            parent_gene_probabs = {}

            for parent in mother, father:
                parent_num_genes = 1 if parent in one_gene else 2 if parent in two_genes else 0
                
                # For each parent, depending on current scenario of num genes, get probab of passing on a gene 
                if parent_num_genes == 0:
                    parent_gene_probabs[parent] = PROBS["mutation"]
                elif parent_num_genes == 1:
                    parent_gene_probabs[parent] = 0.5
                else:
                    parent_gene_probabs[parent] = 1 - PROBS["mutation"]
                
            # Calc probab of a person with X genes having the gene/trait
            if person_num_genes == 0:
                joint_people_probability *= (1 - parent_gene_probabs[mother]) * (1 - parent_gene_probabs[father])
            elif person_num_genes == 1:
                joint_people_probability *= ((1 - parent_gene_probabs[mother]) * parent_gene_probabs[father]) + ((1 - parent_gene_probabs[father]) * parent_gene_probabs[mother])
            else:
                joint_people_probability *= parent_gene_probabs[mother] * parent_gene_probabs[father]

            joint_people_probability *= PROBS["trait"][person_num_genes][person_has_trait]
                
        else:
            # Person does not have info about parents, calc gene/trait prob based on PROBS table
            joint_people_probability *= PROBS["gene"][person_num_genes] * PROBS["trait"][person_num_genes][person_has_trait]

    # Old debugging code, to be deleted.        
    # myStr = (str(person) + ": " + str(joint_people_probability) + "\n")
    # f.write(myStr)
    # print (myStr)

    return joint_people_probability



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    # Update each person's probabilities for genes and trait
    for person in probabilities:
        person_num_genes = 1 if person in one_gene else 2 if person in two_genes else 0
        person_has_trait = person in have_trait

        probabilities[person]['gene'][person_num_genes] += p
        probabilities[person]['trait'][person_has_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        person_probabs_gene     = probabilities[person]["gene"]
        person_probabs_trait    = probabilities[person]["trait"]

        gene_probabs_sum = 0

        # Sum up this person's probabs of having X number of genes
        for i in range(len(person_probabs_gene)):
            gene_probabs_sum += person_probabs_gene[i]

        # Normalize their gene probabs...
        for i in range(len(person_probabs_gene)):
            person_probabs_gene[i] /= gene_probabs_sum

        # Siilarly, normalize their trait probabs...
        trait_probabs_sum = person_probabs_trait[True] + person_probabs_trait[False]
        person_probabs_trait[True]  /= trait_probabs_sum
        person_probabs_trait[False] /= trait_probabs_sum


if __name__ == "__main__":
    main()
