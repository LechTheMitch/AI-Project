from knapsack import Knapsack

weights = list(map(int, input("Enter the Weights Seprated by spaces ").split(" ")))
values = list(map(int, input("Enter the Values Seprated by spaces ").split(" ")))

while len(values) != len(weights):
    values = list(map(int, input("Please enter the same number of values as waits ").split(" ")))
