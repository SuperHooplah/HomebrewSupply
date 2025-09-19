
# imports
from itertools import combinations
import numpy as np
import pandas as pd

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

def jaccard_pairs(ingredience_df):
    recipes = ingredience_df.groupby('Recipe Name')['Name'].apply(set).to_dict()
    recipe_names = sorted(recipes.keys())

    # Creates a data frame with recipe_names as both index and column
    similarity_matrix = pd.DataFrame(index=recipe_names, columns=recipe_names, dtype=float)

    for recipe1, recipe2 in combinations(sorted(recipes.keys()), 2):
            # gets two lists of the ingredients that make up the recipe
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

    # return
    return similarity_matrix

def weighted_jaccard_pairs(ingredience_df):
    recipes = ingredience_df.groupby('Recipe Name')['Name'].apply(set).to_dict()
    ingredient_types =ingredience_df.groupby('Name')['Ingredient Type'].first().to_dict()

    recipe_names = sorted(recipes.keys())
    weights = {
        'Yeast (packet)': 10,
        'Hops (grams)': 5,
        'Malt (ounces)': 1
    }
    # Creates a data frame with recipe_names as both index and column
    similarity_matrix = pd.DataFrame(index=recipe_names, columns=recipe_names, dtype=float)

    for recipe1, recipe2 in combinations(sorted(recipes.keys()), 2):
        # gets two lists of the ingredients that make up the recipe
        ingredients1 = recipes[recipe1]
        ingredients2 = recipes[recipe2]
        intersection_weight = 0
        union_weight = 0

        # Weighted Jaccard similarity: ∑|A ∩ B| / ∑|A ∪ B|
        intersection = ingredients1 & ingredients2
        union = ingredients1 | ingredients2

        # get weights of the items
        similarity = 0.0  # If there are no intersections, than it's going to be 0 / n which equals 0
        if len(intersection) > 0:
            for item in intersection:
                intersection_weight += weights[ingredient_types[item]]

            for item in union:
                union_weight += weights[ingredient_types[item]]

            if union_weight > 0:
                similarity = intersection_weight / union_weight

        similarity_matrix.loc[recipe1, recipe2] = similarity
        similarity_matrix.loc[recipe2, recipe1] = similarity

        # Fill the diagonal with -1s (each recipe is identical to itself)
        np.fill_diagonal(similarity_matrix.values, -1.0)

    return similarity_matrix
