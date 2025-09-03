'''Goal: Build an application that you can load a spreadsheet into, view recipes, and see pairwise similarities
in order to determine what recipes share the most ingredients. Potentially make a tree.'''

# imports
import sys # used to get csv file
import csv
import pandas as pd
from pandasgui import show
from itertools import combinations
from sklearn.metrics import jaccard_score
import numpy as np
import matplotlib.pyplot as plt

# global variables
fields = []  # Column names
rows = []    # Data rows


# - pandas dataframe


# - pairwise similarities table


# - Decision tree


# - Recipe viewer

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
        ingredients1 = recipes[recipe1]
        ingredients2 = recipes[recipe2]

        # Jaccard similarity: |A ∩ B| / |A ∪ B|
        intersection = len(ingredients1 & ingredients2)
        union = len(ingredients1 | ingredients2)
        similarity = intersection / union if union > 0 else 0.0

        similarity_matrix.loc[recipe1, recipe2] = similarity
        similarity_matrix.loc[recipe2, recipe1] = similarity

    # Fill the diagonal with 1s (each recipe is identical to itself)
    np.fill_diagonal(similarity_matrix.values, -1.0)

'''
    # open pandasgui for testing purposes. More to come
    show(similarity_matrix)
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
