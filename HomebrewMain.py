'''Goal: Build an application that you can load a spreadsheet into, view recipes, and see pairwise similarities
in order to determine what recipes share the most ingredients. Potentially make a tree.'''


# imports
import sys
import pandas as pd
from pandasgui import show
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt

# - GUI and Recipe viewer

def main():
    # Get file from user
    if len(sys.argv) < 2:
        filename = 'Ingredience - Master List.csv'
    else:
        filename = sys.argv[1]

    # reads provided csv file and construct a dataframe
    IngredienceDF = pd.read_csv(filename)

    # TODO: DELETE THIS WHEN FINISHED
    print(IngredienceDF.head())

    recipes = IngredienceDF.groupby('Recipe Name')['Name'].apply(set).to_dict()

    recipe_names = sorted(recipes.keys())

    similarity_matrix = pd.DataFrame(index=recipe_names, columns=recipe_names, dtype=float)

    # Compute Jaccard similarity for each pair
    for recipe1, recipe2 in combinations(recipe_names, 2):
        # gets two arrays of the ingredients that make up the recipe
        ingredients1 = recipes[recipe1]
        ingredients2 = recipes[recipe2]

        # Jaccard similarity: |A ∩ B| / |A ∪ B|
        intersection = len(ingredients1 & ingredients2)
        union = len(ingredients1 | ingredients2)
        if union > 0:
            similarity = intersection / union
        else:
            similarity = 0.0

        similarity_matrix.loc[recipe1, recipe2] = similarity
        similarity_matrix.loc[recipe2, recipe1] = similarity

    # Fill the diagonal with -1s (each recipe is identical to itself)
    np.fill_diagonal(similarity_matrix.values, -1.0)

    # open pandasgui for testing purposes.
    # show(similarity_matrix)

    '''So how do we solve the problem of working our way through the entire recipe book with as little waste as
    possible. Well, that just sounds like a Traveling Salesman problem! For those unaware, the TSP is a common
    issue in computational complexity where you try to find the lowest cost "route" between certain nodes. In our case,
    our TSP will use our similarity matrix in order to traverse to the next brew with the highest similarity.
    
    My basic idea is as follows
    We start with the Amber Ale, per the instructions of my friend who I am building this for in the first place.
    We will then observe all of the values and prioritize the one with the highest similarity.
    '''

    recipe_order, value = greedy_tsp(similarity_matrix, "Amber Ale")
    print("Optimal order: " + str(recipe_order) + "\nValue = " + str(value))



''' 
    Credit to W3schools for the TSP methods. I've modified them to find the largest value (since higher similarity means
    more ingredients in common):
    https://www.w3schools.com/dsa/dsa_ref_traveling_salesman.php
    
    For the more advanced algos, I plan to use this resource:
    https://codingclutch.com/solving-the-travelling-salesman-problem-in-python-a-comprehensive-guide/#dynamic-programming-held-karp-algorithm
'''

def greedy_tsp(similarity_matrix, start_node):
    n = len(similarity_matrix)
    nodes = similarity_matrix.columns.to_list()
    nodes.remove('Amber Ale')
    directions = {node: False for node in nodes}
    route = ['Amber Ale']
    total_distance = 0

    for j in range(1, n):
        last = route[-1]
        nearest = None
        max_dist = float('-inf')
        for i in nodes:
            if not directions[i] and similarity_matrix.loc[last, i] > max_dist:
                max_dist = similarity_matrix.loc[last, i]
                nearest = i
        route.append(nearest)
        directions[nearest] = True
        total_distance += max_dist

    return route, total_distance


''' 
    This program was made by an ace woman for her best friend who is also a woman and also gay. 
    Computer Science was built on the backs of gay men and unrecognized women. I will never be half the people they 
    were, but if I don't acknowledge what I am then people can pretend I didn't exist when the history books write
    about this time, like they tried to pretend my grandmothers didn't exist. 
'''

if __name__ == "__main__":
    main()
