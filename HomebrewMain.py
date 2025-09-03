'''Goal: Build an application that you can load a spreadsheet into, view recipes, and see pairwise similarities
in order to determine what recipes share the most ingredients. Potentially make a tree.'''

# imports
import sys # used to get csv file
import csv
import pandas as pd
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
