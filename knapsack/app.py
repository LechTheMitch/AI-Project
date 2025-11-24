from knapsack import Knapsack as K, ProblemType

def get_knapvalues(itemname: str):
    while True:
        try:
            knapvalues = list(map(int, input(f"Enter the {itemname} Seprated by spaces ").split()))

            if any(knapvalue <= 0 for knapvalue in knapvalues):
                print(f"All {itemname.lower()} must be positive integers")
                continue
        
            return knapvalues

        except ValueError:
            print(f"{itemname} must be positive integers")

capacity = int(input("Please enter the Sack's capacity "))
weights = get_knapvalues("Weights")

while True:
    values = get_knapvalues("Values")
    
    if len(weights) == len(values):
        break

    print("There must be as many values as there are weights")

s = K(ProblemType.BOUNDED, capacity, weights, values)
s.test_print(weights[0])