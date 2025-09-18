
# imports
from itertools import combinations
import numpy as np

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

def jaccard_pairs(recipes, similarity_matrix):
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