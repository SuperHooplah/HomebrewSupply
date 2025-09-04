'''Goal: Build an application that you can load a spreadsheet into, view recipes, and see pairwise similarities
in order to determine what recipes share the most ingredients. Potentially make a tree.'''

# imports

import pandas as pd
from pandasgui import show
from itertools import combinations, permutations
import numpy as np
import matplotlib.pyplot as plt

# - GUI and Recipe viewer

def main():
    '''
    # Get file from user
    if len(sys.argv) < 2:
        print("Usage: python HomebrewMain.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    '''

    filename = 'Ingredience - Master List.csv'

    # reads provided csv file and construct a dataframe
    IngredienceDF = pd.read_csv(filename)

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
        similarity = intersection / union if union > 0 else 0.0 # compact if is easier to think with

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
    We will then observe all of the values and prioritize the one with the highest similarity (Currently, Lawn Mower)
    '''

'''
    recipe_order, value = brute_force_tsp(similarity_matrix)
    print("Optimal order: " + recipe_order + "\nValue = " + value)
'''


''' 
    Credit to W3schools for the TSP methods. I've modified them to find the largest value (since higher similarity means
    more ingredients in common
'''

'''
def calculate_distance(route, distances):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distances.loc[route[i], route[i + 1]]
    total_distance += distances.loc[route[-1], route[0]]
    return total_distance

 # Time to put my $3000 pc to use lmao
def brute_force_tsp(distances):
    n = len(distances)
    nodes = list(range(1, n))
    longest_route = None
    max_distance = float('-inf')
    for perm in permutations(nodes):
        current_route = [0] + list(perm)
        current_distance = calculate_distance(current_route, distances)

        if current_distance > max_distance:
            max_distance = current_distance
            longest_route = current_route

    longest_route.append(0)
    return longest_route, max_distance
'''

'''
    making a plot with matplotlib.pyplot
    
    plt.bar(IngredienceDF['Name'], IngredienceDF['Amount'], color = 'skyblue')
    plt.xlabel("Ingredient Name")
    plt.ylabel("Amount")
    plt.title("My first chart lol")
    plt.show()
'''

if __name__ == "__main__":
    main()
