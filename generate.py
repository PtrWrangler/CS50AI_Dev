from collections import deque
from genericpath import exists
import sys
from typing import overload

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

        print ("hello")

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            self.domains[variable] = [word for word in self.domains[variable] if len(word) == variable.length]

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # If there exists an overlapping letter for these two variables
        overlap_idxs = self.crossword.overlaps[x, y]
        if overlap_idxs is None:
            return False 

        # print ("\n")
        # print ("Letter index of x,y that overlap: " + str(self.crossword.overlaps[x, y]))
        # print ("Words available for var x: " + str(self.domains[x]))
        # print ("Words available for var y: " + str(self.domains[y]))

        # For each possible word in x, 
        #   if there exists a word in y that contains the overlap letter from x in the correct overlapping idx, 
        #   keep the x word in the variable domain, else remove it. 
        rervised = False
        for word_x in list(self.domains[x]):
            # print (word_x + " " + word_x[overlap_idxs[0]])
            overlap_letter = word_x[overlap_idxs[0]]
            possible_y_word = False
            for word_y in self.domains[y]:
                if overlap_letter == word_y[overlap_idxs[1]]:
                    possible_y_word = True
                    continue
            if not possible_y_word:
                # print ("before removal: " + str(self.domains[x]))
                self.domains[x].remove(word_x)
                # print ("after removal: " + str(self.domains[x]))
                rervised = True

        return rervised

                # possible_y_word = [ overlap_letter == word_y[overlap_idxs[1]] for word_y in self.domains[y] ]
                # print (word_x + " " + word_x[overlap_idxs[0]] + " " + str(possible_y_word))


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # Maintain a queue of the 'edges' between variables that have a binary contraint between them
        if arcs == None:
            arcs = deque()
            for var1 in self.crossword.variables:
                for var2 in self.crossword.neighbors(var1):
                    arcs.append((var1, var2))
        else:
            arcs = deque(arcs)

        # While arcs is not empty there are still edges we need to make arc consistent
        while arcs:
            x, y = arcs.pop()
            # Make variable x arc consisitent with y
            if self.revise(x, y):
                # If a change was made to variable x's domain...

                # If now there is nothing remaining in the domain of x, there is no way we can solve the Constraint Satisfaction Problem.
                if len(self.domains[x]) == 0:
                    return False

                # ...it MIGHT mean that another arc that WAS arc consistent with x, is no longer. So we need to add additional arcs that we might need to (re)check
                for neighbor_of_x in self.crossword.neighbors(x) - {y}:
                    arcs.appendleft((neighbor_of_x, x))
        return True
                    

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        # Validate assignment completion
        for var in self.crossword.variables:
            if var not in assignment.keys() or assignment[var] == None:
                return False

        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        already_compared = set()

        for var_x, word_x in assignment.items():
            for var_y, word_y in assignment.items():
                
                # Dont bother comparing the variable to itself
                if var_x == var_y:
                    continue

                # We only need to compare each variable to every other variable once
                if var_y in already_compared:
                    continue

                # Dont allow duplicate words in our crossword
                if word_x == word_y:
                    return False

                # If the variables have an overlap, make sure that the letter fits
                if self.crossword.overlaps[var_x, var_y] is not None:
                    var_x_overlap_idx, var_y_overlap_idx = self.crossword.overlaps[var_x, var_y]
                    if word_x[var_x_overlap_idx] != word_y[var_y_overlap_idx]:
                        return False

            already_compared.add(var_x)

        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        # return ordered list of vals in domain of var
        best_word_rankings = []

        # For each currently possible word in the domain of the current function variable...
        for word in self.domains[var]:
            count = 0
            
            # For each neighboring variable, how many words in their domain would we eliminate if we were to choose this word to assign to the function variable in question
            for neighbor_var in self.crossword.neighbors(var):
                overlap = self.crossword.overlaps[var, neighbor_var]

                # Count how many words we would eliminate based on the overlapping letters not being consistent
                for neighbor_var_word in self.domains[neighbor_var]:
                    if word[overlap[0]] != neighbor_var_word[overlap[1]]:
                        count += 1

            # Build the unsorted list of all the possible words for this var and the count of wordds choosing it would eliminate from neighboring vars
            best_word_rankings.append((word, count))

        # Sort the list and zip it into a list removing the weights
        best_word_rankings.sort(key=lambda x: x[1])
        best_word_ordered_list = [ranked_word[0] for ranked_word in best_word_rankings]
        
        return best_word_ordered_list


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        unassigned_variable = None

        # Find one of the variables that is not yet in the assignment
        for var in self.domains:
            if var not in assignment.keys():

                # We're looking for the variable with firstly the least remaining values, or secondarily the highest degree (num neighbors) to return
                if ( unassigned_variable is None or 
                     len(self.domains[var]) < len(self.domains[unassigned_variable]) or 
                     ( len(self.domains[var]) == len(self.domains[unassigned_variable]) and 
                     len(self.crossword.neighbors(var)) > 
                     len(self.crossword.neighbors(unassigned_variable)) )):
                    unassigned_variable = var

        return unassigned_variable


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        # Check if every line has been assigned a possible word
        if not self.assignment_complete(assignment):
            print ("Assignemnt incomplete. Not every line has a possible word.")
        else:
            return assignment
        
        # Get one of the variables that is not yet in the assignment
        var = self.select_unassigned_variable(assignment)

        # Consider all the values in this variables domain (in order of most promising words, that eliminate the least possibilities for other variables...)
        for value in self.order_domain_values(var, assignment):

            assignment[var] = value
            if self.consistent(assignment):

                result = self.backtrack(assignment)
                if result:
                    return result
            
            assignment.pop(var, None)
        return False      


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
