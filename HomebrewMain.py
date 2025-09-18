'''Goal: Build an application that you can load a spreadsheet into, view recipes, and see pairwise similarities
in order to determine what recipes share the most ingredients. Potentially make a tree.'''


# imports
import sys
import pandas as pd
from pandasgui import show
import matplotlib.pyplot as plt
import Calculations.recipeCruncher as rc

def main():
    # Get file from user
    if len(sys.argv) < 2:
        filename = 'Ingredience - Master List.csv'
    else:
        filename = sys.argv[1]

    '''reads provided csv file and construct a dataframe. This script assumes the following fields in the provided
    CSV:
    
    'Recipe Name': STRING - The name of the recipe
    'Ingredient Type': STRING - The kind of ingredient in a general category (ex: Yeast, Malt, Hop)
    'Lifespan (in Days)': INTEGER - The Lifespan of the Ingredient
    'Name': STRING - The name of the specific ingredient (American Ale, Crystal/Caramel 80, Biscuit)
    'Amount': INTEGER - The amount used, typically specified in the Ingredient Type field.
    '''
    ingredience_df = pd.read_csv(filename)

    ''' Creates a dictionary of recipes that list all used ingredients
    key: String name of Recipe
    values: list of ingredients '''

    recipes = ingredience_df.groupby('Recipe Name')['Name'].apply(set).to_dict()
    recipe_names = sorted(recipes.keys())

    # Creates a data frame with recipe_names as both index and column
    similarity_matrix = pd.DataFrame(index=recipe_names, columns=recipe_names, dtype=float)

    # Compute the Jaccard similarity between a recipe

    similarity_matrix = rc.jaccard_pairs(recipes, similarity_matrix)

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

    recipe_order, value = rc.greedy_tsp(similarity_matrix, "Amber Ale")
    print("Optimal order: " + str(recipe_order) + "\nValue = " + str(value))

if __name__ == "__main__":
    main()
