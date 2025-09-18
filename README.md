# HomebrewSupply
A python application that takes an input from an amateur alcohol homebrewer and gives the optimal order to make 
the recipes in, accounting for pairwise similarity between recipes and ingredient spoilage.

Currently, it needs to be run in the command line, and it will break as the file that is hardcoded into it is not
provided. I am working to add functionality for a text based GUI and adding custom files, but I am prioritizing the
original purpose of the project currently.

Great news though, it no longer takes 20000 years to run. (probably)

### Sources:

Jaccard Principle, based off of: https://www.geeksforgeeks.org/data-science/how-to-calculate-jaccard-similarity-in-python/

Credit to W3schools for the TSP methods. I've modified them to find the largest value (since higher similarity means more ingredients in common): https://www.w3schools.com/dsa/dsa_ref_traveling_salesman.php

or the more advanced algos, I plan to use this resource: https://codingclutch.com/solving-the-travelling-salesman-problem-in-python-a-comprehensive-guide